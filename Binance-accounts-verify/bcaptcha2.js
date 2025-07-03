// Simple JSON stringify function for JScript compatibility
function stringifyJSON(obj) {
  if (typeof obj === "string") {
    return '"' + obj.replace(/"/g, '\\"') + '"';
  }
  if (typeof obj === "number" || typeof obj === "boolean") {
    return obj.toString();
  }
  if (obj === null) {
    return "null";
  }
  if (typeof obj === "object") {
    var parts = [];
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        parts.push('"' + key + '":' + stringifyJSON(obj[key]));
      }
    }
    return "{" + parts.join(",") + "}";
  }
  return "null";
}

function jt(distance, bizId, data, userAgent, platform, clientInterHeight, clientOuterHeight, slideX, slideY) {
  var timestamp = new Date().getTime();
  var result = {
    bizId: (bizId || "").toString(),
    distance: parseFloat(distance || 0),
    userAgent: (userAgent || "").toString(),
    platform: (platform || "Win32").toString(),
    clientInterHeight: parseFloat(clientInterHeight || 800),
    clientOuterHeight: parseFloat(clientOuterHeight || 900),
    slideX: parseFloat(slideX || 0),
    slideY: parseFloat(slideY || 0),
    timestamp: timestamp,
    version: "1.0.2"
  };
  
  return stringifyJSON(result);
}
