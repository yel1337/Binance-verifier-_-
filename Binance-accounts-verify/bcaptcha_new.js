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
  
  return JSON.stringify(result);
}
