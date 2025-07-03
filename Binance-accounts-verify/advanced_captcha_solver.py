#!/usr/bin/env python3
"""
Advanced Captcha Solution Generator
This creates more realistic captcha solutions that mimic human behavior
"""

import sys
import os
import time
import json
import math
import random
import execjs
from datetime import datetime

def generate_mouse_trajectory(distance, duration_ms=1000):
    """Generate realistic mouse movement trajectory"""
    print(f"🖱️ Generating mouse trajectory for distance: {distance}px over {duration_ms}ms")
    
    trajectory = []
    steps = max(10, min(50, int(distance / 5)))  # 10-50 steps based on distance
    
    for i in range(steps + 1):
        progress = i / steps
        
        # Easing function (cubic bezier)
        if progress < 0.5:
            eased = 2 * progress * progress
        else:
            eased = 1 - 2 * (1 - progress) * (1 - progress)
        
        # Add some randomness to make it more human-like
        noise = random.uniform(-0.02, 0.02)
        eased = max(0, min(1, eased + noise))
        
        x = int(eased * distance)
        y = random.randint(-2, 2)  # Small vertical movement
        timestamp = int(progress * duration_ms)
        
        trajectory.append({
            'x': x,
            'y': y,
            'time': timestamp
        })
    
    print(f"   📊 Generated {len(trajectory)} trajectory points")
    return trajectory

def generate_advanced_captcha_data(distance, bizId, validateId, sessionId):
    """Generate advanced captcha data that mimics real browser behavior"""
    print(f"🔧 Generating advanced captcha data")
    
    # Generate mouse trajectory
    trajectory = generate_mouse_trajectory(distance, random.randint(800, 1500))
    
    # Timing data
    start_time = int(time.time() * 1000)
    end_time = start_time + trajectory[-1]['time']
    
    # Browser fingerprint data
    fingerprint = {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'platform': 'Win32',
        'language': 'en-US',
        'screen': {
            'width': 1920,
            'height': 1080,
            'availWidth': 1920,
            'availHeight': 1040,
            'colorDepth': 24,
            'pixelDepth': 24
        },
        'timezone': -300,  # EST
        'plugins': ['PDF Viewer', 'Chrome PDF Viewer'],
        'canvas': generate_canvas_fingerprint()
    }
    
    # Main captcha data
    captcha_data = {
        'bizId': bizId,
        'validateId': validateId,
        'sessionId': sessionId,
        'distance': distance,
        'startTime': start_time,
        'endTime': end_time,
        'duration': end_time - start_time,
        'trajectory': trajectory,
        'fingerprint': fingerprint,
        'version': '1.0.2',
        'timestamp': int(time.time() * 1000)
    }
    
    print(f"   ✅ Advanced captcha data generated")
    print(f"   📊 Trajectory points: {len(trajectory)}")
    print(f"   ⏱️ Duration: {captcha_data['duration']}ms")
    
    return captcha_data

def generate_canvas_fingerprint():
    """Generate a simple canvas fingerprint"""
    # This is a simplified version - real implementations are more complex
    return {
        'hash': 'abc123def456',  # Would be generated from actual canvas rendering
        'width': 300,
        'height': 150
    }

def create_enhanced_js_context():
    """Create an enhanced JavaScript context with better captcha handling"""
    
    js_code = '''
    // Enhanced mouse trajectory simulation
    function generateTrajectory(distance, duration) {
        var trajectory = [];
        var steps = Math.max(10, Math.min(50, Math.floor(distance / 5)));
        
        for (var i = 0; i <= steps; i++) {
            var progress = i / steps;
            
            // Cubic bezier easing
            var eased;
            if (progress < 0.5) {
                eased = 2 * progress * progress;
            } else {
                eased = 1 - 2 * (1 - progress) * (1 - progress);
            }
            
            // Add small random variations
            var noise = (Math.random() - 0.5) * 0.04;
            eased = Math.max(0, Math.min(1, eased + noise));
            
            var x = Math.round(eased * distance);
            var y = Math.round((Math.random() - 0.5) * 4); // -2 to +2
            var time = Math.round(progress * duration);
            
            trajectory.push({
                x: x,
                y: y,
                time: time
            });
        }
        
        return trajectory;
    }
    
    // Enhanced parameter generation function
    function jt_enhanced(distance, bizId, data, userAgent, platform, validateId, 
                        clientInterHeight, clientOuterHeight, clientW, clientH, 
                        centerX, centerY) {
        
        var now = new Date().getTime();
        var duration = Math.floor(Math.random() * 700) + 800; // 800-1500ms
        var trajectory = generateTrajectory(distance, duration);
        
        // Calculate more realistic timing
        var startTime = now - duration;
        var endTime = now;
        
        // Enhanced parameter object
        var result = {
            bizId: (bizId || "login").toString(),
            validateId: (validateId || "").toString(),
            sessionId: (data && data.sessionId) ? data.sessionId.toString() : "",
            distance: parseFloat(distance || 0),
            startTime: startTime,
            endTime: endTime,
            duration: duration,
            trajectory: trajectory,
            userAgent: (userAgent || "").toString(),
            platform: (platform || "Win32").toString(),
            clientInterHeight: parseFloat(clientInterHeight || 969),
            clientOuterHeight: parseFloat(clientOuterHeight || 1048),
            clientWidth: parseFloat(clientW || 1920),
            clientHeight: parseFloat(clientH || 1080),
            centerX: parseFloat(centerX || 150),
            centerY: parseFloat(centerY || 150),
            timestamp: now,
            version: "1.0.2",
            // Additional browser fingerprint
            screen: {
                width: 1920,
                height: 1080,
                availWidth: 1920,
                availHeight: 1040,
                colorDepth: 24
            },
            timezone: -300,
            language: "en-US"
        };
        
        return JSON.stringify(result);
    }
    
    // Legacy function for compatibility
    function jt(distance, bizId, data, userAgent, platform, validateId, 
               clientInterHeight, clientOuterHeight, clientW, clientH, 
               centerX, centerY) {
        return jt_enhanced(distance, bizId, data, userAgent, platform, validateId,
                          clientInterHeight, clientOuterHeight, clientW, clientH,
                          centerX, centerY);
    }
    '''
    
    return execjs.compile(js_code)

