#!/usr/bin/env python3
"""
Error Analysis and Monitoring Script for Binance Verification
"""

import re
import time
from collections import defaultdict, Counter
from datetime import datetime
from proxy_rotator import proxy_rotator

class ErrorMonitor:
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.proxy_errors = defaultdict(int)
        self.total_attempts = 0
        self.successful_attempts = 0
        
    def analyze_error(self, error_message, phone_number=None):
        """Analyze and categorize errors"""
        self.total_attempts += 1
        
        error_lower = error_message.lower()
        
        # Categorize errors
        if 'syntaxerror' in error_lower:
            self.error_counts['JavaScript SyntaxError'] += 1
            return 'js_error'
        elif 'tunnel failed' in error_lower or '502' in error_lower:
            self.error_counts['Proxy Connection Failed (502)'] += 1
            return 'proxy_error'
        elif 'timeout' in error_lower:
            self.error_counts['Connection Timeout'] += 1
            return 'timeout_error'
        elif 'connection' in error_lower:
            self.error_counts['Connection Error'] += 1
            return 'connection_error'
        elif 'captcha' in error_lower:
            self.error_counts['Captcha Error'] += 1
            return 'captcha_error'
        else:
            self.error_counts['Other Error'] += 1
            return 'other_error'
    
    def print_analysis(self):
        """Print error analysis"""
        print("\n" + "="*50)
        print("ERROR ANALYSIS REPORT")
        print("="*50)
        print(f"Total Attempts: {self.total_attempts}")
        print(f"Success Rate: {(self.successful_attempts/max(self.total_attempts,1)*100):.1f}%")
        print("\nError Breakdown:")
        for error_type, count in self.error_counts.items():
            percentage = (count/max(self.total_attempts,1)*100)
            print(f"  {error_type}: {count} ({percentage:.1f}%)")
        
        print("\nProxy Status:")
        proxy_rotator.print_stats()

def analyze_common_errors():
    """Analyze the common errors you're seeing"""
    
    print("COMMON ERROR ANALYSIS")
    print("="*50)
    
    print("\n1. SyntaxError: Syntax error")
    print("   - Cause: JavaScript execution issues in execjs")
    print("   - Solution: Added fallback handling for JS errors")
    print("   - Impact: Should be reduced with new error handling")
    
    print("\n2. curl: (56) CONNECT tunnel failed, response 502")
    print("   - Cause: Proxy server returning HTTP 502 error")
    print("   - Meaning: Proxy server cannot connect to target")
    print("   - Solution: Automatic proxy rotation and retry logic")
    print("   - Impact: System will try different proxies automatically")
    
    print("\n3. Connection timeout after 10026 milliseconds")
    print("   - Cause: Proxy or network latency issues")
    print("   - Solution: Retry with different proxy")
    print("   - Impact: Improved retry mechanism")

def check_proxy_health():
    """Check proxy health and provide recommendations"""
    print("\nPROXY HEALTH CHECK")
    print("="*30)
    
    stats = proxy_rotator.get_proxy_stats()
    
    print(f"Total Proxies: {stats['total_proxies']}")
    print(f"Fresh Proxies Available: {stats['fresh_proxies']}")
    print(f"Unused Proxies: {stats['unused_proxies']}")
    print(f"Total Usage Count: {stats['total_usage']}")
    
    # Calculate usage efficiency
    if stats['total_usage'] > 0:
        avg_usage = stats['total_usage'] / stats['total_proxies']
        print(f"Average Usage per Proxy: {avg_usage:.1f}")
        
        if avg_usage > 10:
            print("⚠️  WARNING: High proxy usage detected")
            print("   Recommendation: Consider reducing thread count")
        elif avg_usage < 2:
            print("✅ Good: Low proxy usage, good distribution")
    
    if stats['fresh_proxies'] < 5:
        print("⚠️  WARNING: Low fresh proxy count")
        print("   Recommendation: Wait for IP rotation or reduce load")
    else:
        print("✅ Good: Sufficient fresh proxies available")

def provide_optimization_tips():
    """Provide optimization recommendations"""
    print("\nOPTIMIZATION RECOMMENDATIONS")
    print("="*35)
    
    print("1. Thread Management:")
    print("   - Use 1-3 threads for better success rate")
    print("   - Higher thread counts may overwhelm proxies")
    
    print("\n2. Proxy Rotation:")
    print("   - System automatically rotates every 15 minutes")
    print("   - Failed proxies are temporarily disabled")
    print("   - Fresh IPs are prioritized")
    
    print("\n3. Error Handling:")
    print("   - Automatic retry with different proxies")
    print("   - JavaScript errors have fallback handling")
    print("   - Connection errors trigger proxy rotation")
    
    print("\n4. Monitoring:")
    print("   - Watch proxy stats during operation")
    print("   - Monitor success vs error ratios")
    print("   - Adjust thread count based on performance")

if __name__ == "__main__":
    print("BINANCE VERIFICATION ERROR ANALYSIS")
    print("=" * 60)
    
    # Analyze common errors
    analyze_common_errors()
    
    # Check proxy health
    check_proxy_health()
    
    # Provide optimization tips
    provide_optimization_tips()
    
    print("\n" + "="*60)
    print("SUMMARY OF IMPROVEMENTS MADE:")
    print("="*60)
    print("✅ Added retry logic (3 attempts per verification)")
    print("✅ Improved proxy error detection and rotation")
    print("✅ Added JavaScript error fallback handling")
    print("✅ Enhanced proxy health monitoring")
    print("✅ Automatic failed proxy reset after 5 minutes")
    print("✅ Better error categorization and logging")
    print("\nThe system should now handle errors more gracefully!")
