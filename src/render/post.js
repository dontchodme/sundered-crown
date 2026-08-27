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
 * THIS VERSION ADDS NO EFFECT. It is step 2 of §8 — source canvas ->
 * framebuffer -> a single trivial shader -> screen, with the A/B toggle,
 * before any effect exists, because the plumbing is where this goes wrong and
 * not the maths. The one thing it must do is be INVISIBLE: passthrough has to
 * come back byte-identical to the 2D canvas it was handed, and `selfTest()`
 * is how that gets asserted rather than believed.
 *
 * THE CONTROL IS THE OLD PIXELS. `state.enabled === false` does not render a
 * neutral pass — it renders nothing at all, and the caller shows the original
 * canvas. A control that goes through the same code it is controlling for is
 * not a control.
 */
(function (root) {
  'use strict';

  var VERSION = '0.1.0-plumbing';

  /* A fullscreen triangle, not a quad: no seam down the diagonal, one fewer
     vertex, and the clip-space maths is the same. */
  var VERT = [
    '#version 300 es',
    'out vec2 vUv;',
    'void main(){',
    /* 0 -> (-1,-1), 1 -> (3,-1), 2 -> (-1,3) */
    '  vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);',
    '  vUv = p;',
    '  gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);',
    '}'
  ].join('\n');

  /* Sampling is NEAREST at 1:1, so this is a copy and must stay one. Any
     arithmetic here — a multiply by 1.0, a clamp, a pow(x, 1.0) — risks
     coming back off by a bit on some driver, and then the identity check
     that guards every later effect is already red for a reason nobody
     remembers. Effects go in their OWN pass. */
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

  /* Same copy, without the flip. Passes after the first are already in GL
     orientation, so flipping again would stand the picture back on its head. */
  var FRAG_COPY_NOFLIP = FRAG_COPY.replace('vec2(vUv.x, 1.0 - vUv.y)', 'vUv');

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

  /* An offscreen RGBA8 target. NEAREST and CLAMP_TO_EDGE on purpose: at 1:1
     they make a copy exact, and every later effect that wants filtering can
     ask for it on its own sampler rather than inheriting it here. */
  function makeTarget(gl, w, h) {
    var tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA,
                  gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
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

    this._vao = gl.createVertexArray();      // required in GLES3 even with no attributes
    this._pCopyFlip = program(gl, FRAG_COPY, 'copy');
    this._pCopy = program(gl, FRAG_COPY_NOFLIP, 'copy-noflip');

    this._src = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this._src);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

    this._a = null;
    this._b = null;
    this._w = 0;
    this._h = 0;

    /* Every effect this chain grows lands in here as { name, program, set }.
       Empty is the honest state today and the A/B toggle still has something
       to prove against it: that the plumbing itself costs no pixels. */
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
    var gl = this.gl;
    freeTarget(gl, this._a);
    freeTarget(gl, this._b);
    this._a = makeTarget(gl, w, h);
    this._b = makeTarget(gl, w, h);
    this._w = w;
    this._h = h;
    if (this.canvas.width !== w) this.canvas.width = w;
    if (this.canvas.height !== h) this.canvas.height = h;
  };

  Post.prototype._draw = function (prog, tex, target) {
    var gl = this.gl;
    gl.bindFramebuffer(gl.FRAMEBUFFER, target ? target.fbo : null);
    gl.viewport(0, 0, this._w, this._h);
    gl.useProgram(prog);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    var u = gl.getUniformLocation(prog, 'uSrc');
    if (u) gl.uniform1i(u, 0);
    gl.bindVertexArray(this._vao);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    gl.bindVertexArray(null);
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
   *            Brief §6: intensity ramps with the director's own tier so a
   *            fatal blow looks like one. Nothing consumes it yet.
   */
  Post.prototype.render = function (src, state) {
    if (!state || state.enabled === false) return false;
    var gl = this.gl;
    var w = src.width, h = src.height;
    if (!w || !h) return false;
    this.resize(w, h);

    gl.bindTexture(gl.TEXTURE_2D, this._src);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, src);

    /* Upload -> A, flipping once on the way in. Even with no effect passes
       this hop is taken on purpose: it is the FBO path, and the identity
       check is worth nothing if the thing it checks is not the thing that
       runs when an effect exists. */
    this._draw(this._pCopyFlip, this._src, this._a);

    var read = this._a, write = this._b, i, p;
    for (i = 0; i < this.passes.length; i++) {
      p = this.passes[i];
      if (p.enabled === false) continue;
      gl.useProgram(p.program);
      if (p.set) p.set(gl, p.program, state, read, this);
      this._draw(p.program, read.tex, write);
      var t = read; read = write; write = t;
    }

    this._draw(this._pCopy, read.tex, null);
    return true;
  };

  /* Bottom-up, the way GL hands them over. The caller flips if it wants to
     compare against getImageData. */
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
   * it was handed, pixel for pixel. With no effect passes the answer must be
   * zero: same bytes, or the plumbing is bending the picture before anything
   * has asked it to, and every later side-by-side is comparing two unknowns.
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
    var gl = this.gl;
    freeTarget(gl, this._a);
    freeTarget(gl, this._b);
    gl.deleteTexture(this._src);
    gl.deleteProgram(this._pCopy);
    gl.deleteProgram(this._pCopyFlip);
    gl.deleteVertexArray(this._vao);
    this._a = this._b = null;
  };

  var API = {
    VERSION: VERSION,
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
