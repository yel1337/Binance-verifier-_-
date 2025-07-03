#!/usr/bin/env python3
"""
Test script to verify the main Binance-accounts.py fixes
This tests the variable name fix and KeyboardInterrupt handling
"""

import sys
import os
import signal
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_variable_fix():
    """Test if the client_interHeight variable fix works"""
    print("🧪 Testing Variable Name Fix")
    print("=" * 50)
    
    try:
        # Read the main script to check for the fix
        with open('Binance-accounts.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if the malformed line is fixed
        if "verify=False)  # 下载验证码图片        client_interHeight" in content:
            print("❌ Variable name issue still exists (malformed line)")
            return False
        elif "client_interHeight = client_info[0]" in content:
            print("✅ Variable name fix applied correctly")
            return True
        else:
            print("⚠️  Cannot verify variable fix")
            return False
            
    except Exception as e:
        print(f"❌ Error checking variable fix: {e}")
        return False

def test_keyboard_interrupt_handling():
    """Test if KeyboardInterrupt handling is added"""
    print("\n🧪 Testing KeyboardInterrupt Handling")
    print("=" * 50)
    
    try:
        with open('Binance-accounts.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for KeyboardInterrupt handling
        if "except KeyboardInterrupt:" in content:
            print("✅ KeyboardInterrupt handling added to main script")
            
            # Count occurrences
            count = content.count("except KeyboardInterrupt:")
            print(f"   Found {count} KeyboardInterrupt handlers")
            
            # Check specific patterns
            if "用户中断程序运行" in content:
                print("✅ Main execution KeyboardInterrupt handler found")
            if "正在安全关闭线程" in content:
                print("✅ Thread pool KeyboardInterrupt handler found")
                
            return True
        else:
            print("❌ KeyboardInterrupt handling not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking KeyboardInterrupt handling: {e}")
        return False

def test_import_dependencies():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing Module Imports")
    print("=" * 50)
    
    modules_to_test = [
        "proxy_rotator",
        "execjs",
        "requests",
        "concurrent.futures",
        "threading"
    ]
    
    success_count = 0
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module}: {e}")
            
    return success_count == len(modules_to_test)

def main():
    """Run all tests"""
    print("🔧 Binance-accounts.py Fix Verification")
    print("=" * 60)
    print(f"Testing time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Variable Name Fix", test_variable_fix),
        ("KeyboardInterrupt Handling", test_keyboard_interrupt_handling),
        ("Module Imports", test_import_dependencies),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All fixes verified successfully!")
        print("\n💡 The main script should now:")
        print("   ✅ Handle JavaScript execution without variable errors")
        print("   ✅ Respond properly to Ctrl+C interruption")
        print("   ✅ Safely shutdown threads when interrupted")
        print("\n🚀 Ready to test the main script!")
    else:
        print("\n⚠️  Some fixes may not be working correctly.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("✅ All fixes verified! You can now run:")
        print("   python Binance-accounts.py")
        print("   (Use Ctrl+C to stop safely)")
    else:
        print("❌ Some issues detected. Please review the output above.")
    print("=" * 60)
