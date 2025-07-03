// Enhanced JScript-compatible captcha solver
// This version includes realistic mouse trajectory simulation

// JSON stringify function for JScript compatibility
function stringifyJSON(obj) {
  if (typeof obj === "string") {
    return '"' + obj.replace(/"/g, '\\"').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t') + '"';
  }
  if (typeof obj === "number") {
    return obj.toString();
  }
  if (typeof obj === "boolean") {
    return obj.toString();
  }
  if (obj === null || obj === undefined) {
    return "null";
  }
  if (typeof obj === "object") {
    if (obj.constructor === Array) {
      var parts = [];
      for (var i = 0; i < obj.length; i++) {
        parts.push(stringifyJSON(obj[i]));
      }
      return "[" + parts.join(",") + "]";
    } else {
      var parts = [];
      for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
          parts.push('"' + key + '":' + stringifyJSON(obj[key]));
        }
      }
      return "{" + parts.join(",") + "}";
    }
  }
  return "null";
}

// Enhanced mouse trajectory generation
function generateTrajectory(distance, duration) {
    var trajectory = [];
    var steps = Math.max(15, Math.min(50, Math.floor(distance / 3)));
    
    for (var i = 0; i <= steps; i++) {
        var progress = i / steps;
        
        // Cubic bezier easing with more realistic curve
        var eased;
        if (progress < 0.25) {
            // Slow start
            eased = 2 * progress * progress;
        } else if (progress < 0.75) {
            // Fast middle
            eased = progress;
        } else {
            // Slow end with slight overshoot correction
            var t = (progress - 0.75) / 0.25;
            eased = 0.75 + 0.25 * (1 - (1 - t) * (1 - t));
        }
        
        // Add human-like random variations
        var noise = (Math.random() - 0.5) * 0.03;
        eased = Math.max(0, Math.min(1, eased + noise));
        
        var x = Math.round(eased * distance);
        var y = Math.round((Math.random() - 0.5) * 6); // -3 to +3 vertical drift
        var time = Math.round(progress * duration);
        
        // Add small pauses at beginning and end
        if (i === 0) time = 0;
        if (i === 1) time = Math.round(duration * 0.05); // 5% delay start
        if (i === steps) time = duration;
        
        trajectory.push({
            x: x,
            y: y,
            time: time
        });
    }
    
    return trajectory;
}

// Calculate more accurate distance based on puzzle piece position
function calculatePuzzleDistance(puzzleX, backgroundWidth) {
    // More sophisticated calculation
    var gapX = backgroundWidth - puzzleX;
    
    // Add small random adjustment to mimic human imprecision
    var humanError = (Math.random() - 0.5) * 8; // -4 to +4 pixels
    var adjustedDistance = gapX + humanError;
    
    // Ensure distance is reasonable
    return Math.max(10, Math.min(backgroundWidth - 20, adjustedDistance));
}

// Enhanced parameter generation
function jt_enhanced(distance, bizId, data, userAgent, platform, validateId, 
                    clientInterHeight, clientOuterHeight, clientW, clientH, 
                    centerX, centerY) {
    
    var now = new Date().getTime();
    
    // More realistic timing - humans take 1-3 seconds
    var baseDuration = Math.max(800, Math.min(3000, distance * 12 + Math.random() * 500));
    var duration = Math.round(baseDuration);
    
    // Calculate adjusted distance with human-like error
    var adjustedDistance = calculatePuzzleDistance(distance, 340); // Assume 340px background width
    
    // Generate realistic trajectory
    var trajectory = generateTrajectory(adjustedDistance, duration);
    
    // Calculate timing
    var startTime = now - duration - Math.round(Math.random() * 100); // Small random offset
    var endTime = startTime + duration;
    
    // Extract session info
    var sessionId = "";
    var actualValidateId = validateId || "";
    if (data && typeof data === "object") {
        if (data.sessionId) sessionId = data.sessionId.toString();
        if (data.validateId) actualValidateId = data.validateId.toString();
    }
    
    // Enhanced parameter object with more browser-like data
    var result = {
        bizId: (bizId || "login").toString(),
        validateId: actualValidateId,
        sessionId: sessionId,
        distance: parseFloat(adjustedDistance),
        startTime: startTime,
        endTime: endTime,
        duration: duration,
        trajectory: trajectory,
        userAgent: (userAgent || "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36").toString(),
        platform: (platform || "Win32").toString(),
        clientInterHeight: parseFloat(clientInterHeight || 969),
        clientOuterHeight: parseFloat(clientOuterHeight || 1048),
        clientWidth: parseFloat(clientW || 1920),
        clientHeight: parseFloat(clientH || 1080),
        centerX: parseFloat(centerX || 150),
        centerY: parseFloat(centerY || 150),
        timestamp: now,
        version: "1.0.2",
        // Additional browser fingerprint data
        screen: {
            width: parseFloat(clientW || 1920),
            height: parseFloat(clientH || 1080),
            availWidth: parseFloat(clientW || 1920),
            availHeight: parseFloat(clientH || 1080) - 40, // Minus taskbar
            colorDepth: 24,
            pixelDepth: 24
        },
        timezone: -300, // EST
        language: "en-US",
        hardwareConcurrency: 8,
        deviceMemory: 8,// Enhanced mouse behavior characteristics
        mouseBehavior: {
            acceleration: Math.round(adjustedDistance / duration * 1000 * 100) / 100,
            maxSpeed: calculateMaxSpeed(trajectory),
            steadiness: calculateSteadiness(trajectory)
        }
    };
    
    return stringifyJSON(result);
}

// Helper functions for JScript compatibility
function calculateMaxSpeed(trajectory) {
    var maxSpeed = 0;
    for (var i = 1; i < trajectory.length; i++) {
        var prevP = trajectory[i-1];
        var currP = trajectory[i];
        var deltaX = currP.x - prevP.x;
        var deltaT = currP.time - prevP.time;
        if (deltaT > 0) {
            var speed = Math.abs(deltaX / deltaT) * 1000;
            if (speed > maxSpeed) {
                maxSpeed = speed;
            }
        }
    }
    return Math.round(maxSpeed * 100) / 100;
}

function calculateSteadiness(trajectory) {
    var totalY = 0;
    for (var i = 0; i < trajectory.length; i++) {
        totalY += trajectory[i].y;
    }
    var avgY = totalY / trajectory.length;
    var steadiness = 1 - Math.abs(avgY / 10);
    return Math.round(steadiness * 100) / 100;
}

// Legacy compatibility function
function jt(distance, bizId, data, userAgent, platform, validateId, 
           clientInterHeight, clientOuterHeight, clientW, clientH, 
           centerX, centerY) {
    return jt_enhanced(distance, bizId, data, userAgent, platform, validateId,
                      clientInterHeight, clientOuterHeight, clientW, clientH,
                      centerX, centerY);
}
