#!/usr/bin/env python3
"""
Quick Start Script for Binance Account Verification System
Run this script to verify the system is ready and start processing
"""

import os
import sys
import time
from datetime import datetime

def print_banner():
    """Print system banner"""
    print("=" * 70)
    print("🚀 BINANCE ACCOUNT VERIFICATION SYSTEM")
    print("   Advanced Proxy Rotation + Captcha Handling")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_system_ready():
    """Quick system readiness check"""
    print("🔍 Quick System Check...")
    
    checks = [
        ("Proxy Rotator", "proxy_rotator.py"),
        ("Main Script", "Binance-accounts.py"),
        ("JavaScript Handler", "bcaptcha.js"),
        ("Backup JS Handler", "bcaptcha2.js"),
        ("Input Directory", "待检测"),
        ("Input File", "待检测/numbers.txt"),
    ]
    
    all_good = True
    for name, path in checks:
        if os.path.exists(path):
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - Missing: {path}")
            all_good = False
    
    return all_good

def check_input_file():
    """Check if there are phone numbers to process"""
    input_file = "待检测/numbers.txt"
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if lines:
            print(f"📱 Found {len(lines)} phone numbers to process")
            print(f"   First few: {', '.join(lines[:3])}{'...' if len(lines) > 3 else ''}")
            return True
        else:
            print("❌ numbers.txt is empty")
            return False
    else:
        print("❌ numbers.txt not found")
        return False

def run_quick_tests():
    """Run quick tests to verify system functionality"""
    print("\n🧪 Running Quick Tests...")
    
    try:
        # Test proxy system
        from proxy_rotator import proxy_rotator
        proxy = proxy_rotator.get_smart_proxy()
        print(f"✅ Proxy System: {len(proxy_rotator.raw_proxies)} proxies loaded")
        
        # Test JavaScript
        import execjs
        with open('bcaptcha.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        result = ctx.call('jt', 100, 'test', '', 'Mozilla/5.0', 'Win32', 800, 900, 0, 0)
        print("✅ JavaScript System: Captcha handler working")
        
        return True
        
    except Exception as e:
        print(f"❌ System Test Failed: {e}")
        return False

def show_usage_options():
    """Show available options to the user"""
    print("\n" + "=" * 70)
    print("📋 AVAILABLE ACTIONS")
    print("=" * 70)
    
    print("⚠️  IMPORTANT: Make sure to activate the virtual environment first:")
    print("   .\\venv\\Scripts\\Activate.ps1")
    print()
    
    options = [
        ("1", "Start Account Verification", "python Binance-accounts.py"),
        ("2", "Test Proxy Rotation", "python test_proxy_rotation.py"),
        ("3", "Test JavaScript Execution", "python test_javascript.py"),
        ("4", "Run Comprehensive Tests", "python comprehensive_test.py"),
        ("5", "Analyze Errors/Performance", "python error_analysis.py"),
        ("6", "Test Recent Fixes", "python test_fixes.py"),
        ("7", "Test JSON Error Handling", "python test_json_fixes.py"),
        ("8", "View System Status", "python quick_start.py"),
    ]
    
    for num, desc, cmd in options:
        print(f"{num}. {desc}")
        print(f"   Command: {cmd}")
        print()
    
    print("🛑 To stop the main script safely: Press Ctrl+C")
    print("   The script now handles interruptions gracefully!")

def main():
    """Main quick start function"""
    print_banner()
    
    # System readiness check
    if not check_system_ready():
        print("\n❌ System not ready. Please ensure all files are present.")
        return False
    
    # Quick functionality tests
    if not run_quick_tests():
        print("\n❌ System tests failed. Please check error messages above.")
        return False
    
    # Check input file
    has_numbers = check_input_file()
    
    print("\n" + "=" * 70)
    print("✅ SYSTEM STATUS: READY FOR OPERATION")
    print("=" * 70)
    
    if has_numbers:
        print("🎯 Ready to process phone numbers!")
        print("\n💡 To start verification:")
        print("   python Binance-accounts.py")
        print("\n📊 To monitor performance:")
        print("   python test_proxy_rotation.py")
        print("   python error_analysis.py")
    else:
        print("📝 Add phone numbers to 待检测/numbers.txt first")
        print("   Format: One phone number per line")
        print("   Example: +1234567890")
    
    show_usage_options()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        
        print("\n" + "=" * 70)
        if success:
            print("🚀 System Ready! Choose an action above or run:")
            print("   python Binance-accounts.py")
        else:
            print("⚠️  Please fix issues before proceeding")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the system and try again.")
