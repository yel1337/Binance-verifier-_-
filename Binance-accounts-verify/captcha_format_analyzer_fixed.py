#!/usr/bin/env python3
"""
Captcha Format Analyzer - Fixed Version
Comprehensive testing of different data formats for Binance validateCaptcha endpoint
"""

import requests
import json
import time
import sys
import random
from urllib.parse import urlencode

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Test configuration
BASE_URL = 'https://accounts.binance.com'
TEST_PROXY = {
    'http': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323',
    'https': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323'
}

def get_test_headers():
    """Generate realistic test headers"""
    return {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain',
        'origin': BASE_URL,
        'referer': f'{BASE_URL}/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

def test_captcha_endpoint_formats():
    """Test different data formats for validateCaptcha endpoint"""
    
    print("🔍 Captcha Format Analyzer - FIXED VERSION")
    print("=" * 50)
    
    # Sample test data (mimicking what get_data would generate)
    test_data = {
        "bizId": "test_biz_123",
        "distance": 120,
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "platform": "Win32",
        "clientInterHeight": 937,
        "clientOuterHeight": 1040,
        "slideX": 50,
        "slideY": 200,
        "timestamp": int(time.time() * 1000),
        "validateId": "test_validate_123",
        "sessionId": "test_session_123",
        "captchaType": "bCAPTCHA"
    }
    
    # Test different data formats
    formats_to_test = [
        {
            "name": "JSON String (current)",
            "data": json.dumps(test_data, separators=(',', ':')),
            "content_type": "text/plain"
        },
        {
            "name": "JSON Object with application/json",
            "data": test_data,
            "content_type": "application/json"
        },
        {
            "name": "URL Encoded Form Data",
            "data": urlencode(test_data),
            "content_type": "application/x-www-form-urlencoded"
        },
        {
            "name": "JSON String with application/json",
            "data": json.dumps(test_data, separators=(',', ':')),
            "content_type": "application/json"
        },
        {
            "name": "Minimal JSON String",
            "data": json.dumps({
                "bizId": test_data["bizId"],
                "validateId": test_data["validateId"],
                "timestamp": test_data["timestamp"]
            }, separators=(',', ':')),
            "content_type": "text/plain"
        }
    ]
    
    # CORRECT URL from the main script
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    print(f"🎯 Testing URL: {url}")
    
    for i, format_test in enumerate(formats_to_test, 1):
        print(f"\n📝 Test {i}: {format_test['name']}")
        print("-" * 30)
        
        headers = get_test_headers()
        headers['content-type'] = format_test['content_type']
        
        try:
            # Determine how to send the data
            if format_test['content_type'] == 'application/json' and isinstance(format_test['data'], dict):
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=format_test['data'],
                    proxies=TEST_PROXY,
                    timeout=15, 
                    verify=False
                )
            else:
                response = requests.post(
                    url, 
                    headers=headers, 
                    data=format_test['data'],
                    proxies=TEST_PROXY,
                    timeout=15, 
                    verify=False
                )
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Length: {len(response.text)}")
            print(f"   Content-Type: {response.headers.get('content-type', 'Not specified')}")
            
            if response.text.strip():
                try:
                    response_json = response.json()
                    print(f"   Response JSON: {response_json}")
                except:
                    print(f"   Response Text: {response.text[:200]}...")
            else:
                print("   Response: EMPTY")
                
            # Check response headers for clues
            interesting_headers = ['x-trace-id', 'x-request-id', 'server', 'cache-control']
            for header in interesting_headers:
                if header in response.headers:
                    print(f"   {header}: {response.headers[header]}")
                    
        except Exception as e:
            print(f"   ERROR: {e}")
        
        time.sleep(2)  # Avoid rate limiting

