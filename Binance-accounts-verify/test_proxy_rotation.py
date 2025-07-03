#!/usr/bin/env python3
"""
Test script for proxy rotation functionality
"""

from proxy_rotator import proxy_rotator
import requests
import time

def test_ip_change():
    """Test if different proxies return different IPs"""
    print("Testing proxy rotation and IP changes...")
    
    used_ips = []
    
    for i in range(5):
        try:
            # Get a fresh proxy
            proxy_dict = proxy_rotator.get_smart_proxy()
            print(f"\nTest {i+1}: Using proxy {proxy_dict['parsed']['username'][:15]}...")
            
            # Test the IP
            response = requests.get('http://httpbin.org/ip', 
                                  proxies=proxy_dict, 
                                  timeout=10)
            
            if response.status_code == 200:
                ip_data = response.json()
                current_ip = ip_data['origin']
                print(f"Current IP: {current_ip}")
                used_ips.append(current_ip)
            else:
                print(f"Failed to get IP: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error testing proxy: {e}")
        
        # Small delay between tests
        time.sleep(2)
    
    # Print results
    print(f"\n=== Test Results ===")
    print(f"Total unique IPs obtained: {len(set(used_ips))}")
    print(f"All IPs: {used_ips}")
    
    # Print proxy stats
    proxy_rotator.print_stats()

def test_rotation_methods():
    """Test different proxy rotation methods"""
    print("\n=== Testing Different Rotation Methods ===")
    
    methods = [
        ("Smart Rotation", proxy_rotator.get_smart_proxy),
        ("Round Robin", proxy_rotator.get_round_robin_proxy),
        ("Random", proxy_rotator.get_random_proxy)
    ]
    
    for method_name, method_func in methods:
        print(f"\n{method_name}:")
        try:
            proxy_dict = method_func()
            print(f"  Proxy: {proxy_dict['parsed']['username'][:20]}...")
            print(f"  Full URL: {proxy_dict['http']}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("Proxy Rotator Test Suite")
    print("=" * 40)
    
    # Test different rotation methods
    test_rotation_methods()
    
    # Test IP changes
    test_ip_change()
