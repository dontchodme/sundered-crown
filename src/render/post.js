/* THE POST CHAIN — composite the finished 2D frame through WebGL2.
 *
 * `docs/RENDERER-BRIEF.md` §5. This file is NOT app-only code and must never
 * become app-only code: if the app has bloom and the mp4 does not, that is a
 * picture fault by construction, and it breaks the one guarantee Electron was
 * chosen for. The app loads it through app/ui/post-dev.js; later
 * tools/post_build.py inserts this same text into the chain so cinema_clip.py
 * renders through it too.
 *
 * So: NO engine imports, no `document` outside what is handed in, no reference
 * to anything in the shell. Source canvas plus a state object goes in,
 * composited pixels come out.
 *
 * THE CONTROL IS THE OLD PIXELS. `state.enabled === false` does not render a
 * neutral pass — it renders nothing at all, and the caller shows the original
 * canvas. A control that goes through the same code it is controlling for is
 * not a control.
 *
 * AND WITH NO PASSES REGISTERED THE CHAIN IS INVISIBLE. Not approximately:
 * `selfTest()` compares every channel of every pixel against the 2D canvas it
 * was handed and must report zero. tools/post_identity.py and `npm run post`
 * both assert it. Every effect below is measured against that.
 */
(function (root) {
  'use strict';

  var VERSION = '0.2.0-bloom';

  /* A fullscreen triangle, not a quad: no seam down the diagonal, one fewer
     vertex, and the clip-space maths is the same. */
  var VERT = [
    '#version 300 es',
    'out vec2 vUv;',
    'void main(){',
    '  vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);',
    '  vUv = p;',
    '  gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);',
    '}'
  ].join('\n');

  /* Sampling is NEAREST at 1:1, so this is a copy and must stay one. Any
     arithmetic here — a multiply by 1.0, a clamp, a pow(x, 1.0) — risks
     coming back off by a bit on some driver, and then the identity check
     that guards every effect is already red for a reason nobody remembers. */
  var FRAG_COPY = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    /* The 2D canvas has row 0 at the top; GL reads v upward. Flipped here,
       once, rather than in every pass that follows. */
    '  oCol = texture(uSrc, vec2(vUv.x, 1.0 - vUv.y));',
    '}'
  ].join('\n');

  var FRAG_COPY_NOFLIP = FRAG_COPY.replace('vec2(vUv.x, 1.0 - vUv.y)', 'vUv');

  /* ---------------------------------------------------------- BLOOM ---
     Bright-pass, a downsample pyramid, then a tent upsample back up,
     accumulating. Dual-filter rather than a separable gaussian: five levels
     of bilinear taps reach further for less bandwidth, and reach is what
     makes a bloom read as light rather than as a blurred copy of the art.

     THE THRESHOLD IS THE WHOLE ARGUMENT. The art is already additive in
     twenty-odd places (`globalCompositeOperation = "lighter"` — see
     docs/RENDER-LAYERS.md §3), so the bright parts of this picture are
     genuinely bright and a threshold near white picks out exactly the ult
     art, the weapon glow and the brink pulse. Drop it too low and the relic
     bodies and the hall floor start glowing, which reads as fog. */

  /* Rec. 709 luma, with a soft knee so a pixel does not pop into the bloom
     the instant it crosses the line — a hard threshold crawls visibly along
     a moving edge. */
  var FRAG_BRIGHT = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'uniform vec2 uTexel;',      // texel of the SOURCE
    'uniform vec4 uRect;',       // arena rect, normalised xy wh; w<=0 = whole frame
    'uniform float uThresh;',
    'uniform float uKnee;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    /* NO FLIP HERE, AND THIS COST A SHEET. This pass is handed the target the
       initial copy already flipped into GL orientation, so flipping again
       samples a vertically MIRRORED frame — and because the rect was masked
       in the same mirrored space, the mask let the HUD through and dropped it
       near the arena floor as an upside-down ghost of "78% 100%".
       ONE PLACE KNOWS ABOUT THE FLIP: the copy on the way in. Everything
       after it, including uRect, is GL-oriented. */
    '  vec2 uv = vUv;',
    /* Four bilinear taps: a free box downsample on the way in. */
    '  vec3 c = texture(uSrc, uv + vec2(-1.0, -1.0) * uTexel).rgb;',
    '  c += texture(uSrc, uv + vec2( 1.0, -1.0) * uTexel).rgb;',
    '  c += texture(uSrc, uv + vec2(-1.0,  1.0) * uTexel).rgb;',
    '  c += texture(uSrc, uv + vec2( 1.0,  1.0) * uTexel).rgb;',
    '  c *= 0.25;',
    /* OUTSIDE THE ARENA RECT NOTHING IS EMISSIVE. docs/RENDER-LAYERS.md §3:
       every `lighter` layer in the frame is inside this rect and the HUD sits
       entirely above it, so masking here leaves the readout alone by geometry
       rather than by hoping the threshold spares it. */
    '  if (uRect.z > 0.0) {',
    '    vec2 p = uv;',
    '    if (p.x < uRect.x || p.y < uRect.y ||',
    '        p.x > uRect.x + uRect.z || p.y > uRect.y + uRect.w) {',
    '      oCol = vec4(0.0); return;',
    '    }',
    '  }',
    '  float l = dot(c, vec3(0.2126, 0.7152, 0.0722));',
    '  float w = smoothstep(uThresh, uThresh + max(uKnee, 1e-4), l);',
    '  oCol = vec4(c * w, 1.0);',
    '}'
  ].join('\n');

  var FRAG_DOWN = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'uniform vec2 uTexel;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    '  vec3 c = texture(uSrc, vUv + vec2(-1.0, -1.0) * uTexel).rgb;',
    '  c += texture(uSrc, vUv + vec2( 1.0, -1.0) * uTexel).rgb;',
    '  c += texture(uSrc, vUv + vec2(-1.0,  1.0) * uTexel).rgb;',
    '  c += texture(uSrc, vUv + vec2( 1.0,  1.0) * uTexel).rgb;',
    '  oCol = vec4(c * 0.25, 1.0);',
    '}'
  ].join('\n');

  /* 3x3 tent on the way back up. Blended additively onto the level below, so
     each level contributes its own reach. */
  var FRAG_UP = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'uniform vec2 uTexel;',
    'uniform float uScatter;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    '  vec2 d = uTexel * uScatter;',
    '  vec3 c = texture(uSrc, vUv + vec2(-d.x,  d.y)).rgb;',
    '  c += texture(uSrc, vUv + vec2( 0.0,  d.y)).rgb * 2.0;',
    '  c += texture(uSrc, vUv + vec2( d.x,  d.y)).rgb;',
    '  c += texture(uSrc, vUv + vec2(-d.x,  0.0)).rgb * 2.0;',
    '  c += texture(uSrc, vUv).rgb * 4.0;',
    '  c += texture(uSrc, vUv + vec2( d.x,  0.0)).rgb * 2.0;',
    '  c += texture(uSrc, vUv + vec2(-d.x, -d.y)).rgb;',
    '  c += texture(uSrc, vUv + vec2( 0.0, -d.y)).rgb * 2.0;',
    '  c += texture(uSrc, vUv + vec2( d.x, -d.y)).rgb;',
    '  oCol = vec4(c * (1.0 / 16.0), 1.0);',
    '}'
  ].join('\n');

  /* --------------------------------------------------------- TRAILS ---
     A persistence buffer, and the operator is a MAX rather than a sum:

         trail = max(bright, trail_prev * decay)

     A summing accumulator runs away. Stationary bright art converges to
     bright/(1-decay), so the hex grid and a resting relic would climb frame
     after frame into a bloom that has nothing to do with motion. Under a max
     the trail can never exceed the source that fed it: something that does
     not move sits at its own brightness and is invisible, and something that
     does leaves a decaying smear behind it. That is the whole effect.

     It runs on the THRESHOLDED image, not on the frame. Smearing everything
     would ghost the arena floor and the hall grid into a permanent haze —
     which is fog, not speed. */
  var FRAG_TRAIL = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',      // this frame's bright pass
    'uniform sampler2D uPrev;',     // the trail so far
    'uniform float uDecay;',
    'uniform vec2 uSpread;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    '  vec3 cur = texture(uSrc, vUv).rgb;',
    /* A TENT ON THE WAY BACK, AND NOT A DILATION. Without any spreading the
       trail is a string of beads: at 60fps a flail head travels much further
       between frames than its own width, so a plain max() of two positions
       leaves two separate blobs and every frame adds another one.

       The first attempt at closing that gap took the MAX of the neighbours,
       which is a box dilation -- and a box dilation grows a square. Over the
       dozen frames of a 0.12s tail it turned every trail into a grey
       rectangle, which was worse than the beading and obviously wrong in one
       glance at the sheet.

       A 3x3 tent conserves energy instead of taking the brightest neighbour,
       so the beads bleed into each other and the whole thing dims as it
       spreads. It softens; it does not grow. */
    '  vec3 old = texture(uPrev, vUv + vec2(-uSpread.x,  uSpread.y)).rgb;',
    '  old += texture(uPrev, vUv + vec2( 0.0,  uSpread.y)).rgb * 2.0;',
    '  old += texture(uPrev, vUv + vec2( uSpread.x,  uSpread.y)).rgb;',
    '  old += texture(uPrev, vUv + vec2(-uSpread.x,  0.0)).rgb * 2.0;',
    '  old += texture(uPrev, vUv).rgb * 4.0;',
    '  old += texture(uPrev, vUv + vec2( uSpread.x,  0.0)).rgb * 2.0;',
    '  old += texture(uPrev, vUv + vec2(-uSpread.x, -uSpread.y)).rgb;',
    '  old += texture(uPrev, vUv + vec2( 0.0, -uSpread.y)).rgb * 2.0;',
    '  old += texture(uPrev, vUv + vec2( uSpread.x, -uSpread.y)).rgb;',
    '  old *= (1.0 / 16.0);',
    '  oCol = vec4(max(cur, old * uDecay), 1.0);',
    '}'
  ].join('\n');

  var FRAG_COMBINE = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'uniform sampler2D uBloom;',
    'uniform float uIntensity;',
    'uniform vec4 uRect;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'void main(){',
    '  vec3 base = texture(uSrc, vUv).rgb;',
    /* MASKED HERE TOO, AND THIS IS THE HALF THAT IS EASY TO MISS. Masking the
       bright pass stops the HUD CONTRIBUTING light; it does not stop light
       from inside the arena being BLURRED OUT past the rect and landing on
       the chrome. The first sheet showed exactly that — a bright bar under
       the hall where the tug plate and the footer had been lit by the fight
       above them. Both ends have to be masked or the readout glows. */
    '  vec2 p = vUv;',
    '  if (uRect.z > 0.0 && (p.x < uRect.x || p.y < uRect.y ||',
    '      p.x > uRect.x + uRect.z || p.y > uRect.y + uRect.w)) {',
    '    oCol = vec4(base, 1.0); return;',
    '  }',
    '  vec3 b = texture(uBloom, vUv).rgb;',
    /* Added, not screened. The art underneath is already doing additive
       compositing in Canvas 2D; screening on top of it desaturates the
       gold, which is the one colour this game cannot afford to lose. */
    '  oCol = vec4(base + b * uIntensity, 1.0);',
    '}'
  ].join('\n');

  /* ---------------------------------------------------------- GRADE ---
     Vignette, grain and a small contrast curve, in one pass, at the end.
     Brief §5: "filmic grade + tonemap: one place, instead of per-draw colour
     choices".

     THE VIGNETTE YIELDS TO THE DIRECTOR. `CINE.wash` is already a darkening
     scrim centred on the point of contact, and it exists because a full-frame
     scrim at 0.75 measured INVISIBLE against an already-dark arena -- the
     frame is not the subject, the blow is. A lens vignette is a different
     job: frame-centred, always on, keeping the eye in. They only collide
     during a cut, near the focus, where both darken the same pixels.

     So the vignette scales by (1 - yield * cutK) and backs off exactly as far
     as the scrim comes in. Nobody has to choose which one fires. Priced
     rather than asserted: tools/post_grade_probe.py measures the mid-tone
     drop with each alone and both together, and if the stack turns out to be
     negligible the yield can go to 0 and this comment becomes the reason why.

     GRAIN IS KEYED TO THE FRAME INDEX, NOT A CLOCK. A wall-clock seed would
     make the same seed grain differently in the app and in the mp4, and grain
     that differs between two renders of one fight is the determinism problem
     wearing a different hat. */
  var FRAG_GRADE = [
    '#version 300 es',
    'precision highp float;',
    'uniform sampler2D uSrc;',
    'uniform vec4 uRect;',
    'uniform vec2 uSize;',
    'uniform float uVig;',      // strength, already yielded
    'uniform float uVigR;',     // where the falloff starts, 0..1 of the radius
    'uniform float uGrain;',
    'uniform float uFrame;',
    'uniform float uContrast;',
    'uniform float uLift;',
    'in vec2 vUv;',
    'out vec4 oCol;',
    'float hash(vec3 p){',
    '  p = fract(p * vec3(443.897, 441.423, 437.195));',
    '  p += dot(p, p.yzx + 19.19);',
    '  return fract((p.x + p.y) * p.z);',
    '}',
    'void main(){',
    '  vec3 c = texture(uSrc, vUv).rgb;',
    '  if (uRect.z > 0.0 && (vUv.x < uRect.x || vUv.y < uRect.y ||',
    '      vUv.x > uRect.x + uRect.z || vUv.y > uRect.y + uRect.w)) {',
    '    oCol = vec4(c, 1.0); return;',
    '  }',
    /* Contrast about the mid, then the lift, then the vignette, then grain.
       Order matters: grain added before the vignette would be darkened along
       with everything else at the edges, and film grain does not fade out
       towards the corners. */
    '  c = (c - 0.5) * uContrast + 0.5 + uLift;',
    '  if (uVig > 0.0) {',
    /* Normalised to the RECT, not the frame, so the falloff is centred on the
       hall and not on a point somewhere under the HUD. */
    '    vec2 q = (vUv - uRect.xy) / uRect.zw - 0.5;',
    '    q.x *= uRect.z * uSize.x / (uRect.w * uSize.y);',
    '    float d = length(q) * 1.41421356;',
    '    float v = 1.0 - uVig * smoothstep(uVigR, 1.0, d);',
    '    c *= v;',
    '  }',
    '  if (uGrain > 0.0) {',
    '    float n = hash(vec3(gl_FragCoord.xy, uFrame)) - 0.5;',
    /* Scaled by luma so the grain sits in the mids and does not speckle the
       blacks, which is where it reads as compression noise instead of film. */
    '    float l = dot(c, vec3(0.2126, 0.7152, 0.0722));',
    '    c += n * uGrain * (0.35 + 0.65 * smoothstep(0.02, 0.5, l));',
    '  }',
    '  oCol = vec4(clamp(c, 0.0, 1.0), 1.0);',
    '}'
  ].join('\n');

  function compile(gl, type, src, name) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      var log = gl.getShaderInfoLog(s);
      gl.deleteShader(s);
      throw new Error('post: ' + name + ' failed to compile\n' + log);
    }
    return s;
  }

  function program(gl, frag, name) {
    var v = compile(gl, gl.VERTEX_SHADER, VERT, name + '.vert');
    var f = compile(gl, gl.FRAGMENT_SHADER, frag, name + '.frag');
    var p = gl.createProgram();
    gl.attachShader(p, v);
    gl.attachShader(p, f);
    gl.linkProgram(p);
    gl.deleteShader(v);
    gl.deleteShader(f);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      var log = gl.getProgramInfoLog(p);
      gl.deleteProgram(p);
      throw new Error('post: ' + name + ' failed to link\n' + log);
    }
    return p;
  }

  /* NEAREST and CLAMP_TO_EDGE by default, on purpose: at 1:1 they make a copy
     exact. The bloom pyramid asks for LINEAR explicitly, because there the
     filtering IS the blur. */
  function makeTarget(gl, w, h, linear) {
    var f = linear ? gl.LINEAR : gl.NEAREST;
    var tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA,
                  gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, f);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, f);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    var fbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0,
                            gl.TEXTURE_2D, tex, 0);
    var ok = gl.checkFramebufferStatus(gl.FRAMEBUFFER) === gl.FRAMEBUFFER_COMPLETE;
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    if (!ok) throw new Error('post: framebuffer incomplete at ' + w + 'x' + h);
    return { tex: tex, fbo: fbo, w: w, h: h };
  }

  function freeTarget(gl, t) {
    if (!t) return;
    gl.deleteTexture(t.tex);
    gl.deleteFramebuffer(t.fbo);
  }

  /* ------------------------------------------------------------------ */

  function Post(canvas) {
    /* premultipliedAlpha:false and alpha:false together are what keep a
       passthrough exact. With alpha:true the compositor multiplies the
       drawing buffer by its own alpha on the way to the screen and the
       identity check comes back off by a bit in the darks — which reads as a
       shader bug and is not one. */
    var gl = canvas.getContext('webgl2', {
      alpha: false,
      depth: false,
      stencil: false,
      antialias: false,
      premultipliedAlpha: false,
      preserveDrawingBuffer: true,
      powerPreference: 'high-performance'
    });
    if (!gl) throw new Error('post: no WebGL2 context');

    this.canvas = canvas;
    this.gl = gl;
    this.version = VERSION;

    this._vao = gl.createVertexArray();   // required in GLES3 even with no attributes
    this._pCopyFlip = program(gl, FRAG_COPY, 'copy');
    this._pCopy = program(gl, FRAG_COPY_NOFLIP, 'copy-noflip');
    this._pBright = null;
    this._pDown = null;
    this._pUp = null;
    this._pCombine = null;
    this._pTrail = null;
    this._pGrade = null;

    /* The readout layer, uploaded separately and composited last. See
       `state.readouts` on render(). */
    this._ro = null;

    this._src = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this._src);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

    this._a = null;
    this._b = null;
    this._mips = [];
    this._tr0 = null;
    this._tr1 = null;
    this._trBright = null;
    this._historyValid = false;
    this._w = 0;
    this._h = 0;

    /* Every effect the chain grows lands in here as { name, run }. Empty is
       the state post_identity.py asserts against. */
    this.passes = [];

    gl.disable(gl.BLEND);
    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.SCISSOR_TEST);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
    gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE);
  }

  Post.prototype.resize = function (w, h) {
    w = Math.max(1, w | 0);
    h = Math.max(1, h | 0);
    if (w === this._w && h === this._h) return;
    var gl = this.gl, i;
    freeTarget(gl, this._a);
    freeTarget(gl, this._b);
    for (i = 0; i < this._mips.length; i++) freeTarget(gl, this._mips[i]);
    this._mips = [];
    this._a = makeTarget(gl, w, h);
    this._b = makeTarget(gl, w, h);
    this._w = w;
    this._h = h;
    /* Down to about 8px on the short side. Levels beyond that stop adding
       reach and start adding a wash over the whole frame. */
    var mw = Math.max(1, w >> 1), mh = Math.max(1, h >> 1);
    var hw = mw, hh = mh;
    while (this._mips.length < 6 && Math.min(mw, mh) >= 8) {
      this._mips.push(makeTarget(gl, mw, mh, true));
      mw = Math.max(1, mw >> 1);
      mh = Math.max(1, mh >> 1);
    }
    /* Half res, like the pyramid's first level: a trail is a smear and does
       not need the detail. Two of them, because a pass cannot read and write
       the same texture. */
    freeTarget(gl, this._tr0);
    freeTarget(gl, this._tr1);
    freeTarget(gl, this._trBright);
    this._tr0 = makeTarget(gl, hw, hh, true);
    this._tr1 = makeTarget(gl, hw, hh, true);
    this._trBright = makeTarget(gl, hw, hh, true);
    this._historyValid = false;
    if (this.canvas.width !== w) this.canvas.width = w;
    if (this.canvas.height !== h) this.canvas.height = h;
  };

  Post.prototype._draw = function (prog, tex, target, setUniforms) {
    var gl = this.gl;
    var vw = target ? target.w : this._w;
    var vh = target ? target.h : this._h;
    gl.bindFramebuffer(gl.FRAMEBUFFER, target ? target.fbo : null);
    gl.viewport(0, 0, vw, vh);
    gl.useProgram(prog);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    var u = gl.getUniformLocation(prog, 'uSrc');
    if (u) gl.uniform1i(u, 0);
    if (setUniforms) setUniforms(gl, prog);
    gl.bindVertexArray(this._vao);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    gl.bindVertexArray(null);
  };

  /* BLOOM, as one entry in `passes` rather than as a special case in render().
   * Registered with setBloom(opts) and removed with setBloom(null), so
   * `passes.length === 0` keeps meaning exactly what post_identity.py checks:
   * nothing is switched on, and the chain must therefore be invisible.
   *
   * opts: { threshold, knee, intensity, scatter, levels, tier }
   *   threshold  luma a pixel must reach to bloom at all. The art is already
   *              additive in twenty-odd places, so this can sit high.
   *   knee       softness of that edge. A hard threshold crawls on moving art.
   *   intensity  how much of the blurred light is added back.
   *   scatter    tent radius on the way up; reach, not brightness.
   *   levels     pyramid depth, capped by the frame size.
   *   cutGain    extra intensity at a FULL KILL, as a multiple of the base:
   *              1.0 doubles it there and adds proportionally less on a
   *              smaller cut, because the ramp is driven by CINE.wash, which
   *              already peaks at each tier's own amplitude. Zero outside a
   *              cut, and zero altogether unless the caller passes CINE
   *              through in state. Brief §6.
   */
  Post.prototype.setBloom = function (opts) {
    var i, gl = this.gl;
    for (i = 0; i < this.passes.length; i++) {
      if (this.passes[i].name === 'bloom') { this.passes.splice(i, 1); break; }
    }
    if (!opts) return this;

    if (!this._pBright) {
      this._pBright = program(gl, FRAG_BRIGHT, 'bright');
      this._pDown = program(gl, FRAG_DOWN, 'down');
      this._pUp = program(gl, FRAG_UP, 'up');
      this._pCombine = program(gl, FRAG_COMBINE, 'combine');
    }

    var o = {
      threshold: opts.threshold === undefined ? 0.72 : opts.threshold,
      knee: opts.knee === undefined ? 0.18 : opts.knee,
      intensity: opts.intensity === undefined ? 0.55 : opts.intensity,
      scatter: opts.scatter === undefined ? 1.0 : opts.scatter,
      levels: opts.levels === undefined ? 5 : opts.levels,
      /* Extra intensity at a full kill, as a multiple of the base. 0 is flat
         — the chain applied at constant strength, which wastes everything the
         director already knows. */
      cutGain: opts.cutGain === undefined ? 0 : opts.cutGain
    };
    var self = this;
    this.passes.push({
      name: 'bloom',
      opts: o,
      run: function (read, write, state) { self._bloom(o, read, write, state); }
    });
    return this;
  };

  /* TRAILS. Registered like bloom, and removed the same way, so
   * `passes.length === 0` keeps meaning "nothing is switched on" for
   * post_identity.py.
   *
   * opts: { seconds, intensity, threshold, knee }
   *   seconds    TIME CONSTANT, not a per-frame factor, and this is the whole
   *              correctness argument. The app runs at whatever rAF gives it
   *              — 60 on one machine, 120 on another — and cinema_clip
   *              captures at a fixed 60. A per-frame decay would make the same
   *              seed leave a trail of one length on screen and a different
   *              one in the mp4, which is a picture fault by construction and
   *              the exact thing docs/ARCHITECTURE.md §1 was built to stop.
   *              Decay is exp(-dt/seconds), so a trail is the same number of
   *              SECONDS long everywhere.
   *   intensity  how much of it is added back.
   *   threshold  its own bright-pass. Held near bloom's by default, but
   *              separate: what is worth smearing and what is worth glowing
   *              are not the same question.
   */
  Post.prototype.setTrails = function (opts) {
    var i, gl = this.gl;
    for (i = 0; i < this.passes.length; i++) {
      if (this.passes[i].name === 'trails') { this.passes.splice(i, 1); break; }
    }
    if (!opts) { this._historyValid = false; return this; }

    if (!this._pBright) {
      this._pBright = program(gl, FRAG_BRIGHT, 'bright');
      this._pDown = program(gl, FRAG_DOWN, 'down');
      this._pUp = program(gl, FRAG_UP, 'up');
      this._pCombine = program(gl, FRAG_COMBINE, 'combine');
    }
    if (!this._pTrail) this._pTrail = program(gl, FRAG_TRAIL, 'trail');

    var o = {
      seconds: opts.seconds === undefined ? 0.10 : opts.seconds,
      intensity: opts.intensity === undefined ? 0.55 : opts.intensity,
      threshold: opts.threshold === undefined ? 0.70 : opts.threshold,
      knee: opts.knee === undefined ? 0.18 : opts.knee,
      spread: opts.spread === undefined ? 1.0 : opts.spread
    };
    var self = this;
    /* FIRST in the list, before bloom, so the smear is part of the picture
       bloom then sees. A trail that does not glow reads as a printing fault. */
    this.passes.unshift({
      name: 'trails',
      opts: o,
      run: function (read, write, state) { self._trails(o, read, write, state); }
    });
    return this;
  };

  /* The history is a fight's worth of state. It belongs to ONE match: carry it
     across a restart and the first frame of the new fight arrives with the old
     one smeared over it. The app calls this on every new match; the capture
     calls it at init and between the columns of a filmstrip. */
  Post.prototype.resetHistory = function () {
    this._historyValid = false;
    return this;
  };

  Post.prototype._trails = function (o, read, write, state) {
    var gl = this.gl, self = this;
    var rect = (state && state.rectN) ? state.rectN : null;
    var dt = (state && state.dt > 0) ? Math.min(state.dt, 0.25) : (1 / 60);

    /* its own bright pass, at half res */
    this._draw(this._pBright, read.tex, this._trBright, function (g, p) {
      g.uniform2f(g.getUniformLocation(p, 'uTexel'), 1 / self._w, 1 / self._h);
      g.uniform1f(g.getUniformLocation(p, 'uThresh'), o.threshold);
      g.uniform1f(g.getUniformLocation(p, 'uKnee'), o.knee);
      if (rect) g.uniform4f(g.getUniformLocation(p, 'uRect'),
                            rect[0], rect[1], rect[2], rect[3]);
      else g.uniform4f(g.getUniformLocation(p, 'uRect'), 0, 0, -1, -1);
    });

    /* A cold buffer holds whatever the driver left in it. Seed it from this
       frame rather than clearing to black: a trail that fades IN over its own
       time constant on the first frame of a fight is a flash of nothing. */
    if (!this._historyValid) {
      this._draw(this._pCopy, this._trBright.tex, this._tr0);
      this._historyValid = true;
    }

    var decay = Math.exp(-dt / Math.max(1e-3, o.seconds));
    this._draw(this._pTrail, this._trBright.tex, this._tr1, function (g, p) {
      g.activeTexture(g.TEXTURE1);
      g.bindTexture(g.TEXTURE_2D, self._tr0.tex);
      g.uniform1i(g.getUniformLocation(p, 'uPrev'), 1);
      g.uniform1f(g.getUniformLocation(p, 'uDecay'), decay);
      g.uniform2f(g.getUniformLocation(p, 'uSpread'),
                  o.spread / self._tr0.w, o.spread / self._tr0.h);
      g.activeTexture(g.TEXTURE0);
    });
    var t = this._tr0; this._tr0 = this._tr1; this._tr1 = t;

    /* Composited with the same masked add bloom uses, so the readout is left
       alone by the same geometry. */
    this._draw(this._pCombine, read.tex, write, function (g, p) {
      g.activeTexture(g.TEXTURE1);
      g.bindTexture(g.TEXTURE_2D, self._tr0.tex);
      g.uniform1i(g.getUniformLocation(p, 'uBloom'), 1);
      g.uniform1f(g.getUniformLocation(p, 'uIntensity'), o.intensity);
      if (rect) g.uniform4f(g.getUniformLocation(p, 'uRect'),
                            rect[0], rect[1], rect[2], rect[3]);
      else g.uniform4f(g.getUniformLocation(p, 'uRect'), 0, 0, -1, -1);
      g.activeTexture(g.TEXTURE0);
    });
  };

  /* THE GRADE. Last in the chain, so it sees the bloom and the trails as
   * part of the picture rather than grading a frame they will later be added
   * to.
   *
   * opts: { vignette, vignetteFrom, washYield, grain, contrast, lift }
   *   vignette      strength of the corner falloff, 0..1.
   *   vignetteFrom  where it starts, as a fraction of the half-diagonal.
   *   washYield     how far the vignette gets out of CINE.wash's way during a
   *                 cut. 1 = fully. See the note above FRAG_GRADE.
   *   grain         amplitude, scaled by luma inside the shader.
   *   contrast      about 0.5. 1.0 is untouched.
   *   lift          added after contrast; negative crushes.
   */
  Post.prototype.setGrade = function (opts) {
    var i, gl = this.gl;
    for (i = 0; i < this.passes.length; i++) {
      if (this.passes[i].name === 'grade') { this.passes.splice(i, 1); break; }
    }
    if (!opts) return this;
    if (!this._pGrade) this._pGrade = program(gl, FRAG_GRADE, 'grade');

    var o = {
      vignette: opts.vignette === undefined ? 0.35 : opts.vignette,
      vignetteFrom: opts.vignetteFrom === undefined ? 0.45 : opts.vignetteFrom,
      washYield: opts.washYield === undefined ? 1 : opts.washYield,
      grain: opts.grain === undefined ? 0.02 : opts.grain,
      contrast: opts.contrast === undefined ? 1.04 : opts.contrast,
      lift: opts.lift === undefined ? 0 : opts.lift
    };
    var self = this;
    this.passes.push({
      name: 'grade',
      opts: o,
      run: function (read, write, state) { self._grade(o, read, write, state); }
    });
    return this;
  };

  Post.prototype._grade = function (o, read, write, state) {
    var self = this;
    var rect = (state && state.rectN) ? state.rectN : null;
    var cutK = (state && state.cutK) ? state.cutK : 0;
    /* The yield. At a full kill with washYield 1 the vignette is gone and the
       director owns the darkening outright; between cuts it owns none of it. */
    var vig = o.vignette * Math.max(0, 1 - o.washYield * cutK);
    var frame = (state && state.frame) ? state.frame : 0;

    this._draw(this._pGrade, read.tex, write, function (g, p) {
      g.uniform2f(g.getUniformLocation(p, 'uSize'), self._w, self._h);
      g.uniform1f(g.getUniformLocation(p, 'uVig'), vig);
      g.uniform1f(g.getUniformLocation(p, 'uVigR'), o.vignetteFrom);
      g.uniform1f(g.getUniformLocation(p, 'uGrain'), o.grain);
      g.uniform1f(g.getUniformLocation(p, 'uContrast'), o.contrast);
      g.uniform1f(g.getUniformLocation(p, 'uLift'), o.lift);
      g.uniform1f(g.getUniformLocation(p, 'uFrame'), frame % 1024);
      if (rect) g.uniform4f(g.getUniformLocation(p, 'uRect'),
                            rect[0], rect[1], rect[2], rect[3]);
      else g.uniform4f(g.getUniformLocation(p, 'uRect'), 0, 0, -1, -1);
    });
  };

  Post.prototype._bloom = function (o, read, write, state) {
    var gl = this.gl, i;
    var n = Math.max(1, Math.min(o.levels | 0, this._mips.length));
    var rect = (state && state.rectN) ? state.rectN : null;

    /* bright-pass, source -> mip 0 (already half size) */
    var self = this;
    this._draw(this._pBright, read.tex, this._mips[0], function (g, p) {
      g.uniform2f(g.getUniformLocation(p, 'uTexel'), 1 / self._w, 1 / self._h);
      g.uniform1f(g.getUniformLocation(p, 'uThresh'), o.threshold);
      g.uniform1f(g.getUniformLocation(p, 'uKnee'), o.knee);
      if (rect) g.uniform4f(g.getUniformLocation(p, 'uRect'),
                            rect[0], rect[1], rect[2], rect[3]);
      else g.uniform4f(g.getUniformLocation(p, 'uRect'), 0, 0, -1, -1);
    });
    /* The bright pass reads the SOURCE, which is stored top-down, so it flips
       on the way in. Every level below is already in GL orientation. */

    for (i = 0; i < n - 1; i++) {
      (function (src, dst) {
        self._draw(self._pDown, src.tex, dst, function (g, p) {
          g.uniform2f(g.getUniformLocation(p, 'uTexel'), 1 / src.w, 1 / src.h);
        });
      })(this._mips[i], this._mips[i + 1]);
    }

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE);
    for (i = n - 1; i > 0; i--) {
      (function (src, dst) {
        self._draw(self._pUp, src.tex, dst, function (g, p) {
          g.uniform2f(g.getUniformLocation(p, 'uTexel'), 1 / src.w, 1 / src.h);
          g.uniform1f(g.getUniformLocation(p, 'uScatter'), o.scatter);
        });
      })(this._mips[i], this._mips[i - 1]);
    }
    gl.disable(gl.BLEND);

    /* Brief §6: a fatal blow should LOOK like one. At cutGain 1.0 a kill
       doubles the bloom and a T2 adds a bit over half of that, because cutK
       carries the tier. Outside a cut it is exactly the chosen look. */
    var amount = o.intensity
               * (1 + o.cutGain * (state && state.cutK ? state.cutK : 0));
    this._draw(this._pCombine, read.tex, write, function (g, p) {
      g.activeTexture(g.TEXTURE1);
      g.bindTexture(g.TEXTURE_2D, self._mips[0].tex);
      g.uniform1i(g.getUniformLocation(p, 'uBloom'), 1);
      g.uniform1f(g.getUniformLocation(p, 'uIntensity'), amount);
      if (rect) g.uniform4f(g.getUniformLocation(p, 'uRect'),
                            rect[0], rect[1], rect[2], rect[3]);
      else g.uniform4f(g.getUniformLocation(p, 'uRect'), 0, 0, -1, -1);
      g.activeTexture(g.TEXTURE0);
    });
  };

  /* state, and this is the contract the builder will have to honour too:
   *
   *   enabled  false renders NOTHING. The caller shows the untouched canvas.
   *   rect     { x, y, w, h } the arena rect in SOURCE pixels. Every emissive
   *            layer in the frame is inside it and the HUD is above it, so a
   *            pass that wants to leave the readout alone restricts itself
   *            here rather than trying to mask by content. See
   *            docs/RENDER-LAYERS.md §1.
   *   cine     { on, cut, tier, zoom, wash, bars, flash, fx, fy } — read only.
   *   readouts a canvas holding ONLY the floats, tags and ult-name callout on
   *            transparency (renderer.roMode 2). Composited last and never
   *            bloomed. Omit it and they stay in the world, which is what
   *            ate them on Ironhail — see docs/RENDER-LAYERS.md §4.
   */
  Post.prototype.render = function (src, state) {
    if (!state || state.enabled === false) return false;
    var gl = this.gl;
    var w = src.width, h = src.height;
    if (!w || !h) return false;
    this.resize(w, h);

    /* Normalised once, here, so no pass has to know the frame size. */
    if (state.rect) {
      /* Source pixels are top-down; everything past the initial copy is
         GL-oriented, bottom-up. Flipped ONCE, here, so no shader has to
         remember which space it is in. */
      state.rectN = [state.rect.x / w,
                     1 - (state.rect.y + state.rect.h) / h,
                     state.rect.w / w,
                     state.rect.h / h];
    }
    /* HOW BIG IS THIS MOMENT, RIGHT NOW — and the director already computes
       it, so this reads rather than re-derives.
     *
     * `CINE.wash` is the scrim's current strength. It rises and falls across
     * the three movements of the beat, and it PEAKS AT THE TIER'S OWN
     * AMPLITUDE: 0.30 for a T2, 0.42 for a T3, 0.55 for a kill. So one number
     * carries both the envelope and the tier, it is zero whenever no cut is
     * running, and it stays correct on its own if the director is ever
     * retuned. A second envelope written here would be a copy that drifts.
     *
     * Normalised by the kill amplitude so a fatal blow is 1.0 and everything
     * else is honestly less than that. The constant is the one thing here
     * that would go stale if TIER_KILL moved — named, so it can be found. */
    var CUT_WASH_MAX = 0.55;            // TIER_KILL.wash
    var wash = (state.cine && state.cine.wash) || 0;
    state.cutK = Math.max(0, Math.min(1, wash / CUT_WASH_MAX));
    /* Seconds since the last composited frame. Trails decay against this and
       not against a frame count, so a trail is the same length in seconds
       whatever rate the caller is running at. Defaulted, never guessed at
       silently: a caller that does not pass it gets 60fps and the trail is
       wrong by exactly the ratio it lied about. */
    if (!(state.dt > 0)) state.dt = 1 / 60;
    /* Grain is keyed to this, not to a clock: two renders of one seed have to
       grain identically or the mp4 and the app are different pictures again. */
    if (!(state.frame >= 0)) state.frame = (this._frame = (this._frame | 0) + 1);

    gl.bindTexture(gl.TEXTURE_2D, this._src);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, src);

    /* Upload -> A, flipping once on the way in. Even with no passes this hop
       is taken on purpose: it is the FBO path, and the identity check is
       worth nothing if the thing it checks is not the thing that runs when an
       effect exists. */
    this._draw(this._pCopyFlip, this._src, this._a);

    var read = this._a, write = this._b, i, p, t;
    for (i = 0; i < this.passes.length; i++) {
      p = this.passes[i];
      if (p.enabled === false) continue;
      p.run(read, write, state);
      t = read; read = write; write = t;
    }

    this._draw(this._pCopy, read.tex, null);

    /* THE READOUTS GO BACK ON TOP, UNTOUCHED, AND LAST.
     *
     * The damage floats, the status tags and the ultimate-name callout are
     * text. On Paradox they survived the bloom; on Ironhail and Dawnbringer,
     * whose art is warm and broad, the same settings ate them — because the
     * light that destroys a readout comes from the art NEXT to it, which no
     * threshold can reach. So they are not in the source that gets bloomed at
     * all: the engine draws them separately (renderer.roMode 2) and they are
     * blended over the finished picture here.
     *
     * Straight alpha, not premultiplied: UNPACK_PREMULTIPLY_ALPHA_WEBGL is
     * false for every upload this file makes, so SRC_ALPHA / ONE_MINUS is the
     * matching blend. Getting that pair wrong shows up as dark fringing round
     * every glyph, which reads as a font problem. */
    if (state.readouts && state.readouts.width) {
      if (!this._ro) {
        this._ro = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, this._ro);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      }
      gl.bindTexture(gl.TEXTURE_2D, this._ro);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE,
                    state.readouts);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      this._draw(this._pCopyFlip, this._ro, null);
      gl.disable(gl.BLEND);
    }
    return true;
  };

  /* Bottom-up, the way GL hands them over. */
  Post.prototype.readPixels = function () {
    var gl = this.gl;
    var px = new Uint8Array(this._w * this._h * 4);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.readPixels(0, 0, this._w, this._h, gl.RGBA, gl.UNSIGNED_BYTE, px);
    return px;
  };

  /* THE CHECK THAT MAKES THE A/B TOGGLE MEAN ANYTHING.
   *
   * Runs the chain over `src` and compares the result against the 2D canvas
   * it was handed, pixel for pixel. With no passes registered the answer must
   * be zero: same bytes, or the plumbing is bending the picture before
   * anything has asked it to, and every later side-by-side is comparing two
   * unknowns.
   *
   * Returns { total, differing, maxDelta, sample } — never throws on a
   * mismatch, because the number is the point.
   */
  Post.prototype.selfTest = function (src, state) {
    var st = {};
    for (var k in (state || {})) st[k] = state[k];
    st.enabled = true;
    this.render(src, st);

    var w = this._w, h = this._h;
    var got = this.readPixels();
    var want = src.getContext('2d').getImageData(0, 0, w, h).data;

    var differing = 0, maxDelta = 0, sample = null, x, y, i, j, d, ch;
    for (y = 0; y < h; y++) {
      /* GL row 0 is the BOTTOM row; getImageData row 0 is the top. */
      var gy = h - 1 - y;
      for (x = 0; x < w; x++) {
        i = (gy * w + x) * 4;
        j = (y * w + x) * 4;
        var bad = false;
        for (ch = 0; ch < 3; ch++) {          // RGB. alpha:false makes A moot.
          d = Math.abs(got[i + ch] - want[j + ch]);
          if (d > maxDelta) maxDelta = d;
          if (d !== 0) bad = true;
        }
        if (bad) {
          differing++;
          if (!sample) {
            sample = { x: x, y: y,
                       got: [got[i], got[i + 1], got[i + 2]],
                       want: [want[j], want[j + 1], want[j + 2]] };
          }
        }
      }
    }
    return { total: w * h, differing: differing, maxDelta: maxDelta,
             sample: sample, passes: this.passes.length };
  };

  Post.prototype.dispose = function () {
    var gl = this.gl, i;
    freeTarget(gl, this._a);
    freeTarget(gl, this._b);
    for (i = 0; i < this._mips.length; i++) freeTarget(gl, this._mips[i]);
    this._mips = [];
    freeTarget(gl, this._tr0);
    freeTarget(gl, this._tr1);
    freeTarget(gl, this._trBright);
    this._tr0 = this._tr1 = this._trBright = null;
    gl.deleteTexture(this._src);
    if (this._ro) gl.deleteTexture(this._ro);
    this._ro = null;
    gl.deleteProgram(this._pCopy);
    gl.deleteProgram(this._pCopyFlip);
    if (this._pTrail) gl.deleteProgram(this._pTrail);
    if (this._pGrade) gl.deleteProgram(this._pGrade);
    if (this._pBright) {
      gl.deleteProgram(this._pBright);
      gl.deleteProgram(this._pDown);
      gl.deleteProgram(this._pUp);
      gl.deleteProgram(this._pCombine);
    }
    gl.deleteVertexArray(this._vao);
    this._a = this._b = null;
  };

  /* THE SPREAD, NAMED IN ONE PLACE so the app, the filmstrip tool and the
     builder cannot drift into showing Rick three different things. Rule 2:
     offer a spread, not a guess — and price it from measurement where a
     measurement can price it. These three differ ONLY in intensity and the
     threshold that follows from it; reach and knee are held so the comparison
     has one variable. */
  var SPREAD = {
    /* CHOSEN BY RICK, 2026-08-27, off the sheet at
       05-reference/post/bloom-spread-paradox-heartwood-25064.png — three
       moments of seed 25064, four columns, one runtime.

       MID over HIGH on legibility: at HIGH the relic blows out to a white
       disc and the damage floats are lost (the `24` at t=37.4 and the `89` at
       the kill). At MID the lightning and the relic read as light sources and
       every float on the sheet still reads.

       REVISED THE SAME DAY, TO LOW, and the reason is the one this project
       keeps relearning: MID was chosen when Paradox was the only evidence.
       On ironhail v dawnbringer, whose relic bodies are already near white,
       MID fuses the two fighters into a single mass by t=25.9 and HIGH loses
       them entirely. LOW is the only setting on the two-pairing sheet
       (bloom-spread-paradox-heartwood-25064-ironhail-dawnbringer-4412.png)
       where both relics stay separable on BOTH kinds of art. It is subtler on
       Paradox's lightning than MID was, and that is the price.

       The readout question that was tangled up with this is now answered
       separately and structurally -- floats, tags and the ult-name callout
       leave the bloom's source entirely at renderer.roMode 1, so they read at
       every setting. See docs/RENDER-LAYERS.md §4. */
    DEFAULT: 'low',
    off: null,
    low: { threshold: 0.80, knee: 0.16, intensity: 0.35, scatter: 1.0, levels: 5, cutGain: 0.6 },
    mid: { threshold: 0.72, knee: 0.18, intensity: 0.60, scatter: 1.1, levels: 5, cutGain: 0.6 },
    high: { threshold: 0.62, knee: 0.22, intensity: 0.95, scatter: 1.25, levels: 6, cutGain: 0.6 }
  };

  /* THE TRAIL SPREAD, and it varies ONE thing: how long the smear lasts, in
     seconds. Intensity and threshold are held, because "how long" is the
     question a person can actually answer from a picture — and because the
     bloom spread already established the register these sit inside.

     Seconds, not frames. A trail of 0.12s is 0.12s in a 120Hz app and in a
     60fps mp4; a trail of "8 frames" is two different pictures. */
  var TRAILS = {
    /* CHOSEN BY RICK, 2026-08-27, off the trail spread; REVISED THE SAME
       DAY to LONG once bloom came down to LOW.

       THE TWO SETTINGS ARE NOT INDEPENDENT, which is why the sheet was
       re-rendered rather than re-read. Under MID the long tails competed
       with the bloom's own glow and the arena read as busy. Under LOW they
       are the brightest moving thing in the frame and read as speed. A look
       chosen against a base that has since moved is a look chosen for the
       wrong picture.

       THE COST IS THE BEADING AND IT WAS TAKEN KNOWINGLY. At 60fps a fast
       arc beads, because a persistence buffer knows where a thing WAS and
       not where it went, and the artefact scales with how many frames of
       history are held: LONG holds about fourteen where SHORT held four. On
       the flail's arc it reads as stroboscopy rather than as a smear.

       The fix is to accumulate at the sim's 120Hz instead of the render's
       60, and tools/post_cost.py has priced it: the frame is already 7.36ms
       against an 8.33ms budget at 120Hz BEFORE the chain, on this Intel UHD.
       A real trade, not a cleanup. */
    DEFAULT: 'long',
    off: null,
    short: { seconds: 0.06, intensity: 0.55, threshold: 0.70, knee: 0.18 },
    mid:   { seconds: 0.12, intensity: 0.55, threshold: 0.70, knee: 0.18 },
    long:  { seconds: 0.24, intensity: 0.55, threshold: 0.70, knee: 0.18 }
  };

  /* THE CUT RAMP SPREAD. One variable: how much brighter a fatal blow gets.
     The control is the chosen look with the ramp OFF — flat intensity — so
     the sheet answers only "should the director drive this", and not that
     question tangled up with "is the base right", which is already settled. */
  var CUTRAMP = {
    /* CHOSEN BY RICK, 2026-08-27: gentle, 0.6. Carried on every SPREAD entry
       above, so a caller that takes the chosen look gets the chosen ramp with
       it and cannot accidentally ship the chain flat.

       0.6 is a lift you notice without being able to name, and it is the
       safest of the three against the failure that pushed bloom down to LOW
       in the first place -- warm relic bodies fusing into one mass. STRONG
       would have put a kill briefly into the HIGH register; that was both the
       argument for it and the argument against it. */
    DEFAULT: 'gentle',
    off:    0,
    gentle: 0.6,
    mid:    1.2,
    strong: 2.0
  };

  /* THE GRADE SPREAD. One variable: how graded. All three components move
     together, because "how filmic does this look" is the question a person
     can answer from a picture — asking about contrast, vignette and grain
     separately would be three sheets to settle one impression. */
  var GRADE = {
    /* CHOSEN BY RICK, 2026-08-27, off the grade sheet. Corners sink, centre
       holds, grain visible without being obtrusive.

       The vignette's washYield is 1 here, and the reason is measured rather
       than argued: tools/post_grade_probe.py puts the un-yielded vignette at
       1.18 of 37.09 mean luma on a cut frame -- 3.2% -- and the yield
       recovers 62% of that. Small either way. The scrim is much the stronger
       of the two darkenings and the vignette is a garnish on top of it, which
       is the opposite of the "two effects fighting" this was first framed as. */
    DEFAULT: 'mid',
    off:    null,
    subtle: { vignette: 0.22, vignetteFrom: 0.55, washYield: 1,
              grain: 0.012, contrast: 1.02, lift: 0 },
    mid:    { vignette: 0.38, vignetteFrom: 0.45, washYield: 1,
              grain: 0.022, contrast: 1.05, lift: -0.004 },
    strong: { vignette: 0.55, vignetteFrom: 0.35, washYield: 1,
              grain: 0.034, contrast: 1.09, lift: -0.008 }
  };

  var API = {
    VERSION: VERSION,
    SPREAD: SPREAD,
    TRAILS: TRAILS,
    CUTRAMP: CUTRAMP,
    GRADE: GRADE,
    create: function (canvas) { return new Post(canvas); },
    supported: function () {
      try {
        var c = (typeof OffscreenCanvas !== 'undefined')
          ? new OffscreenCanvas(1, 1)
          : (typeof document !== 'undefined' ? document.createElement('canvas') : null);
        return !!(c && c.getContext('webgl2'));
      } catch (e) { return false; }
    }
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  root.SWBPost = API;
})(typeof globalThis !== 'undefined' ? globalThis : this);
