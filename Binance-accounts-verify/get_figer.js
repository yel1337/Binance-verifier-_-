function x64hash128(key, seed) {
  // Simplified fingerprint generator
  return 'fp_' + Math.random().toString(36).substr(2, 16) + '_' + seed;
}