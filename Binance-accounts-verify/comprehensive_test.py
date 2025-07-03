#!/usr/bin/env python3
"""
Comprehensive test suite for the Binance account verification system
Tests proxy rotation, JavaScript execution, and main functionality
"""

import sys
import os
import time
import json
from datetime import datetime

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from proxy_rotator import proxy_rotator
import execjs

def test_proxy_system():
    """Test the proxy rotation system"""
    print("🔄 Testing Proxy System")
    print("=" * 50)
    
    try:
        # Test proxy loading
        total_proxies = len(proxy_rotator.raw_proxies)
        print(f"✅ Loaded {total_proxies} proxies")
        
        if total_proxies == 0:
            print("❌ No proxies loaded from config")
            return False
              # Test different rotation methods
        smart_proxy = proxy_rotator.get_smart_proxy()
        round_robin_proxy = proxy_rotator.get_round_robin_proxy()
        random_proxy = proxy_rotator.get_random_proxy()
        
        print(f"✅ Smart proxy: {smart_proxy['raw'][:50]}...")
        print(f"✅ Round robin proxy: {round_robin_proxy['raw'][:50]}...")
        print(f"✅ Random proxy: {random_proxy['raw'][:50]}...")
        
        # Test proxy stats
        proxy_rotator.print_stats()
        
        return True
        
    except Exception as e:
        print(f"❌ Proxy system error: {e}")
        return False

def test_javascript_execution():
    """Test JavaScript execution for captcha handling"""
    print("\n🔧 Testing JavaScript Execution")
    print("=" * 50)
    
    try:
        # Test bcaptcha.js
        with open('bcaptcha.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
            
        ctx = execjs.compile(js_code)
        result = ctx.call('jt', 100, 'login', '', 'Mozilla/5.0', 'Win32', 800, 900, 0, 0)
        
        # Parse and validate result
        data = json.loads(result)
        expected_keys = ['bizId', 'distance', 'userAgent', 'platform', 'clientInterHeight', 
                        'clientOuterHeight', 'slideX', 'slideY', 'timestamp', 'version']
        
        missing_keys = [key for key in expected_keys if key not in data]
        if missing_keys:
            print(f"❌ Missing keys in JS result: {missing_keys}")
            return False
            
        print("✅ JavaScript execution successful")
        print(f"   Timestamp: {data['timestamp']}")
        print(f"   Version: {data['version']}")
        
        return True
        
    except Exception as e:
        print(f"❌ JavaScript execution error: {e}")
        return False

def test_config_loading():
    """Test configuration file loading"""
    print("\n📁 Testing Configuration Loading")
    print("=" * 50)
    
    try:        # Test config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # The config currently has proxies section (legacy)
        if 'proxies' in config:
            print("✅ config.json loaded successfully (legacy format)")
        else:
            print("❌ config.json format unknown")
            return False
        
        # Test other required files
        required_files = ['useragents.txt', 'countries.json', 'lat.json']
        for file in required_files:
            if not os.path.exists(file):
                print(f"❌ Missing required file: {file}")
                return False
                
        print(f"✅ All required files present: {', '.join(required_files)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading error: {e}")
        return False

def test_directory_structure():
    """Test directory structure for account processing"""
    print("\n📂 Testing Directory Structure")
    print("=" * 50)
    
    required_dirs = ['待检测', '已激活', '未注册', '检测失败']
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
                print(f"✅ Created directory: {dir_name}")
            except Exception as e:
                print(f"❌ Failed to create directory {dir_name}: {e}")
                return False
        else:
            print(f"✅ Directory exists: {dir_name}")
            
    return True

def test_main_imports():
    """Test importing the main Binance-accounts module"""
    print("\n🐍 Testing Main Module Imports")
    print("=" * 50)
    
    try:
        # Test importing main components
        import requests
        import concurrent.futures
        import ddddocr
        from PIL import Image
        import cv2
        import numpy as np
        
        print("✅ All required packages imported successfully")
        
        # Test if main script can be imported (partially)
        print("✅ Main dependencies verified")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🧪 Binance Account Verification System - Comprehensive Test")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Directory Structure", test_directory_structure),
        ("Main Module Imports", test_main_imports),
        ("Proxy System", test_proxy_system),
        ("JavaScript Execution", test_javascript_execution),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 70)
    print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All systems operational! Ready for production use.")
        print("\n💡 Next steps:")
        print("   1. Run the main Binance-accounts.py script")
        print("   2. Monitor proxy rotation and error handling")
        print("   3. Check logs for any issues during operation")
    else:
        print("⚠️  Some tests failed. Please review and fix issues before running.")
        
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
