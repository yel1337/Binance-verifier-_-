#!/usr/bin/env python3
"""
Test the sig parameter hypothesis
"""

import json
import time
import requests
from urllib.parse import urlencode

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Configuration
BASE_URL = 'https://accounts.binance.com'
PROXY = {
    'http': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323',
    'https': 'http://14acfa7f9a57c:74f453f102@46.34.62.73:12323'
}

def test_sig_parameter():
    """Test sending the JSON as the sig parameter"""
    
    print("🔬 Testing sig Parameter Format")
    print("=" * 50)
    
    # Sample captcha data (what get_data generates as JSON string)
    captcha_json = json.dumps({
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
    }, separators=(',', ':'))
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': BASE_URL,
        'referer': f'{BASE_URL}/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    
    # Test 1: Only sig parameter
    print("\n📝 Test 1: Only sig parameter")
    print("-" * 30)
    
    data = urlencode({'sig': captcha_json})
    
    try:
        print(f"   📤 Data: sig={captcha_json[:100]}...")
        
        response = requests.post(
            url,
            headers=headers,
            data=data,
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
                
                if resp_json.get('status') == 'SUCCESS':
                    print("   🎉 SUCCESS! Found the correct format!")
                    if 'data' in resp_json and 'token' in resp_json['data']:
                        print(f"   🎯 Token: {resp_json['data']['token']}")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(2)
    
    # Test 2: sig + captcha-sdk-version header
    print("\n📝 Test 2: sig + captcha-sdk-version header")
    print("-" * 30)
    
    headers_with_version = headers.copy()
    headers_with_version['captcha-sdk-version'] = '1.0.2'
    
    try:
        response = requests.post(
            url,
            headers=headers_with_version,
            data=data,
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
                
                if resp_json.get('status') == 'SUCCESS':
                    print("   🎉 SUCCESS! Found the correct format!")
                    if 'data' in resp_json and 'token' in resp_json['data']:
                        print(f"   🎯 Token: {resp_json['data']['token']}")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(2)
    
    # Test 3: sig + additional common parameters
    print("\n📝 Test 3: sig + additional parameters")
    print("-" * 30)
    
    extended_data = urlencode({
        'sig': captcha_json,
        'captchaType': 'bCAPTCHA',
        'validateId': 'test_validate_123',
        'sessionId': 'test_session_123'
    })
    
    try:
        response = requests.post(
            url,
            headers=headers,
            data=extended_data,
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
                
                if resp_json.get('status') == 'SUCCESS':
                    print("   🎉 SUCCESS! Found the correct format!")
                    if 'data' in resp_json and 'token' in resp_json['data']:
                        print(f"   🎯 Token: {resp_json['data']['token']}")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing sig Parameter Hypothesis...")
    
    try:
        test_sig_parameter()
        
        print(f"\n✅ sig parameter test complete!")
        print("\n💡 If successful, update validateCaptcha to:")
        print("   1. Parse JSON string from get_data()")
        print("   2. Send as: urlencode({'sig': json_string})")
        print("   3. Content-Type: application/x-www-form-urlencoded")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
