import os
import re
import time
import random
import traceback
import threading
import sqlite3
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ───────────── 配置 ─────────────
DB_FILE     = "phone_numbers.db"
MAX_RETRIES = 5
URL         = "https://accounts.binance.com/zh-CN/login"

driver_init_lock = threading.Lock()

# ───────────── 日志函数 ─────────────
def log(phone, message, log_set):
    """仅打印未打印过的消息，每条消息都以 [phone] 开头"""
    full_msg = f"[{phone}] {message}"
    if full_msg not in log_set:
        print(full_msg)
        log_set.add(full_msg)

# ───────────── 数据库操作 ─────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers (
            phone  TEXT PRIMARY KEY,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def fetch_next_phone(conn):
    cur = conn.cursor()
    cur.execute("BEGIN IMMEDIATE")
    cur.execute("SELECT phone FROM phone_numbers WHERE status='Ready' LIMIT 1")
    row = cur.fetchone()
    if not row:
        conn.commit()
        return None
    phone = row[0]
    cur.execute("UPDATE phone_numbers SET status='Processing' WHERE phone=?", (phone,))
    conn.commit()
    return phone

def update_phone_status(conn, phone, new_status):
    conn.execute("UPDATE phone_numbers SET status=? WHERE phone=?", (new_status, phone))
    conn.commit()

# ───────────── 浏览器辅助 ─────────────
def _nuke_overlays(dr):
    dr.execute_script(
        "document.querySelectorAll("
        "'#onetrust-banner-sdk,#onetrust-consent-sdk,"
        ".oxnv-mask,.oxnv-dialog-mask,[class*=\"oxnv-dialog\"]').forEach(e=>e.remove());"
    )

def safe_click(dr, element, retries=3):
    for _ in range(retries):
        try:
            dr.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            dr.execute_script("arguments[0].click();", element)
            return True
        except Exception:
            time.sleep(0.3)
    return False

def _dismiss_onetrust(dr, timeout=8):
    try:
        banner = WebDriverWait(dr, timeout).until(
            EC.presence_of_element_located((By.ID, "onetrust-banner-sdk"))
        )
        btn = banner.find_element(
            By.CSS_SELECTOR, "#onetrust-accept-btn-handler, .onetrust-close-btn-handler"
        )
        safe_click(dr, btn)
        WebDriverWait(dr, 5).until(EC.invisibility_of_element(banner))
    except TimeoutException:
        _nuke_overlays(dr)
    except Exception:
        _nuke_overlays(dr)

def dismiss_cookie_banner(dr, timeout=8):
    cookie_selectors = [
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),
        (By.CSS_SELECTOR, ".ot-sdk-btn.ot-sdk-btn-primary"),
        (By.XPATH, "//button[contains(text(),'接受所有') or contains(text(),'Accept All')]")
    ]
    end = time.time() + timeout
    while time.time() < end:
        for by, sel in cookie_selectors:
            try:
                btn = dr.find_element(by, sel)
                if btn.is_displayed() and btn.is_enabled():
                    safe_click(dr, btn)
                    return
            except Exception:
                pass
        for iframe in dr.find_elements(By.TAG_NAME, "iframe"):
            try:
                dr.switch_to.frame(iframe)
                for by, sel in cookie_selectors:
                    elems = dr.find_elements(by, sel)
                    if elems and elems[0].is_displayed():
                        safe_click(dr, elems[0])
                        dr.switch_to.default_content()
                        return
            except Exception:
                pass
            finally:
                dr.switch_to.default_content()
        time.sleep(0.5)
    dr.execute_script(
        "document.querySelectorAll("
        "'#onetrust-banner-sdk, .ot-sdk-container, .cookie-consent')"
        ".forEach(el=>el.remove());"
    )

def dismiss_compliance_popup(dr, timeout=10):
    try:
        btn = WebDriverWait(dr, timeout).until(
            EC.element_to_be_clickable((By.ID, "binance_hk_compliance_popup_proceed"))
        )
        safe_click(dr, btn)
    except Exception:
        pass