def test_real_captcha_flow():
    """Test getting a real captcha session and trying to validate it"""
    
    print("\n🔄 Real Captcha Flow Test")
    print("=" * 50)
    
    try:
        # Step 1: Get a real captcha session
        headers = get_test_headers()
        headers['content-type'] = 'application/json'
        
        precheck_url = f'{BASE_URL}/bapi/accounts/v1/public/account/security/precheck'
        precheck_data = {
            "bizType": "login",
            "mobile": "1234567890",  # Test number
            "callingCode": "1"
        }
        
        print("📞 Getting real captcha session...")
        precheck_response = requests.post(
            precheck_url,
            headers=headers,
            json=precheck_data,
            proxies=TEST_PROXY,
            timeout=15,
            verify=False
        )
        
        print(f"   Precheck Status: {precheck_response.status_code}")
        print(f"   Precheck Response: {precheck_response.text[:300]}...")
        
        if precheck_response.status_code == 200 and precheck_response.text.strip():
            try:
                precheck_json = precheck_response.json()
                if precheck_json.get('data') and precheck_json['data'].get('sessionId'):
                    session_id = precheck_json['data']['sessionId']
                    validate_id = precheck_json['data'].get('validateId', '')
                    captcha_type = precheck_json['data'].get('captchaType', 'bCAPTCHA')
                    
                    print(f"   ✅ Got session: {session_id}")
                    print(f"   ✅ Validate ID: {validate_id}")
                    print(f"   ✅ Captcha Type: {captcha_type}")
                    
                    # Step 2: Test validateCaptcha with real session data
                    real_test_data = {
                        "bizId": session_id,
                        "validateId": validate_id,
                        "sessionId": session_id,
                        "captchaType": captcha_type,
                        "timestamp": int(time.time() * 1000),
                        "userAgent": headers['user-agent'],
                        "platform": "Win32"
                    }
                    
                    validate_url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
                    validate_headers = get_test_headers()
                    validate_headers['content-type'] = 'text/plain'
                    
                    print(f"\n🔄 Testing validateCaptcha with real session...")
                    validate_response = requests.post(
                        validate_url,
                        headers=validate_headers,
                        data=json.dumps(real_test_data, separators=(',', ':')),
                        proxies=TEST_PROXY,
                        timeout=15,
                        verify=False
                    )
                    
                    print(f"   Validate Status: {validate_response.status_code}")
                    print(f"   Validate Length: {len(validate_response.text)}")
                    if validate_response.text.strip():
                        print(f"   Validate Response: {validate_response.text}")
                    else:
                        print("   Validate Response: EMPTY")
                        
                else:
                    print("   ❌ No session data in precheck response")
                    print(f"   Full response: {precheck_json}")
            except Exception as e:
                print(f"   ❌ Error parsing precheck response: {e}")
        else:
            print("   ❌ Precheck failed")
            
    except Exception as e:
        print(f"   ❌ Real captcha flow error: {e}")

def analyze_headers_and_timing():
    """Analyze what headers and timing might be important"""
    
    print("\n📊 Headers and Timing Analysis")
    print("=" * 50)
    
    # Test different header combinations
    header_tests = [
        {
            "name": "Minimal headers",
            "headers": {
                'content-type': 'text/plain',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        },
        {
            "name": "Full browser headers",
            "headers": get_test_headers()
        },
        {
            "name": "With captcha SDK version",
            "headers": {**get_test_headers(), 'captcha-sdk-version': '1.0.2'}
        },
        {
            "name": "With X-Requested-With",
            "headers": {**get_test_headers(), 'x-requested-with': 'XMLHttpRequest'}
        }
    ]
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    test_data = json.dumps({"test": "data"}, separators=(',', ':'))
    
    for header_test in header_tests:
        print(f"\n🔬 Testing: {header_test['name']}")
        try:
            response = requests.post(
                url,
                headers=header_test['headers'],
                data=test_data,
                proxies=TEST_PROXY,
                timeout=10,
                verify=False
            )
            print(f"   Status: {response.status_code}")
            print(f"   Length: {len(response.text)}")
            if response.text.strip():
                print(f"   Response: {response.text[:100]}...")
        except Exception as e:
            print(f"   Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 Starting Captcha Format Analysis - FIXED VERSION...")
    
    try:
        test_captcha_endpoint_formats()
        time.sleep(3)
        test_real_captcha_flow()
        time.sleep(3)
        analyze_headers_and_timing()
        
        print(f"\n✅ Analysis complete!")
        print("\n💡 Key findings to look for:")
        print("   - Which data format gets a non-empty response")
        print("   - What status codes indicate success vs failure")
        print("   - Any response headers that give clues")
        print("   - Whether real session data makes a difference")
        
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
