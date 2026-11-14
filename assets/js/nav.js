// Navigationsleiste – Nachbau von top_nav.swf (zax-game.com, 2002–2004)
//
// * Ein kleiner Flash-Zeitleisten-Player spielt die Original-Animationen aus
//   assets/js/nav-data.js ab (aus top_nav.swf exportiert): Einfahren der Leiste,
//   Lichtreflex über dem Logo, Funken an den beiden Kapseln, Ladeanzeige.
// * Die Punktmatrix-Anzeige und das Menü sind HTML, damit sie erweiterbar bleiben;
//   ihre Effekte (Aufklappen, Geisterbilder, Aufbau Zeile für Zeile) folgen den
//   Bildern der Originaldatei.
// * Töne: Hover (snd38), Tippen der Anzeige (snd15), Zap (snd60), Knistern (snd62).
//   Das Dauer-Knistern alle ~10 s (Sprite 64) ist bewusst entfernt.
// * Anzeige zeigt beim Überfahren den Menüpunkt; Klick lädt sofort.
(function () {
  'use strict';
  var nav = document.querySelector('.navbar');
  if (!nav) return;
  var FPS = 12, TICK = 1000 / FPS;
  var display = nav.querySelector('.display');
  var pageText = display && display.querySelector('.page-text');
  var menuLinks = Array.prototype.slice.call(nav.querySelectorAll('.menu a'));
  var reduced = false;
  try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  // ---------------------------------------------------------------- Speicher
  function load(store, key) { try { return window[store].getItem(key); } catch (e) { return null; } }
  function save(store, key, val) { try { window[store].setItem(key, val); } catch (e) {} }

  // ---------------------------------------------------------------- Töne
  var soundOn = load('localStorage', 'zaxSound') !== 'off';
  var base = (nav.getAttribute('data-sound-base') || 'assets/snd/');
  var SOUNDS = { 15: 'typing.mp3', 38: 'hover.mp3', 60: 'zap.mp3', 62: 'crackle.mp3' };
  var pool = {};
  function sound(id, vol) {
    if (!soundOn || !SOUNDS[id]) return;
    try {
      var list = pool[id] || (pool[id] = []), a = null;
      for (var i = 0; i < list.length; i++) if (list[i].paused || list[i].ended) { a = list[i]; break; }
      if (!a) { if (list.length > 3) return; a = new Audio(base + SOUNDS[id]); list.push(a); }
      a.volume = vol || 0.6; a.currentTime = 0;
      var p = a.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  var toggle = document.querySelector('.sound-toggle');
  function showToggle() { if (toggle) { toggle.textContent = 'Sound: ' + (soundOn ? 'on' : 'off'); toggle.setAttribute('aria-pressed', soundOn ? 'true' : 'false'); } }
  if (toggle) {
    toggle.hidden = false; showToggle();
    toggle.addEventListener('click', function () { soundOn = !soundOn; save('localStorage', 'zaxSound', soundOn ? 'on' : 'off'); showToggle(); });
  }

  // ---------------------------------------------------------------- Skalierung
  function scale() {
    var s = Math.min(1, document.documentElement.clientWidth / 797);
    document.documentElement.style.setProperty('--nav-scale', s);
  }
  scale();
  window.addEventListener('resize', scale);

  // ---------------------------------------------------------------- Flash-Player
  var DATA = window.ZAX_NAV;
  var SVGNS = 'http://www.w3.org/2000/svg';
  var player = null;

  function Player(svg, data) {
    this.svg = svg; this.data = data; this.defs = document.createElementNS(SVGNS, 'defs');
    svg.appendChild(this.defs); this.filters = {}; this.made = {}; this.n = 0;
    this.urlHook = null;
    var root = { def: data.root, frame: -1, playing: true, dl: {}, g: svg, name: '', parent: null, kids: [] };
    this.root = root;
  }
  Player.prototype.symbol = function (cid) {
    var id = 'zx' + cid;
    if (!this.made[cid]) {
      var g = document.createElementNS(SVGNS, 'g'); g.setAttribute('id', id);
      // eindeutige IDs für Verläufe/Muster in diesem Dokument
      g.innerHTML = this.data.chars[cid].svg;
      this.defs.appendChild(g); this.made[cid] = true;
    }
    return '#' + id;
  };
  Player.prototype.filter = function (x) {
    var key = x.join(',');
    if (this.filters[key]) return this.filters[key];
    var id = 'zxf' + (++this.n), f = document.createElementNS(SVGNS, 'filter');
    f.setAttribute('id', id); f.setAttribute('color-interpolation-filters', 'sRGB');
    f.setAttribute('x', '-50%'); f.setAttribute('y', '-50%'); f.setAttribute('width', '200%'); f.setAttribute('height', '200%');
    var m = document.createElementNS(SVGNS, 'feColorMatrix'); m.setAttribute('type', 'matrix');
    m.setAttribute('values', [x[0] / 256, 0, 0, 0, x[4] / 255, 0, x[1] / 256, 0, 0, x[5] / 255, 0, 0, x[2] / 256, 0, x[6] / 255, 0, 0, 0, 1, 0].join(' '));
    f.appendChild(m); this.defs.appendChild(f);
    return (this.filters[key] = 'url(#' + id + ')');
  };
  Player.prototype.style = function (o) {
    var el = o.el, m = o.m, x = o.x;
    el.setAttribute('transform', 'matrix(' + m.join(' ') + ')');
    if (x) {
      el.setAttribute('opacity', Math.max(0, Math.min(1, x[3] / 256 + x[7] / 255)));
      if (x[0] !== 256 || x[1] !== 256 || x[2] !== 256 || x[4] || x[5] || x[6]) el.setAttribute('filter', this.filter(x));
      else el.removeAttribute('filter');
    } else { el.removeAttribute('opacity'); el.removeAttribute('filter'); }
    if (o.clipUse) o.clipUse.setAttribute('transform', 'matrix(' + m.join(' ') + ')');
  };
  Player.prototype.create = function (clip, op, born) {
    var cid = op.c, ch = this.data.chars[cid];
    var o = { cid: cid, born: born, m: op.m || [1, 0, 0, 1, 0, 0], x: op.x || null, depth: op.d, clip: op.clip || 0 };
    if (!ch) { o.el = document.createElementNS(SVGNS, 'g'); o.dead = true; return o; }
    var g = document.createElementNS(SVGNS, 'g'); o.el = g;
    if (ch.t === 's') {
      var u = document.createElementNS(SVGNS, 'use'); u.setAttribute('href', this.symbol(cid)); g.appendChild(u);
    } else if (ch.t === 'b') {
      for (var i = 0; i < ch.up.length; i++) {
        var r = ch.up[i], gu = document.createElementNS(SVGNS, 'use');
        gu.setAttribute('href', this.symbol(r[0])); gu.setAttribute('transform', 'matrix(' + r[1].join(' ') + ')'); g.appendChild(gu);
      }
    } else if (ch.t === 'm') {
      o.mc = { def: ch, frame: -1, playing: true, dl: {}, g: g, name: op.n || '', parent: clip, kids: [] };
      if (op.n) clip.kids.push(o.mc);
    }
    if (o.clip && ch.t === 's') {
      var cp = document.createElementNS(SVGNS, 'clipPath'), id = 'zxc' + (++this.n);
      cp.setAttribute('id', id); var cu = document.createElementNS(SVGNS, 'use'); cu.setAttribute('href', this.symbol(cid));
      cp.appendChild(cu); this.defs.appendChild(cp); o.clipId = id; o.clipUse = cu;
      g.style.display = 'none';
    }
    this.style(o);
    return o;
  };
  Player.prototype.order = function (clip) {
    var depths = Object.keys(clip.dl).map(Number).sort(function (a, b) { return a - b; });
    var parent = clip.g, holder = null, until = -1;
    while (parent.lastChild && parent.lastChild !== this.defs) parent.removeChild(parent.lastChild);
    for (var i = 0; i < depths.length; i++) {
      var o = clip.dl[depths[i]];
      if (holder && depths[i] > until) holder = null;
      (holder || parent).appendChild(o.el);
      if (o.clipId) {
        holder = document.createElementNS(SVGNS, 'g'); holder.setAttribute('clip-path', 'url(#' + o.clipId + ')');
        parent.appendChild(holder); until = o.clip;
      }
    }
  };
  // Darstellungsliste für ein Bild anwenden
  Player.prototype.apply = function (clip, f, quiet) {
    var ops = clip.def.f[f] || [], changed = false, acts = [];
    for (var i = 0; i < ops.length; i++) {
      var op = ops[i], o;
      if (op.o === 'p') {
        o = clip.dl[op.d];
        if (op.mv && o && op.c === undefined) {
          if (op.m) o.m = op.m; if (op.x !== undefined) o.x = op.x; this.style(o);
        } else {
          if (o) this.destroy(clip, o);
          o = this.create(clip, op, f); clip.dl[op.d] = o; changed = true;
          if (o.mc) this.enter(o.mc, 0, quiet);
        }
      } else if (op.o === 'r') {
        o = clip.dl[op.d]; if (o) { this.destroy(clip, o); delete clip.dl[op.d]; changed = true; }
      } else if (op.o === 's') { if (!quiet) sound(op.id, clip.vol); }
      else if (op.o === 'a') acts.push(op.a);
    }
    if (changed) this.order(clip);
    return acts;
  };
  Player.prototype.destroy = function (clip, o) {
    if (o.mc) { var k = clip.kids.indexOf(o.mc); if (k >= 0) clip.kids.splice(k, 1); }
    if (o.clipUse && o.clipUse.parentNode) this.defs.removeChild(o.clipUse.parentNode);
    if (o.el.parentNode) o.el.parentNode.removeChild(o.el);
  };
  Player.prototype.enter = function (clip, f, quiet) {
    clip.frame = f;
    var acts = this.apply(clip, f, quiet);
    for (var i = 0; i < acts.length; i++) this.run(clip, acts[i]);
  };
  Player.prototype.find = function (clip, path) {
    if (!path) return clip;
    var r = this.root, parts = path.replace(/^\//, '').split('/');
    for (var i = 0; i < parts.length && r; i++) {
      var n = parts[i], hit = null;
      for (var k = 0; k < r.kids.length; k++) if (r.kids[k].name === n) hit = r.kids[k];
      r = hit;
    }
    return r;
  };
  Player.prototype.run = function (clip, acts) {
    var t = clip;
    for (var i = 0; i < acts.length; i++) {
      var a = acts[i];
      if (a[0] === 'target') t = this.find(clip, a[1]);
      else if (!t) continue;
      else if (a[0] === 'stop') t.playing = false;
      else if (a[0] === 'play') t.playing = true;
      else if (a[0] === 'goto') this.goto(t, a[1]);
      else if (a[0] === 'label') { if (a[1] in t.def.l) this.goto(t, t.def.l[a[1]]); }
      else if (a[0] === 'url' && this.urlHook) this.urlHook(a[1], a[2]);
    }
  };
  // Sprung wie im Flash Player: rückwärts wird die Liste neu aufgebaut,
  // unveränderte Objekte bleiben erhalten (laufende Unter-Clips spielen weiter).
  Player.prototype.goto = function (clip, f, quiet) {
    if (f === clip.frame) return;
    if (f < clip.frame) {
      var want = {};
      for (var j = 0; j <= f; j++) {
        var ops = clip.def.f[j] || [];
        for (var i = 0; i < ops.length; i++) {
          var op = ops[i];
          if (op.o === 'p') {
            if (op.mv && op.c === undefined && want[op.d]) { if (op.m) want[op.d].m = op.m; if (op.x !== undefined) want[op.d].x = op.x; }
            else want[op.d] = { op: op, born: j, m: op.m, x: op.x };
          } else if (op.o === 'r') delete want[op.d];
        }
      }
      var changed = false;
      for (var d in clip.dl) {
        var o = clip.dl[d], w = want[d];
        if (!w || w.op.c !== o.cid || w.born !== o.born) { this.destroy(clip, o); delete clip.dl[d]; changed = true; }
      }
      for (d in want) {
        w = want[d]; o = clip.dl[d];
        if (o) { if (w.m) o.m = w.m; o.x = w.x === undefined ? o.x : w.x; this.style(o); continue; }
        var po = {}; for (var k in w.op) po[k] = w.op[k]; po.m = w.m; po.x = w.x;
        o = this.create(clip, po, w.born); clip.dl[d] = o; changed = true;
        if (o.mc) this.enter(o.mc, 0, true);
      }
      if (changed) this.order(clip);
      clip.frame = f - 1;
    }
    while (clip.frame < f - 1) { clip.frame++; this.apply(clip, clip.frame, true); }
    this.enter(clip, f, quiet);
  };
  Player.prototype.step = function (clip) {
    var kids = [];
    for (var d in clip.dl) if (clip.dl[d].mc) kids.push(clip.dl[d].mc);
    if (clip.playing) {
      var n = clip.frame + 1;
      if (n >= clip.def.f.length) this.goto(clip, 0); else this.enter(clip, n);
    }
    for (var i = 0; i < kids.length; i++) if (kids[i].parent === clip) this.step(kids[i]);
  };

  // ---------------------------------------------------------------- Anzeige (Punktmatrix)
  // Original: Text klappt in 4 Bildern auf (Höhe 38/59/79/100 %, Deckkraft 20/47/73/100 %),
  // danach dreimal kurz zwei aufgehellte Geisterbilder (+2 px / −3 px, Höhe 84 %).
  var ghostA = null, ghostB = null, dispTimer = null;
  if (display) {
    ghostA = document.createElement('span'); ghostB = document.createElement('span');
    ghostA.className = ghostB.className = 'ghost'; ghostA.setAttribute('aria-hidden', 'true'); ghostB.setAttribute('aria-hidden', 'true');
    display.appendChild(ghostA); display.appendChild(ghostB);
  }
  function showTitle(text, delayFrames, withSound, done) {
    if (!display) return;
    clearInterval(dispTimer);
    var f = -delayFrames, label = display.querySelector('.page-text');
    var Y = [0.38, 0.59, 0.79, 1], A = [0.2, 0.47, 0.73, 1], GH = [4, 7, 11];
    label.textContent = text; ghostA.textContent = ghostB.textContent = text;
    label.style.opacity = 0; ghostA.style.visibility = ghostB.style.visibility = 'hidden';
    if (reduced) { label.style.opacity = 1; label.style.transform = ''; if (done) done(); return; }
    function frame() {
      if (f >= 0 && f < 4) {
        if (f === 0 && withSound) sound(15, 0.6);
        label.style.opacity = A[f]; label.style.transform = 'scaleY(' + Y[f] + ')';
      }
      var g = f >= 4 && GH.indexOf(f) >= 0;
      ghostA.style.visibility = ghostB.style.visibility = g ? 'visible' : 'hidden';
      f++;
      if (f > 12) { clearInterval(dispTimer); if (done) done(); }
    }
    frame(); dispTimer = setInterval(frame, TICK);
  }

  // ---------------------------------------------------------------- Aufbau
  var svg = null;
  if (DATA && window.SVGElement) {
    svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('class', 'nav-anim'); svg.setAttribute('viewBox', '0 0 797 107');
    svg.setAttribute('width', '797'); svg.setAttribute('height', '107'); svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    nav.insertBefore(svg, nav.firstChild);
    // Pfade der Bitmaps relativ zur aktuellen Seite
    var assetBase = nav.getAttribute('data-asset-base') || '';
    if (assetBase) for (var c in DATA.chars) if (DATA.chars[c].svg) DATA.chars[c].svg = DATA.chars[c].svg.replace(/href="assets\//g, 'href="' + assetBase + 'assets/');
    player = new Player(svg, DATA);
    nav.classList.add('animated');
  }

  var booted = load('sessionStorage', 'zaxBooted') === '1';
  var title = pageText ? pageText.textContent : '';

  function revealMenu(stagger) {
    // Original: ein Menüpunkt pro Bild (Bilder 18–23), 12 Bilder/s
    menuLinks.forEach(function (a, i) {
      var li = a.parentNode;
      if (!stagger) { li.classList.add('on'); return; }
      setTimeout(function () { li.classList.add('on'); }, i * TICK);
    });
  }

  // Seiteninhalt erst nach der Bootsequenz zeigen (Klasse kommt aus dem <head>)
  function revealPage() {
    var de = document.documentElement;
    if (!de.classList.contains('zax-boot')) return;
    de.classList.add('zax-reveal'); de.classList.remove('zax-boot');
  }

  var running = null;
  function loop(onFrame) {
    var last = performance.now(), acc = 0;
    function tick(now) {
      acc += Math.min(now - last, 500); last = now;
      while (acc >= TICK) { acc -= TICK; onFrame(); }
      running = requestAnimationFrame(tick);
    }
    running = requestAnimationFrame(tick);
  }

  if (!player) {
    revealMenu(false); revealPage();
  } else if (!booted && !reduced) {
    // Erster Besuch in dieser Sitzung: Ladeanzeige, dann Bootsequenz wie im Original
    save('sessionStorage', 'zaxBooted', '1');
    nav.classList.add('booting');
    var root = player.root, introFrames = 20, fr = 0;
    root.def.f[0] = root.def.f[0].filter(function (op) { return op.o !== 'a'; });
    player.enter(root, 0, false);          // „WELCOME ZAX … PLEASE WAIT …“
    root.playing = false;
    if (display) { display.querySelector('.page-text').style.opacity = 0; }
    loop(function () {
      fr++;
      if (fr < introFrames) { player.step(root); return; }
      if (fr === introFrames) { root.playing = true; player.goto(root, 9); nav.classList.remove('booting'); return; }
      player.step(root);
      if (root.frame === 17) revealMenu(true);
      if (root.frame === 23 && !root.titled) { root.titled = true; showTitle(title, 12, true, revealPage); }
    });
  } else {
    // Weitere Seiten: Endzustand sofort, Funken im Ruhezustand
    var r = player.root;
    player.goto(r, 9, true); player.goto(r, 29, true); r.playing = false;
    ['left_spark', 'right_spark'].forEach(function (n) {
      var mc = player.find(r, '/' + n);
      if (mc) { player.goto(mc, mc.def.l.loop_start, true); mc.playing = true; }
    });
    revealMenu(false); revealPage();
    loop(function () { player.step(r); });
  }

  // ---------------------------------------------------------------- Menü
  var leaveTimer = null;
  menuLinks.concat(Array.prototype.slice.call(nav.querySelectorAll('.home-link'))).forEach(function (a) {
    function over() {
      sound(38, 0.5);
      if (nav.classList.contains('booting') || !display) return;
      clearTimeout(leaveTimer);
      showTitle(a.getAttribute('data-label') || a.textContent, 0, false);
    }
    function out() {
      if (nav.classList.contains('booting') || !display) return;
      clearTimeout(leaveTimer);
      leaveTimer = setTimeout(function () { showTitle(title, 0, false); }, 150);
    }
    a.addEventListener('mouseenter', over);
    a.addEventListener('mouseleave', out);
    a.addEventListener('focus', function () { if (a.matches(':focus-visible')) over(); });
    a.addEventListener('blur', out);
  });
})();
