#!/usr/bin/env python3
"""
Captcha Diagnostic Script
This script helps diagnose why validateCaptcha is receiving empty responses
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_connectivity():
    """Test basic connectivity to Binance"""
    print("🔍 Testing Basic Connectivity")
    print("=" * 50)
    
    test_urls = [
        "https://accounts.binance.info/",
        "https://www.binance.info/",
        "https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha"
    ]
    
    try:
        from proxy_rotator import proxy_rotator
        proxy_dict = proxy_rotator.get_smart_proxy()
        proxies = {
            'http': proxy_dict['http'],
            'https': proxy_dict['https']
        }
        print(f"Using proxy: {proxy_dict['raw'][:50]}...")
        
        for url in test_urls:
            try:
                print(f"\n🌐 Testing: {url}")
                response = requests.get(url, proxies=proxies, timeout=10, verify=False)
                print(f"   Status: {response.status_code}")
                print(f"   Content-Length: {len(response.text)}")
                print(f"   Headers: {dict(response.headers)}")
                
                if response.status_code == 200 and len(response.text) > 0:
                    print("   ✅ Accessible")
                else:
                    print("   ❌ Issues detected")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error setting up proxy: {e}")
        return False
        
    return True

def test_captcha_endpoint():
    """Test the captcha validation endpoint specifically"""
    print("\n🔍 Testing Captcha Endpoint")
    print("=" * 50)
    
    try:
        from proxy_rotator import proxy_rotator
        proxy_dict = proxy_rotator.get_smart_proxy()
        proxies = {
            'http': proxy_dict['http'],
            'https': proxy_dict['https']
        }
        
        url = "https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha"
        
        # Test different request methods and data
        test_cases = [
            ("GET", None),
            ("POST", ""),
            ("POST", "test"),
            ("POST", '{"test": "data"}'),
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'text/plain',
            'captcha-sdk-version': '1.0.2'
        }
        
        for method, data in test_cases:
            try:
                print(f"\n🧪 Testing {method} with data: {repr(data)}")
                
                if method == "GET":
                    response = requests.get(url, headers=headers, proxies=proxies, timeout=10, verify=False)
                else:
                    response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=10, verify=False)
                
                print(f"   Status: {response.status_code}")
                print(f"   Content-Length: {len(response.text)}")
                print(f"   Response: {response.text[:200]}..." if response.text else "Empty")
                
                if response.headers:
                    print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_headers_and_requests():
    """Test different header combinations"""
    print("\n🔍 Testing Header Combinations")
    print("=" * 50)
    
    try:
        from proxy_rotator import proxy_rotator
        proxy_dict = proxy_rotator.get_smart_proxy()
        proxies = {
            'http': proxy_dict['http'],
            'https': proxy_dict['https']
        }
        
        url = "https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha"
        
        header_sets = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Content-Type': 'text/plain'
            },
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'text/plain',
                'captcha-sdk-version': '1.0.2',
                'origin': 'https://accounts.binance.info',
                'referer': 'https://accounts.binance.info/'
            }
        ]
        
        for i, headers in enumerate(header_sets, 1):
            try:
                print(f"\n🧪 Header Set {i}:")
                for key, value in headers.items():
                    print(f"   {key}: {value}")
                
                response = requests.post(url, headers=headers, data="test", proxies=proxies, timeout=10, verify=False)
                print(f"   Result: Status {response.status_code}, Length {len(response.text)}")
                
                if response.text:
                    print(f"   Response: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_proxy_detection():
    """Test if the proxy is being detected"""
    print("\n🔍 Testing Proxy Detection")
    print("=" * 50)
    
    try:
        from proxy_rotator import proxy_rotator
        
        # Test multiple proxies
        for i in range(3):
            proxy_dict = proxy_rotator.get_random_proxy()
            proxies = {
                'http': proxy_dict['http'],
                'https': proxy_dict['https']
            }
            
            print(f"\n🧪 Testing proxy {i+1}: {proxy_dict['raw'][:50]}...")
            
            # Test IP detection
            try:
                response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
                if response.status_code == 200:
                    ip_data = response.json()
                    print(f"   IP: {ip_data['origin']}")
                else:
                    print(f"   IP check failed: {response.status_code}")
            except Exception as e:
                print(f"   IP check error: {e}")
            
            # Test Binance response
            try:
                url = "https://accounts.binance.info/"
                response = requests.get(url, proxies=proxies, timeout=10, verify=False)
                print(f"   Binance status: {response.status_code}")
                print(f"   Binance content length: {len(response.text)}")
                
                # Check for blocking indicators
                if "blocked" in response.text.lower() or "403" in str(response.status_code):
                    print(f"   ⚠️  Possible blocking detected")
                else:
                    print(f"   ✅ Seems accessible")
                    
            except Exception as e:
                print(f"   Binance test error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all diagnostic tests"""
    print("🔧 Captcha System Diagnostics")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Connectivity", test_basic_connectivity),
        ("Captcha Endpoint", test_captcha_endpoint),
        ("Headers & Requests", test_headers_and_requests),
        ("Proxy Detection", test_proxy_detection),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
    
    print(f"\n{'='*60}")
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print("This diagnostic helps identify:")
    print("✅ Network connectivity issues")
    print("✅ Proxy blocking/detection")
    print("✅ Incorrect request headers")
    print("✅ API endpoint accessibility")
    print("✅ Response format issues")
    
    print("\n💡 Next steps:")
    print("1. Check if proxies are being blocked")
    print("2. Verify request headers match browser")
    print("3. Ensure captcha data format is correct")
    print("4. Test with different proxy providers if needed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Diagnostics interrupted by user")
    except Exception as e:
        print(f"\n❌ Diagnostic error: {e}")
