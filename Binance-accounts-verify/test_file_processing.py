#!/usr/bin/env python3
"""
Simple test to isolate the function iteration error
"""

# Simulate the error by testing the file reading and processing
import os

def test_file_processing():
    """Test the file processing logic"""
    
    # Test if numbers.txt exists and is readable
    file_path = "待检测/numbers.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
        
        print(f"✅ File read successfully: {len(lines)} lines")
        print(f"First few lines: {lines[:5]}")
        
        # Test the split_list function
        def split_list(lst, group_size):
            return [lst[i:i + group_size] for i in range(0, len(lst), group_size)]
        
        result = split_list(lines, 50000)
        print(f"Split result: {len(result)} groups")
        
        # Test iteration over result
        for i, group in enumerate(result):
            print(f"Group {i}: {len(group)} items")
            if i == 0:  # Only process first group for testing
                acts = []
                acts.clear()
                for row in group:
                    phone = str(row)
                    acts.append(phone)
                print(f"Acts populated with {len(acts)} items")
                print(f"First few acts: {acts[:3]}")
                break
                
    except Exception as e:
        print(f"❌ Error during file processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_file_processing()
