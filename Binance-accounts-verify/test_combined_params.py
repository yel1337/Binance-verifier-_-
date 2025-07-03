#!/usr/bin/env python3
"""
Test the final hypothesis: sig + individual parameters
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

def test_sig_plus_individual_params():
    """Test sending both sig parameter AND individual parameters"""
    
    print("🔬 Testing sig + Individual Parameters")
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
    
    # Convert to JSON string for sig parameter
    captcha_json = json.dumps(captcha_data, separators=(',', ':'))
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': BASE_URL,
        'referer': f'{BASE_URL}/',
        'user-agent': captcha_data['userAgent']
    }
    
    # Test 1: sig + all individual parameters
    print("\n📝 Test 1: sig + all individual parameters")
    print("-" * 30)
    
    form_data = {
        'sig': captcha_json,
        # Include all individual parameters as well
        'bizId': str(captcha_data['bizId']),
        'distance': str(captcha_data['distance']),
        'userAgent': str(captcha_data['userAgent']),
        'platform': str(captcha_data['platform']),
        'clientInterHeight': str(captcha_data['clientInterHeight']),
        'clientOuterHeight': str(captcha_data['clientOuterHeight']),
        'slideX': str(captcha_data['slideX']),
        'slideY': str(captcha_data['slideY']),
        'timestamp': str(captcha_data['timestamp']),
        'version': str(captcha_data['version'])
    }
    
    data = urlencode(form_data)
    
    try:
        print(f"   📤 Parameters: {len(form_data)} total")
        print(f"   📤 Has sig: Yes ({len(captcha_json)} chars)")
        print(f"   📤 Has bizId: {form_data.get('bizId', 'No')}")
        
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
    
    # Test 2: sig + minimal required parameters only
    print("\n📝 Test 2: sig + minimal required parameters")
    print("-" * 30)
    
    minimal_data = {
        'sig': captcha_json,
        'bizId': str(captcha_data['bizId']),
        'timestamp': str(captcha_data['timestamp'])
    }
    
    data = urlencode(minimal_data)
    
    try:
        print(f"   📤 Parameters: {len(minimal_data)} total")
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
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(2)
    
    # Test 3: sig + captcha-sdk-version header + key parameters
    print("\n📝 Test 3: sig + captcha-sdk-version + key parameters")
    print("-" * 30)
    
    headers_with_version = headers.copy()
    headers_with_version['captcha-sdk-version'] = '1.0.2'
    
    key_data = {
        'sig': captcha_json,
        'bizId': str(captcha_data['bizId']),
        'distance': str(captcha_data['distance']),
        'timestamp': str(captcha_data['timestamp']),
        'userAgent': str(captcha_data['userAgent'])
    }
    
    data = urlencode(key_data)
    
    try:
        print(f"   📤 Parameters: {len(key_data)} total")
        print(f"   📤 Headers: captcha-sdk-version added")
        
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

if __name__ == "__main__":
    print("🚀 Testing sig + Individual Parameters Hypothesis...")
    
    try:
        test_sig_plus_individual_params()
        
        print(f"\n✅ Combined parameters test complete!")
        print("\n💡 If successful, the correct format is:")
        print("   - Content-Type: application/x-www-form-urlencoded")
        print("   - sig parameter: JSON string from JavaScript")
        print("   - Individual parameters: bizId, distance, timestamp, etc.")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
