#!/usr/bin/env python3
"""
Test the final format: sig + bizId + data parameters
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

def test_final_format():
    """Test the final format: sig + bizId + data"""
    
    print("🔬 Testing Final Format: sig + bizId + data")
    print("=" * 50)
    
    # Sample captcha data
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
    
    # Convert to JSON string
    captcha_json = json.dumps(captcha_data, separators=(',', ':'))
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': BASE_URL,
        'referer': f'{BASE_URL}/',
        'user-agent': captcha_data['userAgent'],
        'captcha-sdk-version': '1.0.2'
    }
    
    # Test different combinations of sig, bizId, and data
    test_combinations = [
        {
            "name": "sig + bizId + data (JSON)",
            "params": {
                'sig': captcha_json,
                'bizId': str(captcha_data['bizId']),
                'data': captcha_json
            }
        },
        {
            "name": "sig + bizId + data (empty)",
            "params": {
                'sig': captcha_json,
                'bizId': str(captcha_data['bizId']),
                'data': ''
            }
        },
        {
            "name": "sig + bizId + data (timestamp)",
            "params": {
                'sig': captcha_json,
                'bizId': str(captcha_data['bizId']),
                'data': str(captcha_data['timestamp'])
            }
        },
        {
            "name": "data only (no sig/bizId)",
            "params": {
                'data': captcha_json
            }
        },
        {
            "name": "bizId + data (no sig)",
            "params": {
                'bizId': str(captcha_data['bizId']),
                'data': captcha_json
            }
        }
    ]
    
    for i, test in enumerate(test_combinations, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print("-" * 30)
        
        data = urlencode(test['params'])
        
        try:
            print(f"   📤 Parameters: {list(test['params'].keys())}")
            print(f"   📤 Data: {data[:100]}...")
            
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
                        return test['name']  # Return successful format
                    elif 'errorData' in resp_json:
                        print(f"   ⚠️  Error: {resp_json['errorData']}")
                        
                except:
                    print(f"   📥 Text: {response.text[:200]}...")
            else:
                print("   📥 Response: EMPTY")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(2)
    
    return None

if __name__ == "__main__":
    print("🚀 Testing Final Captcha Format...")
    
    try:
        successful_format = test_final_format()
        
        if successful_format:
            print(f"\n🎉 SUCCESS! Correct format: {successful_format}")
        else:
            print(f"\n❌ No successful format found")
            print("\n💡 Analysis summary:")
            print("   - Endpoint expects application/x-www-form-urlencoded")
            print("   - Requires: sig, bizId, data parameters")
            print("   - May need additional validation or real session data")
        
        print(f"\n📋 Next steps:")
        print("   1. Update validateCaptcha function with correct format")
        print("   2. Parse JSON from get_data() function")  
        print("   3. Send as URL-encoded form with required parameters")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