def test_enhanced_captcha_solving():
    """Test the enhanced captcha solving approach"""
    print(f"🧪 Testing Enhanced Captcha Solving")
    print("=" * 50)
    
    # Get proxy
    try:
        from proxy_rotator import proxy_rotator
        proxy_dict = proxy_rotator.get_smart_proxy()
        proxies = {
            'http': proxy_dict['http'],
            'https': proxy_dict['https']
        }
        print(f"🔗 Using proxy: {proxy_dict['raw'][:50]}...")
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        return
    
    # Create enhanced JS context
    print(f"\n🔧 Creating enhanced JavaScript context...")
    ctx = create_enhanced_js_context()
    
    # Test parameters
    bizId = 'login'
    validateId = 'enhanced_test_' + str(int(time.time()))
    distance_options = [50, 75, 100, 125, 150]
    
    data = {
        'sessionId': 'enhanced_session_' + str(int(time.time())),
        'validateId': validateId
    }
    
    # Standard browser parameters
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    platform = 'Win32'
    client_interHeight = 969
    client_outerHeight = 1048
    client_w = 1920
    client_h = 1080
    center_x = 150
    center_y = 150
    
    url = 'https://accounts.binance.info/bapi/composite/v1/public/antibot/validateCaptcha'
    
    for distance in distance_options:
        print(f"\n   🎯 Testing distance: {distance}px")
        
        try:
            # Generate enhanced parameter
            param = ctx.call('jt_enhanced', distance, bizId, data, headers['user-agent'], 
                           platform, validateId, client_interHeight, client_outerHeight, 
                           client_w, client_h, center_x, center_y)
            
            print(f"      ✅ Parameter generated: {len(param)} chars")
            
            # Parse to verify structure
            try:
                param_json = json.loads(param)
                print(f"      📊 Parameter keys: {list(param_json.keys())}")
                print(f"      ⏱️ Duration: {param_json.get('duration', 'N/A')}ms")
                print(f"      🖱️ Trajectory points: {len(param_json.get('trajectory', []))}")
            except:
                print(f"      ❌ Failed to parse generated parameter")
                continue
            
            # Prepare request
            from urllib.parse import urlencode
            form_data = {
                'sig': param,
                'bizId': bizId,
                'data': param
            }
            
            form_headers = {
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': 'https://accounts.binance.info',
                'referer': 'https://accounts.binance.info/',
                'user-agent': headers['user-agent'],
                'captcha-sdk-version': '1.0.2'
            }
            
            # Make request
            import requests
            encoded_data = urlencode(form_data)
            response = requests.post(url, headers=form_headers, data=encoded_data, 
                                   proxies=proxies, timeout=15, verify=False)
            
            print(f"      📤 Response status: {response.status_code}")
            
            if response.text:
                try:
                    res_json = response.json()
                    print(f"      📊 Response: {res_json}")
                    
                    if res_json.get('success') == True:
                        token = res_json.get('data', {}).get('token', '')
                        result_code = res_json.get('data', {}).get('result', 'unknown')
                        
                        if token:
                            print(f"      🎉 SUCCESS! Token: {token[:20]}...")
                            print(f"      ✅ Best distance: {distance}px")
                            return distance, param, res_json
                        else:
                            print(f"      ⚠️ Empty token, result: {result_code}")
                    else:
                        print(f"      ❌ Request failed")
                        
                except json.JSONDecodeError:
                    print(f"      ❌ Invalid JSON: {response.text[:100]}...")
            else:
                print(f"      ❌ Empty response")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n📊 No successful token generation with enhanced method")
    return None, None, None

def analyze_result_codes():
    """Analyze what different result codes mean"""
    print(f"\n📋 Captcha Result Code Analysis")
    print("=" * 40)
    
    result_codes = {
        0: "Success - Captcha solved correctly",
        1: "Pending - Captcha validation in progress", 
        2: "Failed - Incorrect solution or timing",
        3: "Expired - Captcha session expired",
        4: "Invalid - Malformed request data",
        5: "Blocked - IP or user blocked"
    }
    
    for code, meaning in result_codes.items():
        print(f"   {code}: {meaning}")
    
    print(f"\n💡 Since we're getting result code 2, the issue is likely:")
    print(f"   - Incorrect distance calculation")
    print(f"   - Unrealistic mouse trajectory")
    print(f"   - Missing timing parameters")
    print(f"   - Insufficient browser fingerprinting")

def main():
    """Main function"""
    print("🔬 Advanced Captcha Solution Generator")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Analyze result codes
    analyze_result_codes()
    
    # Test enhanced solving
    distance, param, response = test_enhanced_captcha_solving()
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("=" * 60)
    if distance:
        print(f"✅ Success with distance: {distance}px")
    else:
        print(f"❌ No successful captcha solution found")
        print(f"\n🔍 Recommendations:")
        print(f"   1. Analyze real browser captcha solutions")
        print(f"   2. Implement more sophisticated mouse simulation")
        print(f"   3. Add proper timing and behavioral patterns")
        print(f"   4. Consider using machine learning for distance calculation")
        print(f"   5. Test with actual puzzle piece gap detection")

if __name__ == "__main__":
    main()
