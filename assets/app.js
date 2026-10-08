(function () {
  var base = document.body.getAttribute('data-base') || '';
  var KEY = 'smd_koszyk';
  var PRODUCTS = {
    tom1: { name: 'Stare małe Dziecko · Tom I', sub: 'Pusta ławka i Niebo · e-book EPUB, MOBI, PDF', price: 2990 },
    prezent: { name: 'Stare małe Dziecko · Tom I – na prezent', sub: 'E-book wysłany e-mailem do obdarowanego', price: 2990 },
    klub: { name: 'Klub Czytelnika · Tom I', sub: 'Tom I teraz, każdy kolejny tom w dniu premiery za 24,90 zł', price: 2490 }
  };
  function zl(gr) { return (gr / 100).toFixed(2).replace('.', ',') + ' zł'; }
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} }
  var cart = load();
  function count() {
    document.querySelectorAll('[data-cart-count]').forEach(function (el) { el.textContent = cart.length; });
  }
  function add(id, meta) {
    if (id !== 'prezent') cart = cart.filter(function (l) { return l.id !== 'tom1' && l.id !== 'klub'; });
    cart.push({ id: id, meta: meta || null });
    save(cart); count();
  }
  count();

  // menu mobilne
  var burger = document.querySelector('.burger'), menu = document.getElementById('menu');
  if (burger && menu) burger.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });

  // przyciski „dodaj do koszyka” na stronie głównej
  document.querySelectorAll('[data-add]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      add(b.getAttribute('data-add'));
      location.href = base + 'koszyk/';
    });
  });

  // formularze zakupu (karta produktu i strona główna)
  document.querySelectorAll('form[data-buy]').forEach(function (buyForm) {
    var gift = buyForm.querySelector('.gift'), priceEl = buyForm.querySelector('[data-price]');
    function sync() {
      var v = buyForm.querySelector('input[name=opcja]:checked').value;
      if (gift) gift.classList.toggle('show', v === 'prezent');
      if (priceEl) priceEl.innerHTML = zl(PRODUCTS[v].price).replace(' zł', ' <small>zł</small>');
    }
    buyForm.addEventListener('change', sync);
    var q = new URLSearchParams(location.search).get('opcja');
    if (q && PRODUCTS[q] && buyForm.querySelector('input[value=' + q + ']')) buyForm.querySelector('input[value=' + q + ']').checked = true;
    sync();
    buyForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = buyForm.querySelector('input[name=opcja]:checked').value, meta = null;
      if (v === 'prezent') {
        if (!gift) { location.href = base + 'tom-1/?opcja=prezent#kup'; return; }
        var em = buyForm.querySelector('[name=g_email]');
        if (!em.value || em.value.indexOf('@') < 1) { em.focus(); buyForm.querySelector('.err').classList.add('show'); return; }
        meta = { email: em.value, kiedy: buyForm.querySelector('[name=g_data]').value, dedykacja: buyForm.querySelector('[name=g_ded]').value };
      }
      add(v, meta);
      location.href = base + 'koszyk/';
    });
  });

  // powiadomienie o kolejnym tomie
  document.querySelectorAll('form[data-ok]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = f.querySelector('input[type=email]');
      if (em && (!em.value || em.value.indexOf('@') < 1)) { em.focus(); return; }
      var ok = document.getElementById(f.getAttribute('data-ok'));
      ok.classList.add('show');
      f.reset();
    });
  });

  // koszyk
  var lines = document.getElementById('cart-lines');
  if (lines) {
    var tpl = document.getElementById('mini-cover').innerHTML;
    function render() {
      var sum = 0, html = '';
      cart.forEach(function (l, i) {
        var p = PRODUCTS[l.id]; if (!p) return;
        sum += p.price;
        var extra = l.meta ? '<span>Dla: ' + esc(l.meta.email) + (l.meta.kiedy ? ', wysyłka ' + esc(l.meta.kiedy) : ', wysyłka od razu') + '</span>' : '';
        html += '<div class="line">' + tpl + '<div><b>' + p.name + '</b><span>' + p.sub + '</span>' + extra +
          '<button class="rm" data-rm="' + i + '">Usuń</button></div><div class="lp">' + zl(p.price) + '</div></div>';
      });
      var has = cart.length > 0;
      lines.innerHTML = has ? html : '<p class="empty">Koszyk jest pusty. <a class="link" href="' + base + 'tom-1/">Zobacz Tom I</a> albo <a class="link" href="' + base + 'czytaj/">przeczytaj początek za darmo</a>.</p>';
      document.getElementById('checkout').hidden = !has;
      document.querySelectorAll('[data-sum]').forEach(function (el) { el.textContent = zl(sum); });
      var netto = Math.round(sum / 1.05);
      document.querySelectorAll('[data-vat]').forEach(function (el) { el.textContent = zl(sum - netto); });
      lines.querySelectorAll('[data-rm]').forEach(function (b) {
        b.addEventListener('click', function () { cart.splice(+b.getAttribute('data-rm'), 1); save(cart); count(); render(); });
      });
    }
    function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    render();
    var fv = document.getElementById('fv'), fvBox = document.getElementById('fv-box');
    fv.addEventListener('change', function () { fvBox.hidden = !fv.checked; });
    document.getElementById('checkout').addEventListener('submit', function (e) {
      e.preventDefault();
      var f = e.target, err = document.getElementById('co-err'), em = f.querySelector('[name=email]');
      var bad = !em.value || em.value.indexOf('@') < 1 || !f.querySelector('[name=reg]').checked || !f.querySelector('[name=cyfrowe]').checked;
      err.classList.toggle('show', bad);
      if (bad) { err.scrollIntoView({ block: 'center' }); return; }
      var pay = f.querySelector('input[name=platnosc]:checked').value;
      document.getElementById('done-mail').textContent = em.value;
      document.getElementById('done-pay').textContent = pay;
      document.getElementById('cart-box').hidden = true;
      var d = document.getElementById('done'); d.classList.add('show');
      cart = []; save(cart); count();
      window.scrollTo(0, 0);
    });
  }

  // czytnik
  var reader = document.getElementById('reader');
  if (reader) {
    var st = { size: 1.18, theme: 'sepia' };
    try { var s = JSON.parse(localStorage.getItem('smd_czytnik')); if (s) st = s; } catch (e) {}
    function apply() {
      reader.style.setProperty('--rs', st.size + 'rem');
      reader.setAttribute('data-theme', st.theme);
      document.querySelectorAll('[data-theme-btn]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-theme-btn') === st.theme); });
      try { localStorage.setItem('smd_czytnik', JSON.stringify(st)); } catch (e) {}
    }
    apply();
    document.querySelectorAll('[data-theme-btn]').forEach(function (b) { b.addEventListener('click', function () { st.theme = b.getAttribute('data-theme-btn'); apply(); }); });
    document.querySelectorAll('[data-size]').forEach(function (b) {
      b.addEventListener('click', function () { st.size = Math.min(1.6, Math.max(0.95, +(st.size + (+b.getAttribute('data-size'))).toFixed(2))); apply(); });
    });
    var sel = document.getElementById('ch');
    sel.addEventListener('change', function () { document.getElementById(sel.value).scrollIntoView(); });
    var bar = document.querySelector('.progress'), secs = reader.querySelectorAll('section[id]');
    function onScroll() {
      var r = reader.getBoundingClientRect(), h = reader.offsetHeight - innerHeight;
      bar.style.width = Math.max(0, Math.min(100, -r.top / h * 100)) + '%';
      var cur = secs[0];
      secs.forEach(function (s) { if (s.getBoundingClientRect().top < 140) cur = s; });
      if (cur && sel.value !== cur.id) sel.value = cur.id;
    }
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

})();
