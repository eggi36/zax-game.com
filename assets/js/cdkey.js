/* CD key generator for Zax: The Alien Hunter.
   The game's check (Zax.exe 0x46b540): the key is cleaned up (upper case, O→0, I→1, L→1, B→8, S→5, digits only)
   and must have 20 digits: two numbers of ten digits, first and last, v = first << 32 | last. Valid when
   bits 20-59 of v modulo 0xffff, xor 0x9249, equal the low 16 bits of last. Bits 16-19 of last are the key's
   kind; the game never asks for it. Everything runs in the browser, nothing is sent anywhere. */
(function () {
  'use strict';
  var M = 0xffffn;

  function check(text) {
    var s = String(text).toUpperCase().replace(/O/g, '0').replace(/[IL]/g, '1').replace(/B/g, '8')
      .replace(/S/g, '5').replace(/[^0-9]/g, '');
    if (s.length !== 20) return false;
    var first = BigInt(s.slice(0, 10)), last = BigInt(s.slice(10));
    if (first > 0xffffffffn || last > 0xffffffffn) return false;     // %010u reads 32-bit numbers
    var v = (first << 32n) | last;
    var t = (v >> 20n) & 0xffffffffffn;                               // bits 20-59
    return (last & M) === (((t % M) ^ 0x9249n) & M);
  }

  function random32() {
    var a = new Uint32Array(1);
    crypto.getRandomValues(a);
    return BigInt(a[0]);
  }

  function generate() {
    var first = random32();
    var r = random32();
    var hi = r & 0xfffn, kind = (r >> 12n) & 0xfn;                    // bits 20-31 and 16-19 of last
    var t = ((first & 0xfffffffn) << 12n) | hi;                       // bits 20-59 of v
    var last = (hi << 20n) | (kind << 16n) | (((t % M) ^ 0x9249n) & M);
    var digits = first.toString().padStart(10, '0') + last.toString().padStart(10, '0');
    return digits.match(/.{4}/g).join('-');
  }

  var out = document.getElementById('cdkey');
  var btn = document.getElementById('cdkey-new');
  var copy = document.getElementById('cdkey-copy');
  if (!out || !btn) return;
  function fresh() {
    var k;
    do { k = generate(); } while (!check(k));
    out.textContent = k;
    if (copy) copy.textContent = 'Copy';
  }
  btn.addEventListener('click', fresh);
  if (copy) copy.addEventListener('click', function () {
    var done = function () { copy.textContent = 'Copied'; };
    if (navigator.clipboard) navigator.clipboard.writeText(out.textContent).then(done, function () {});
  });
  fresh();
  window.zaxCdKey = { check: check, generate: generate };
})();
