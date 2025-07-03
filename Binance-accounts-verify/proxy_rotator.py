import time
import random
import threading
from datetime import datetime, timedelta

class ProxyRotator:
    def __init__(self):
        # List of proxy-jet.io proxies
        self.raw_proxies = [
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000",
            "J6DfqQk--:PoUBUB8@103.35.188.169:10000"
        ]
        
        # Track proxy usage with timestamps
        self.proxy_usage = {}
        self.current_proxy_index = 0
        self.rotation_interval = 15 * 60  # 15 minutes in seconds
        self.lock = threading.Lock()
        
        # Initialize proxy usage tracking
        for proxy in self.raw_proxies:
            self.proxy_usage[proxy] = {
                'last_used': None,
                'usage_count': 0,
                'is_available': True
            }
    
    def _parse_proxy(self, proxy_string):
        """Parse proxy string format: username:password@host:port"""
        try:
            # Split by @ to get auth and server parts
            auth_part, server_part = proxy_string.split('@')
            username, password = auth_part.split(':')
            host, port = server_part.split(':')
            
            return {
                'username': username,
                'password': password,
                'host': host,
                'port': port,
                'raw': proxy_string
            }
        except Exception as e:
            print(f"Error parsing proxy {proxy_string}: {e}")
            return None
    
    def _is_proxy_fresh(self, proxy_string):
        """Check if proxy IP should be fresh (15 minutes since last use)"""
        usage_info = self.proxy_usage.get(proxy_string)
        if not usage_info or usage_info['last_used'] is None:
            return True        
        time_since_last_use = datetime.now() - usage_info['last_used']
        return time_since_last_use >= timedelta(seconds=self.rotation_interval)
    
    def get_fresh_proxy(self):
        """Get a proxy that hasn't been used in the last 15 minutes"""
        with self.lock:
            # Reset failed proxies that have been marked as failed for more than 5 minutes
            current_time = datetime.now()
            for proxy in self.raw_proxies:
                usage_info = self.proxy_usage[proxy]
                if not usage_info['is_available'] and usage_info['last_used']:
                    time_since_failure = current_time - usage_info['last_used']
                    if time_since_failure >= timedelta(minutes=5):
                        usage_info['is_available'] = True
                        print(f"Reset proxy status: {proxy[:50]}...")
            
            # Filter available proxies only
            available_proxies = [proxy for proxy in self.raw_proxies 
                               if self.proxy_usage[proxy]['is_available']]
            
            if not available_proxies:
                # If no proxies are available, reset all and use any
                print("No available proxies, resetting all proxy statuses...")
                for proxy in self.raw_proxies:
                    self.proxy_usage[proxy]['is_available'] = True
                available_proxies = self.raw_proxies
            
            # First, try to find a completely unused proxy
            unused_proxies = [proxy for proxy in available_proxies 
                            if self.proxy_usage[proxy]['last_used'] is None]
            
            if unused_proxies:
                selected_proxy = random.choice(unused_proxies)
            else:
                # If all proxies have been used, find the oldest one
                fresh_proxies = [proxy for proxy in available_proxies 
                               if self._is_proxy_fresh(proxy)]
                
                if fresh_proxies:
                    selected_proxy = random.choice(fresh_proxies)
                else:
                    # If no fresh proxies available, use the least recently used
                    selected_proxy = min(available_proxies, 
                                       key=lambda p: self.proxy_usage[p]['last_used'] or datetime.min)
            
            # Update usage tracking
            self.proxy_usage[selected_proxy]['last_used'] = datetime.now()
            self.proxy_usage[selected_proxy]['usage_count'] += 1
            
            return selected_proxy
    
    def get_proxy_dict(self, proxy_string=None):
        """Convert proxy string to requests-compatible proxy dictionary"""
        if proxy_string is None:
            proxy_string = self.get_fresh_proxy()
        
        parsed = self._parse_proxy(proxy_string)
        if not parsed:
            return None
        
        proxy_url = f"http://{parsed['username']}:{parsed['password']}@{parsed['host']}:{parsed['port']}"
        
        return {
            'http': proxy_url,
            'https': proxy_url,
            'raw': proxy_string,
            'parsed': parsed
        }
    
    def get_round_robin_proxy(self):
        """Get proxy using round-robin method"""
        with self.lock:
            proxy_string = self.raw_proxies[self.current_proxy_index]
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.raw_proxies)
            
            # Update usage tracking
            self.proxy_usage[proxy_string]['last_used'] = datetime.now()
            self.proxy_usage[proxy_string]['usage_count'] += 1
            
            return self.get_proxy_dict(proxy_string)
    
    def get_random_proxy(self):
        """Get a random proxy from the pool"""
        proxy_string = random.choice(self.raw_proxies)
        return self.get_proxy_dict(proxy_string)
    
    def get_smart_proxy(self):
        """Get proxy using smart rotation (prefers fresh IPs)"""
        proxy_string = self.get_fresh_proxy()
        return self.get_proxy_dict(proxy_string)
    
    def mark_proxy_failed(self, proxy_string):
        """Mark a proxy as failed (temporarily unavailable)"""
        with self.lock:
            if proxy_string in self.proxy_usage:
                self.proxy_usage[proxy_string]['is_available'] = False
                print(f"Marked proxy as failed: {proxy_string[:50]}...")
    
    def reset_proxy_status(self, proxy_string):
        """Reset proxy status to available"""
        with self.lock:
            if proxy_string in self.proxy_usage:
                self.proxy_usage[proxy_string]['is_available'] = True
    
    def get_proxy_stats(self):
        """Get statistics about proxy usage"""
        with self.lock:
            stats = {
                'total_proxies': len(self.raw_proxies),
                'fresh_proxies': len([p for p in self.raw_proxies if self._is_proxy_fresh(p)]),
                'unused_proxies': len([p for p in self.raw_proxies 
                                     if self.proxy_usage[p]['last_used'] is None]),
                'total_usage': sum(info['usage_count'] for info in self.proxy_usage.values())
            }
            return stats
    
    def print_stats(self):
        """Print current proxy rotation statistics"""
        stats = self.get_proxy_stats()
        print(f"Proxy Stats - Total: {stats['total_proxies']}, "
              f"Fresh: {stats['fresh_proxies']}, "
              f"Unused: {stats['unused_proxies']}, "
              f"Total Usage: {stats['total_usage']}")

# Global proxy rotator instance
proxy_rotator = ProxyRotator()