def init_browser():
    opts = uc.ChromeOptions()
    # 保留加载插件：YesCaptcha 插件路径请根据实际情况调整
    extension_path = r"C:\Users\matth\Desktop\新建文件夹\币安\YesCaptcha"
    opts.add_argument(f"--disable-extensions-except={extension_path}")
    opts.add_argument(f"--load-extension={extension_path}")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    # 设置无头模式（可选）：新版 Chrome 推荐使用 --headless=new
    opts.add_argument("--headless=new")
    
    with driver_init_lock:
        dr = uc.Chrome(options=opts)
    dr.set_window_size(random.randint(900, 1600), random.randint(600, 1000))
    dr.set_window_position(random.randint(0, 300), random.randint(0, 300))
    dr.get(URL)
    _nuke_overlays(dr)
    _dismiss_onetrust(dr)
    dismiss_cookie_banner(dr)
    dismiss_compliance_popup(dr)
    WebDriverWait(dr, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    return dr

def human_type(el, txt):
    for ch in txt:
        el.send_keys(ch)
        time.sleep(0.04)

# ───────────── 用 DOM 检测并解决滑块验证码 ─────────────
def solve_slider_captcha_by_dom(driver, phone):
    log(phone, "进行验证码处理…", solve_slider_captcha_by_dom.logged)
    try:
        bg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bs-main-image"))
        )
        style = bg.get_attribute("style")
        m = re.search(
            r'background-image\s*:\s*url\(\s*(?:&quot;|["\'])(.*?)(?:&quot;|["\'])\s*\)',
            style
        )
        if m:
            image_url = m.group(1)
        else:
            log(phone, "无验证码背景图片URL", solve_slider_captcha_by_dom.logged)
            return
    except Exception:
        log(phone, "获取验证码背景失败", solve_slider_captcha_by_dom.logged)
        return

    try:
        from binance.slide import SlideSolver
        solver = SlideSolver(image_url)
        offset = solver.solve()
        if offset == 0:
            log(phone, "SlideSolver返回偏移量为0", solve_slider_captcha_by_dom.logged)
    except Exception:
        log(phone, "调用SlideSolver失败", solve_slider_captcha_by_dom.logged)
        return

    try:
        from selenium.webdriver import ActionChains
        slider = driver.find_element(By.CSS_SELECTOR, ".bs-slide-image")
        actions = ActionChains(driver)
        actions.click_and_hold(slider).pause(0.5).move_by_offset(offset, 0).release().perform()
        log(phone, "验证码拖动操作完成", solve_slider_captcha_by_dom.logged)
    except Exception:
        log(phone, "验证码拖动操作失败", solve_slider_captcha_by_dom.logged)

# 用于存储该函数内部的打印记录
solve_slider_captcha_by_dom.logged = set()

