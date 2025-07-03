#!/usr/bin/env python3
"""
Test sending captcha data as individual form parameters
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

def test_individual_parameters():
    """Test sending captcha data as individual form parameters"""
    
    print("🔬 Testing Individual Form Parameters")
    print("=" * 50)
    
    # Sample captcha data (what get_data generates)
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
    
    url = f'{BASE_URL}/bapi/composite/v1/public/antibot/validateCaptcha'
    
    # Test 1: Send all data as individual form parameters
    print("\n📝 Test 1: All parameters individually")
    print("-" * 30)
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': BASE_URL,
        'referer': f'{BASE_URL}/',
        'user-agent': captcha_data['userAgent']
    }
    
    # Convert all values to strings for form data
    form_data = {}
    for key, value in captcha_data.items():
        form_data[key] = str(value)
    
    data = urlencode(form_data)
    
    try:
        print(f"   📤 Data: {data[:150]}...")
        
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
                    print("   🎉 SUCCESS! This is the correct format!")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(2)
    
    # Test 2: Add additional parameters that might be needed
    print("\n📝 Test 2: With additional parameters")
    print("-" * 30)
    
    # Add some additional parameters that might be required
    extended_data = {
        **form_data,
        'captchaType': 'bCAPTCHA',
        'validateId': 'test_validate_123',
        'sessionId': 'test_session_123'
    }
    
    data = urlencode(extended_data)
    
    try:
        print(f"   📤 Data: {data[:150]}...")
        
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
                    print("   🎉 SUCCESS! This is the correct format!")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Minimal required parameters only
    print("\n📝 Test 3: Minimal parameters")
    print("-" * 30)
    
    minimal_data = {
        'bizId': captcha_data['bizId'],
        'timestamp': str(captcha_data['timestamp']),
        'userAgent': captcha_data['userAgent']
    }
    
    data = urlencode(minimal_data)
    
    try:
        print(f"   📤 Data: {data[:150]}...")
        
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
                    print("   🎉 SUCCESS! This is the correct format!")
                elif 'errorData' in resp_json:
                    print(f"   ⚠️  Error: {resp_json['errorData']}")
                    
            except:
                print(f"   📥 Text: {response.text[:200]}...")
        else:
            print("   📥 Response: EMPTY")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Individual Parameters Format...")
    
    try:
        test_individual_parameters()
        
        print(f"\n✅ Individual parameters test complete!")
        print("\n💡 Next step: Update validateCaptcha function to:")
        print("   1. Parse the JSON string from get_data()")
        print("   2. Send data as application/x-www-form-urlencoded")
        print("   3. Include all parameters individually")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
