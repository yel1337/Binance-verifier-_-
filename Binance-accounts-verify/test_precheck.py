#!/usr/bin/env python3
"""
Minimal test to isolate the function iteration error
"""

import sys
import os
import importlib.util

# Import only the necessary parts
def test_pre_check():
    """Test pre_check function specifically"""
    
    try:
        # Import the script as a module
        spec = importlib.util.spec_from_file_location("main_script", "Binance-accounts.py")
        main_module = importlib.util.module_from_spec(spec)
        
        # Execute only the imports and function definitions
        with open("Binance-accounts.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the pre_check function definition
        lines = content.split('\n')
        
        # Find where pre_check function starts
        start_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith('def pre_check('):
                start_line = i
                break
        
        if start_line is None:
            print("❌ Could not find pre_check function")
            return
            
        # Extract the function definition
        function_lines = []
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            if i > start_line and line.strip() and (len(line) - len(line.lstrip())) <= indent_level and not line.strip().startswith('#'):
                break
            function_lines.append(line)
        
        function_code = '\n'.join(function_lines)
        print("📄 Pre_check function code:")
        print(function_code[:300] + "...")
        
        # Test if the function is properly structured
        if 'return' in function_code:
            print("✅ Function has return statement")
        else:
            print("❌ Function missing return statement")
            
    except Exception as e:
        print(f"❌ Error testing pre_check: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pre_check()
