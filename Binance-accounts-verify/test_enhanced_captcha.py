#!/usr/bin/env python3
"""
Quick test of enhanced captcha solving
"""

import sys
import os
import time
import requests
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_captcha():
    """Test the enhanced captcha solving"""
    print("🧪 Testing Enhanced Captcha Solving")
    print("=" * 50)
    
    # Get proxy
    try:
        from proxy_rotator import proxy_rotator
        proxy_dict = proxy_rotator.get_smart_proxy()
        proxies = {
            'http': proxy_dict['http'],
            'https': proxy_dict['https']
        }
        print(f"🔗 Using proxy: {proxy_dict['raw'][:50]}...")
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        return
    
    # Test enhanced JS context
    try:
        import execjs
        with open('bcaptcha2_enhanced.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        print(f"✅ Enhanced JS context loaded")
        
        # Test parameters
        bizId = 'login'
        validateId = 'enhanced_test_' + str(int(time.time()))
        distance = 125
        
        data = {
            'sessionId': 'enhanced_session_' + str(int(time.time())),
            'validateId': validateId
        }
        
        # Call enhanced function
        param = ctx.call('jt_enhanced', distance, bizId, data, 
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Win32', validateId, 969, 1048, 1920, 1080, 150, 150)
        
        print(f"✅ Enhanced parameter generated: {len(param)} chars")
        
        # Parse and verify
        try:
            param_json = json.loads(param)
            print(f"📊 Parameter structure:")
            for key in param_json.keys():
                if key == 'trajectory':
                    print(f"   {key}: {len(param_json[key])} points")
                elif key == 'mouseBehavior':
                    print(f"   {key}: {param_json[key]}")
                else:
                    print(f"   {key}: {param_json[key]}")
        except:
            print(f"❌ Failed to parse parameter JSON")
            return
        
        # Test validateCaptcha endpoint
        print(f"\n🔍 Testing validateCaptcha endpoint...")
        
        url = 'https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha'
        
        from urllib.parse import urlencode
        form_data = {
            'sig': param,
            'bizId': bizId,
            'data': param
        }
        
        form_headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://accounts.binance.info',
            'referer': 'https://accounts.binance.info/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'captcha-sdk-version': '1.0.2'
        }
        
        encoded_data = urlencode(form_data)
        response = requests.post(url, headers=form_headers, data=encoded_data, 
                               proxies=proxies, timeout=15, verify=False)
        
        print(f"📤 Response status: {response.status_code}")
        
        if response.text:
            try:
                res_json = response.json()
                print(f"📊 Response: {res_json}")
                
                if res_json.get('success') == True:
                    token = res_json.get('data', {}).get('token', '')
                    result_code = res_json.get('data', {}).get('result', 'unknown')
                    
                    if token:
                        print(f"🎉 SUCCESS! Token: {token[:20]}...")
                        return True
                    else:
                        print(f"⚠️ Empty token, result: {result_code}")
                        if result_code == 2:
                            print(f"💡 Result 2 = Failed captcha solution")
                        elif result_code == 0:
                            print(f"💡 Result 0 = Success but empty token (test mode?)")
                else:
                    print(f"❌ Request failed")
                    
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON: {response.text[:100]}...")
        else:
            print(f"❌ Empty response")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔬 Enhanced Captcha Test")
    print("=" * 40)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    success = test_enhanced_captcha()
    
    print(f"\n📊 Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    if not success:
        print(f"\n💡 If still failing with result code 2:")
        print(f"   1. The enhanced trajectory might still not be realistic enough")
        print(f"   2. Binance might require actual captcha images from get_data()")
        print(f"   3. Need to analyze real browser requests more carefully")
        print(f"   4. Consider implementing ML-based distance calculation")

if __name__ == "__main__":
    main()
