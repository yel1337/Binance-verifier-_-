#!/usr/bin/env python3
"""
Captcha Solution Debugger
Focuses specifically on why captcha token is empty and how to improve solving accuracy
"""

import sys
import os
import time
import requests
import json
import cv2
import numpy as np
import base64
import execjs
from datetime import datetime
from io import BytesIO
from PIL import Image

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def download_and_analyze_captcha(url, proxies):
    """Download and analyze a captcha image"""
    print(f"🖼️ Downloading captcha: {url}")
    
    try:
        response = requests.get(url, proxies=proxies, timeout=15, verify=False)
        if response.status_code != 200:
            print(f"   ❌ Failed to download: {response.status_code}")
            return None, None
            
        # Save original image
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        print(f"   📏 Image size: {img.size}")
        
        # Convert to CV2 format for analysis
        img_array = np.array(img)
        if len(img_array.shape) == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_cv = img_array
            
        # Analyze image properties
        print(f"   🔍 Image shape: {img_cv.shape}")
        print(f"   📊 Image dtype: {img_cv.dtype}")
        
        # Try to detect puzzle piece and background
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY) if len(img_cv.shape) == 3 else img_cv
        
        # Edge detection to find puzzle piece boundaries
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        print(f"   🧩 Found {len(contours)} potential puzzle pieces")
        
        # Find the largest contour (likely the puzzle piece)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            print(f"   📦 Largest piece bounding box: x={x}, y={y}, w={w}, h={h}")
            
            # Calculate center of puzzle piece
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"   🎯 Puzzle piece center: ({center_x}, {center_y})")
            
            return img_cv, {
                'center_x': center_x,
                'center_y': center_y,
                'bounding_box': (x, y, w, h),
                'area': cv2.contourArea(largest_contour)
            }
        else:
            print("   ❌ No puzzle piece detected")
            return img_cv, None
            
    except Exception as e:
        print(f"   ❌ Error analyzing captcha: {e}")
        return None, None

