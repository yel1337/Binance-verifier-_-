#!/usr/bin/env python3
"""
Quick debug test for the function iteration error
"""

import sys
import os

# Add the path to find the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Binance-accounts import acts, pre_check, COUNTRIES
    
    print(f"Acts variable: {acts}")
    print(f"Acts type: {type(acts)}")
    print(f"Acts length: {len(acts)}")
    
    if acts:
        print("Calling pre_check with acts...")
        result = pre_check(acts)
        print(f"Pre_check result: {result}")
        print(f"Pre_check result type: {type(result)}")
    else:
        print("Acts is empty, testing with sample data...")
        test_acts = ["441234567890", "11234567890"]
        result = pre_check(test_acts)
        print(f"Pre_check result: {result}")
        print(f"Pre_check result type: {type(result)}")
        
        if result:
            print(f"First account: {result[0]}")
            print(f"Country code lookup: {COUNTRIES.get(result[0][0], 'NOT FOUND')}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
