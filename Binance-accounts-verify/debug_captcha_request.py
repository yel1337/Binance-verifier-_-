#!/usr/bin/env python3
"""
Debug the exact captcha request format being sent by the main script
"""

import json
import time
import requests
from urllib.parse import quote, urlencode

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Configuration
BASE_URL = 'https://accounts.binance.com'
PROXY = {
    'http': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323',
    'https': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323'
}

def create_realistic_captcha_data():
    """Create realistic captcha data like the main script would generate"""
    
    # This mimics what get_data() would return from JavaScript execution
    captcha_data = {
        "bizId": "test_session_12345",
        "distance": 156.78,
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "platform": "Win32", 
        "clientInterHeight": 937,
        "clientOuterHeight": 1040,
        "slideX": 52.5,
        "slideY": 183.2,
        "timestamp": int(time.time() * 1000),
        "version": "1.0.2"
    }
    
    return json.dumps(captcha_data, separators=(',', ':'))

def test_different_data_formats():
    """Test different ways to send the captcha data"""
    
    print("🔬 Testing Different Captcha Data Formats")
    print("=" * 50)
    
    captcha_json = create_realistic_captcha_data()
    print(f"📄 Base captcha data: {captcha_json[:100]}...")
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    
    # Test formats
    tests = [
        {
            "name": "Raw JSON String (current method)",
            "data": captcha_json,
            "headers": {
                'content-type': 'text/plain',
                'accept': '*/*',
                'origin': BASE_URL,
                'referer': f'{BASE_URL}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        },
        {
            "name": "URL-encoded with data param",
            "data": urlencode({'data': captcha_json}),
            "headers": {
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': BASE_URL,
                'referer': f'{BASE_URL}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        },
        {
            "name": "URL-encoded with sig param",
            "data": urlencode({'sig': captcha_json}),
            "headers": {
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': BASE_URL,
                'referer': f'{BASE_URL}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        },
        {
            "name": "URL-encoded with multiple params",
            "data": urlencode({
                'sig': captcha_json,
                'captchaType': 'bCAPTCHA',
                'timestamp': str(int(time.time() * 1000))
            }),
            "headers": {
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': BASE_URL,
                'referer': f'{BASE_URL}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        },
        {
            "name": "Raw JSON with captcha-sdk-version header",
            "data": captcha_json,
            "headers": {
                'content-type': 'text/plain',
                'captcha-sdk-version': '1.0.2',
                'accept': '*/*',
                'origin': BASE_URL,
                'referer': f'{BASE_URL}/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print("-" * 30)
        
        try:
            print(f"   📤 Data: {test['data'][:100]}...")
            print(f"   📤 Headers: {test['headers']}")
            
            response = requests.post(
                url,
                headers=test['headers'],
                data=test['data'],
                proxies=PROXY,
                timeout=15,
                verify=False
            )
            
            print(f"   📥 Status: {response.status_code}")
            print(f"   📥 Length: {len(response.text)}")
            
            if response.text.strip():
                try:
                    resp_json = response.json()
                    print(f"   📥 Response: {resp_json}")
                    
                    # Check for specific error messages
                    if 'errorData' in resp_json:
                        print(f"   ⚠️  Error: {resp_json['errorData']}")
                    if 'code' in resp_json:
                        print(f"   📋 Code: {resp_json['code']}")
                        
                except:
                    print(f"   📥 Text: {response.text[:200]}...")
            else:
                print("   📥 Response: EMPTY")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(2)

def analyze_current_script_behavior():
    """Analyze what exactly the current script is sending"""
    
    print("\n🔍 Analyzing Current Script Behavior")
    print("=" * 40)
    
    # Read the current captcha debug output from the logs
    print("Based on the logs, the current script:")
    print("1. ✅ Uses correct URL: /bapi/composite/v1/public/antibot/validateCaptcha")
    print("2. ✅ Gets captcha session data successfully")
    print("3. ✅ Generates captcha params via JavaScript")
    print("4. ❌ Sends data with content-type: text/plain")
    print("5. ❌ Receives empty responses")
    
    print("\nFrom the analyzer, we know:")
    print("- ❌ application/json content-type is NOT supported")
    print("- ❌ URL-encoded needs a 'sig' parameter")  
    print("- ❌ text/plain with current data format returns empty")
    
    print("\n💡 Hypothesis:")
    print("The endpoint expects:")
    print("- Content-Type: application/x-www-form-urlencoded")
    print("- Parameter name: 'sig' (not 'data')")
    print("- Value: The JSON string generated by JavaScript")

if __name__ == "__main__":
    print("🚀 Starting Captcha Debug Analysis...")
    
    try:
        test_different_data_formats()
        analyze_current_script_behavior()
        
        print(f"\n✅ Debug analysis complete!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
