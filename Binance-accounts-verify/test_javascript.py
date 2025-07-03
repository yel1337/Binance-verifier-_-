#!/usr/bin/env python3
"""
Test JavaScript execution to diagnose SyntaxError issues
"""

import execjs
import json
import time

def test_javascript_execution():
    print("Testing JavaScript Execution")
    print("=" * 40)
    
    # Test basic execjs functionality
    try:
        ctx = execjs.compile("function test() { return 'Hello World'; }")
        result = ctx.call('test')
        print(f"✅ Basic execjs test: {result}")
    except Exception as e:
        print(f"❌ Basic execjs failed: {e}")
        return False
    
    # Test bcaptcha.js
    try:
        with open('bcaptcha.js', 'r', encoding='utf-8') as f:
            js1 = f.read()
        
        ctx1 = execjs.compile(js1)
        
        # Test with sample data
        test_result = ctx1.call('jt', 100, "login", {}, "Mozilla/5.0", "Win32", 800, 900, 100, 200)
        print(f"✅ bcaptcha.js test successful")
        print(f"   Result: {test_result[:100]}...")
        
        # Validate JSON
        parsed = json.loads(test_result)
        print(f"   Parsed JSON keys: {list(parsed.keys())}")
        
    except Exception as e:
        print(f"❌ bcaptcha.js failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    # Test bcaptcha2.js
    try:
        with open('bcaptcha2.js', 'r', encoding='utf-8') as f:
            js2 = f.read()
        
        ctx2 = execjs.compile(js2)
        
        # Test with sample data
        test_result = ctx2.call('jt', [1, 2, 3], "login", {}, "Mozilla/5.0", "Win32", "test-id", 800, 900, 1200, 800, 600, 400)
        print(f"✅ bcaptcha2.js test successful")
        print(f"   Result: {test_result[:100]}...")
        
        # Validate JSON
        parsed = json.loads(test_result)
        print(f"   Parsed JSON keys: {list(parsed.keys())}")
        
    except Exception as e:
        print(f"❌ bcaptcha2.js failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False
    
    print("\n✅ All JavaScript tests passed!")
    return True

def test_error_scenarios():
    print("\nTesting Error Scenarios")
    print("=" * 30)
    
    try:
        with open('bcaptcha.js', 'r', encoding='utf-8') as f:
            js1 = f.read()
        
        ctx1 = execjs.compile(js1)
        
        # Test with None values
        try:
            result = ctx1.call('jt', None, None, None, None, None, None, None, None, None)
            print(f"✅ Handled None values: {result[:50]}...")
        except Exception as e:
            print(f"❌ Failed with None values: {e}")
        
        # Test with invalid types
        try:
            result = ctx1.call('jt', "invalid", [], {}, None, "", -1, -1, "x", "y")
            print(f"✅ Handled invalid types: {result[:50]}...")
        except Exception as e:
            print(f"❌ Failed with invalid types: {e}")
            
    except Exception as e:
        print(f"❌ Error scenario test failed: {e}")

if __name__ == "__main__":
    success = test_javascript_execution()
    if success:
        test_error_scenarios()
    else:
        print("\n❌ JavaScript execution has issues that need to be fixed.")
        print("\nTroubleshooting suggestions:")
        print("1. Check if Node.js is properly installed")
        print("2. Verify PyExecJS is working correctly")
        print("3. Check JavaScript file syntax")