# ───────────── 主流程：手机号检测 ─────────────
def enter_phone_number(phone, attempt=1):
    logged_steps = set()  # 用于存储每个手机号的已打印日志
    log(phone, f"开始处理（尝试 {attempt}/{MAX_RETRIES}）", logged_steps)
    if attempt > MAX_RETRIES:
        log(phone, "重试超限，标记为 failed", logged_steps)
        return "failed"

    br = init_browser()
    wait = WebDriverWait(br, 15)
    final_text = ""
    success = False

    # 常用提示文本
    error_msg = "认证失败，请刷新页面后重试"
    net_err   = "Action failed. Please switch network"
    error_req = "我们无法处理您的请求，请稍后重试"
    reg1      = "请输入您的密码"
    reg2      = "通过通行密钥验证"
    not_found = "未找到币安账户"

    # 状态控制变量，确保每种错误仅触发一次刷新动作
    err_ref = False
    net_ref = False
    req_ref = False

    try:
        try:
            inp = wait.until(EC.presence_of_element_located((By.XPATH,
                "/html/body/div[2]/div[1]/main/div/div[1]/form/div/div/div/div/input"
            )))
        except TimeoutException:
            log(phone, "找不到输入框，刷新重试", logged_steps)
            try:
                br.quit()
            except Exception:
                pass
            time.sleep(1)
            return enter_phone_number(phone, attempt)
        
        human_type(inp, phone)
        inp.send_keys("\n")
        log(phone, "手机号已提交", logged_steps)

        # 等待并处理验证码提示
        try:
            WebDriverWait(br, 10, poll_frequency=0.5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]"))
            )
            log(phone, "检测到验证码提示，开始验证码处理", logged_steps)
            solve_slider_captcha_by_dom(br, phone)
        except TimeoutException:
            log(phone, "10秒内未检测到验证码提示，跳过验证码处理", logged_steps)

        log(phone, "等待最终状态更新…", logged_steps)
        try:
            final_element = WebDriverWait(br, 15, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, ("//*[contains(text(),'%s') or contains(text(),'%s') or "
                                "contains(text(),'%s') or contains(text(),'%s') or "
                                "contains(text(),'%s') or contains(text(),'%s')]")
                     % (reg1, reg2, not_found, error_msg, net_err, error_req))
                )
            )
            final_text = final_element.text.strip()
            if not_found not in final_text:
                log(phone, f"最终状态：{final_text}", logged_steps)
        except TimeoutException:
            log(phone, "最终状态等待超时", logged_steps)
            final_text = ""

        last_text = final_text
        while True:
            try:
                el = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ("//*[contains(text(),'%s') or contains(text(),'%s') or "
                                "contains(text(),'%s') or contains(text(),'%s') or "
                                "contains(text(),'%s') or contains(text(),'%s')]")
                     % (reg1, reg2, not_found, error_msg, net_err, error_req))
                ))
                new_text = el.text.strip()
            except TimeoutException:
                log(phone, "最终状态等待超时", logged_steps)
                break

            if new_text == last_text:
                break
            else:
                if not_found not in new_text:
                    log(phone, f"最终状态：{new_text}", logged_steps)
                last_text = new_text

            if error_msg in new_text and not err_ref:
                log(phone, "检测到认证失败提示，刷新后重试", logged_steps)
                br.refresh()
                time.sleep(2)
                WebDriverWait(br, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                wait = WebDriverWait(br, 15)
                inp = wait.until(EC.presence_of_element_located((By.XPATH,
                    "/html/body/div[2]/div[1]/main/div/div[1]/form/div/div/div/div/input"
                )))
                inp.send_keys(Keys.ENTER)
                err_ref = True
                try:
                    WebDriverWait(br, 15, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-bn-type='text' and contains(text(),'安全验证')]")
                        )
                    )
                    log(phone, "刷新后检测到安全验证提示，开始验证码处理", logged_steps)
                    solve_slider_captcha_by_dom(br, phone)
                except TimeoutException:
                    log(phone, "刷新后15秒内未检测到安全验证提示", logged_steps)
                continue

            if net_err in new_text and not net_ref:
                log(phone, "检测到网络错误提示，刷新后重试", logged_steps)
                br.refresh()
                time.sleep(2)
                WebDriverWait(br, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                wait = WebDriverWait(br, 15)
                inp = wait.until(EC.presence_of_element_located((By.XPATH,
                    "/html/body/div[2]/div[1]/main/div/div[1]/form/div/div/div/div/input"
                )))
                inp.send_keys(Keys.ENTER)
                net_ref = True
                try:
                    WebDriverWait(br, 15, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-bn-type='text' and contains(text(),'安全验证')]")
                        )
                    )
                    log(phone, "刷新后检测到安全验证提示，开始验证码处理", logged_steps)
                    solve_slider_captcha_by_dom(br, phone)
                except TimeoutException:
                    log(phone, "刷新后15秒内未检测到安全验证提示", logged_steps)
                continue

            if error_req in new_text and not req_ref:
                log(phone, "检测到请求失败提示，刷新后重试", logged_steps)
                br.refresh()
                time.sleep(2)
                WebDriverWait(br, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                wait = WebDriverWait(br, 15)
                inp = wait.until(EC.presence_of_element_located((By.XPATH,
                    "/html/body/div[2]/div[1]/main/div/div[1]/form/div/div/div/div/input"
                )))
                inp.send_keys(Keys.ENTER)
                req_ref = True
                try:
                    WebDriverWait(br, 15, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@data-bn-type='text' and contains(text(),'安全验证')]")
                        )
                    )
                    log(phone, "刷新后检测到安全验证提示，开始验证码处理", logged_steps)
                    solve_slider_captcha_by_dom(br, phone)
                except TimeoutException:
                    log(phone, "刷新后15秒内未检测到安全验证提示", logged_steps)
                continue

            break
        
        if reg1 in final_text or reg2 in final_text:
            log(phone, "账号状态判断：已注册", logged_steps)
            state = "Found"
            success = True
        elif not_found in final_text:
            log(phone, "账号状态判断：未注册", logged_steps)
            state = "NotFound"
            success = True
        else:
            log(phone, "账号状态判断：无法判定", logged_steps)
            state = "failed"

    except Exception:
        log(phone, "处理过程中异常", logged_steps)
        traceback.print_exc()
        state = "failed"

    finally:
        try:
            br.quit()
        except Exception:
            pass
        time.sleep(1)

    log(phone, f"最终处理结果 -> {state}", logged_steps)
    if not success:
        return enter_phone_number(phone, attempt + 1)
    return state

# ───────────── 主调度函数（方案 1） ─────────────
def schedule_workers():
    max_concurrent_threads = 10  # 同时允许的最大线程数
    active_threads = []          # 当前活跃线程列表

    # 建立独立的数据库连接供调度使用
    conn = sqlite3.connect(DB_FILE, timeout=30, check_same_thread=False)

    while True:
        # 清理已结束的线程
        active_threads = [t for t in active_threads if t.is_alive()]

        if len(active_threads) >= max_concurrent_threads:
            time.sleep(1)
            continue

        phone = fetch_next_phone(conn)
        if not phone:
            break  # 无待处理任务，则退出

        # 如果当前没有活动线程，则不等待，否则等待3～10秒
        if active_threads:
            delay = random.uniform(3, 10)
            print(f"等待 {delay:.1f} 秒后启动处理 {phone}")
            time.sleep(delay)
        else:
            print(f"立即启动处理 {phone}")

        # 定义线程任务：调用手机号处理，并更新数据库状态
        def worker_task(phone):
            res = enter_phone_number(phone)
            update_phone_status(conn, phone, res if res in ("Found", "NotFound") else "Ready")
          
        t = threading.Thread(target=worker_task, args=(phone,))
        t.start()
        active_threads.append(t)

    # 等待所有活动线程结束
    for t in active_threads:
        t.join()
    conn.close()

if __name__ == "__main__":
    init_db()
    schedule_workers()
    print("🎉 所有号码处理完毕！")