/* THE MATH FINGERPRINT — one source, run in every runtime that runs a fight.

   V8 does not promise bit-exact results for the transcendental functions.
   Math.sin, pow, exp and friends are implemented in ieee754.cc and that file
   changes between Chromium releases. A one-ULP change is enough: the sim
   integrates gravity through `Math.pow` every fighter every step of 4800, and
   `engine_ab`, `verify`, every tuned number and every rebuilt clip rest on
   "(build, relic A, relic B, seed) -> the same fight, ALWAYS".

   That sentence has an unwritten clause and this file is how it gets checked:
   ...always, ON THE SAME V8.

   Called with no arguments, returns { ua, <fn>: "<bit pattern>,..." }.  Bit
   patterns, not decimals — a printed double hides the last bit, which is the
   whole quantity being measured here.  */
() => {
  const bits = x => {
    const b = new DataView(new ArrayBuffer(8));
    b.setFloat64(0, x);
    return b.getUint32(0).toString(16).padStart(8, '0') +
           b.getUint32(4).toString(16).padStart(8, '0');
  };
  /* The unary set. Domains are kept legal on purpose: an out-of-domain call
     returns NaN, and NaN PAYLOADS differ between builds without any real
     arithmetic differing, which would report a false positive forever. */
  const un = {
    sin:   i => i * 0.37 + 0.13,
    cos:   i => i * 0.37 + 0.13,
    tan:   i => i * 0.37 + 0.13,
    asin:  i => i * 0.09 - 0.45,
    acos:  i => i * 0.09 - 0.45,
    atan:  i => i * 0.37 + 0.13,
    exp:   i => i * 0.37 + 0.13,
    log:   i => i * 0.37 + 0.13,
    sqrt:  i => i * 0.37 + 0.13,
    cbrt:  i => i * 0.37 + 0.13,
    sinh:  i => i * 0.37 + 0.13,
    cosh:  i => i * 0.37 + 0.13,
    tanh:  i => i * 0.37 + 0.13,
    expm1: i => i * 0.37 + 0.13,
    log1p: i => i * 0.37 + 0.13,
    log2:  i => i * 0.37 + 0.13,
    log10: i => i * 0.37 + 0.13,
  };
  const out = { ua: navigator.userAgent };
  for (const n in un) {
    const s = [];
    for (let i = 1; i <= 12; i++) s.push(bits(Math[n](un[n](i))));
    out[n] = s.join(',');
  }
  const bin = {
    atan2: i => Math.atan2(i * 0.37 + 0.13, 1.9 - i * 0.11),
    pow:   i => Math.pow(1.3 + i * 0.07, 0.5 + i * 0.13),
    hypot: i => Math.hypot(i * 0.37 + 0.13, 1.9 - i * 0.11),
  };
  for (const n in bin) {
    const s = [];
    for (let i = 1; i <= 12; i++) s.push(bits(bin[n](i)));
    out[n] = s.join(',');
  }
  return out;
}