def test_distance_calculation_methods(puzzle_info):
    """Test different methods to calculate the puzzle distance"""
    print(f"\n🧮 Testing Distance Calculation Methods")
    print("=" * 50)
    
    if not puzzle_info:
        print("❌ No puzzle info available")
        return []
    
    # Assume background image width is standard (usually 300px for Binance)
    bg_width = 300
    piece_center_x = puzzle_info['center_x']
    
    methods = []
    
    # Method 1: Simple center-based calculation
    dist1 = bg_width - piece_center_x
    methods.append(('Center-based', dist1))
    print(f"   📏 Center-based distance: {dist1}")
    
    # Method 2: Adjusted for piece width
    piece_width = puzzle_info['bounding_box'][2]
    dist2 = bg_width - piece_center_x - (piece_width // 2)
    methods.append(('Width-adjusted', dist2))
    print(f"   📏 Width-adjusted distance: {dist2}")
    
    # Method 3: Percentage-based (common in real implementations)
    percentage = piece_center_x / puzzle_info['bounding_box'][0] if puzzle_info['bounding_box'][0] > 0 else 1
    dist3 = int(bg_width * (1 - percentage))
    methods.append(('Percentage-based', dist3))
    print(f"   📏 Percentage-based distance: {dist3}")
    
    # Method 4: Gap detection (look for the gap in background)
    # This would require analyzing the background image too
    dist4 = bg_width - piece_center_x + 10  # Add small offset
    methods.append(('Gap-adjusted', dist4))
    print(f"   📏 Gap-adjusted distance: {dist4}")
    
    return methods

def test_javascript_parameter_generation(dist_methods, bizId, validateId):
    """Test JavaScript parameter generation with different distances"""
    print(f"\n🔧 Testing JavaScript Parameter Generation")
    print("=" * 50)
    
    try:
        # Load JavaScript context
        with open('bcaptcha2.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        CTX2 = execjs.compile(js_code)
        print("   ✅ JavaScript context loaded")
        
        # Standard parameters (similar to what's used in main script)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        platform = 'Windows'
        client_interHeight = 969
        client_outerHeight = 1048
        client_w = 1920
        client_h = 1080
        center_x = 150  # Default assumption
        center_y = 150
        
        data = {
            'sessionId': 'test_session_' + str(int(time.time())),
            'validateId': validateId
        }
        
        results = []
        
        for method_name, dist in dist_methods:
            print(f"\n   🧪 Testing {method_name} (distance: {dist})")
            
            try:
                param = CTX2.call('jt', dist, bizId, data, headers['user-agent'], platform, validateId,
                                client_interHeight, client_outerHeight, client_w, client_h, center_x, center_y)
                
                # Parse the generated parameter
                if isinstance(param, str):
                    try:
                        param_json = json.loads(param)
                        print(f"      ✅ Parameter generated successfully")
                        print(f"      📊 Keys: {list(param_json.keys())}")
                        if 'data' in param_json:
                            print(f"      📊 Data keys: {list(param_json['data'].keys()) if isinstance(param_json['data'], dict) else 'not dict'}")
                        
                        results.append({
                            'method': method_name,
                            'distance': dist,
                            'param': param,
                            'success': True
                        })
                        
                    except json.JSONDecodeError:
                        print(f"      ❌ Invalid JSON generated")
                        results.append({
                            'method': method_name,
                            'distance': dist,
                            'param': str(param)[:100] + '...',
                            'success': False
                        })
                else:
                    print(f"      ❌ Non-string parameter: {type(param)}")
                    results.append({
                        'method': method_name,
                        'distance': dist,
                        'param': str(param)[:100] + '...',
                        'success': False
                    })
                    
            except Exception as js_error:
                print(f"      ❌ JavaScript error: {js_error}")
                results.append({
                    'method': method_name,
                    'distance': dist,
                    'param': f'Error: {js_error}',
                    'success': False
                })
        
        return results
        
    except Exception as e:
        print(f"   ❌ Failed to load JavaScript: {e}")
        return []

def test_validatecaptcha_with_params(param_results, proxies):
    """Test validateCaptcha endpoint with different generated parameters"""
    print(f"\n🔍 Testing validateCaptcha with Generated Parameters")
    print("=" * 60)
    
    url = 'https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha'
    
    for result in param_results:
        if not result['success']:
            continue
            
        print(f"\n   🧪 Testing {result['method']} (distance: {result['distance']})")
        
        try:
            # Parse the parameter to extract bizId
            param_data = result['param']
            if isinstance(param_data, str):
                try:
                    parsed_data = json.loads(param_data)
                    biz_id = parsed_data.get('bizId', 'login')
                except:
                    biz_id = 'login'
            else:
                biz_id = 'login'
            
            # Prepare form data
            from urllib.parse import urlencode
            form_data = {
                'sig': param_data,
                'bizId': biz_id,
                'data': param_data
            }
            
            # Headers
            form_headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': 'https://accounts.binance.info',
                'referer': 'https://accounts.binance.info/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'captcha-sdk-version': '1.0.2'
            }
            
            # Make request
            encoded_data = urlencode(form_data)
            response = requests.post(url, headers=form_headers, data=encoded_data, 
                                   proxies=proxies, timeout=15, verify=False)
            
            print(f"      📤 Request status: {response.status_code}")
            print(f"      📏 Response length: {len(response.text)}")
            
            if response.text:
                try:
                    res_json = response.json()
                    print(f"      📊 Response: {res_json}")
                    
                    if res_json.get('success') == True and res_json.get('code') == '000000':
                        token = res_json.get('data', {}).get('token', '')
                        if token:
                            print(f"      ✅ SUCCESS! Token obtained: {token[:20]}...")
                            return result, res_json
                        else:
                            result_code = res_json.get('data', {}).get('result', 'unknown')
                            print(f"      ⚠️ Empty token, result code: {result_code}")
                    else:
                        print(f"      ❌ Failed: {res_json}")
                        
                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON response: {response.text[:100]}...")
            else:
                print(f"      ❌ Empty response")
                
        except Exception as e:
            print(f"      ❌ Request error: {e}")
    
    return None, None

def main():
    """Main diagnostic function"""
    print("🔧 Captcha Solution Debugger")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
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
        proxies = None
        return
    
    # Test parameters
    bizId = 'login'
    validateId = 'test_' + str(int(time.time()))
    
    # Sample captcha URL (you might need to get a real one from the main script)
    sample_captcha_url = "https://bin.bnbstatic.com/image/antibot/SLIDE/img/20250622/01/994b98d362ba488e8c090ac7376f9e9c.png"
    
    # Step 1: Analyze captcha image
    print(f"\n🔍 Step 1: Captcha Image Analysis")
    print("-" * 40)
    img, puzzle_info = download_and_analyze_captcha(sample_captcha_url, proxies)
    
    # Step 2: Test distance calculation methods
    if puzzle_info:
        dist_methods = test_distance_calculation_methods(puzzle_info)
    else:
        # Use default distances for testing
        print(f"⚠️ Using default distance methods")
        dist_methods = [
            ('Default-50', 50),
            ('Default-100', 100),
            ('Default-150', 150),
            ('Default-200', 200)
        ]
    
    # Step 3: Test JavaScript parameter generation
    print(f"\n🔍 Step 2: JavaScript Parameter Generation")
    print("-" * 40)
    param_results = test_javascript_parameter_generation(dist_methods, bizId, validateId)
    
    # Step 4: Test validateCaptcha endpoint
    print(f"\n🔍 Step 3: validateCaptcha Testing")
    print("-" * 40)
    success_result, success_response = test_validatecaptcha_with_params(param_results, proxies)
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("=" * 60)
    if success_result:
        print(f"✅ SUCCESS! Best method: {success_result['method']}")
        print(f"   Distance: {success_result['distance']}")
        print(f"   Token: {success_response.get('data', {}).get('token', 'N/A')[:20]}...")
    else:
        print(f"❌ No successful token generation")
        print(f"💡 Possible issues:")
        print(f"   - Incorrect distance calculation")
        print(f"   - Wrong JavaScript parameters")
        print(f"   - Missing required data in JS execution")
        print(f"   - Binance detection of automation")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Try with real captcha images from get_data()")
    print(f"   2. Analyze successful browser requests")
    print(f"   3. Compare JS parameters with real browser")
    print(f"   4. Test with different mouse trajectories")

if __name__ == "__main__":
    main()
