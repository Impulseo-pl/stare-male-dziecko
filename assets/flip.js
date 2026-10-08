(function () {
  var el = document.getElementById('flipbook');
  if (!el || !window.St) return;
  var book = new St.PageFlip(el, {
    width: 495, height: 703, size: 'stretch',
    minWidth: 260, maxWidth: 440, minHeight: 370, maxHeight: 625,
    showCover: true, usePortrait: true, mobileScrollSupport: true,
    maxShadowOpacity: 0.45, flippingTime: 900
  });
  book.loadFromHTML(el.querySelectorAll('.fpage'));
  var cnt = document.getElementById('flip-count'), total = book.getPageCount();
  function upd() { cnt.textContent = 'Strona ' + (book.getCurrentPageIndex() + 1) + ' z ' + total; }
  book.on('flip', upd); upd();
  document.getElementById('flip-prev').addEventListener('click', function () { book.flipPrev(); });
  document.getElementById('flip-next').addEventListener('click', function () { book.flipNext(); });
  document.addEventListener('keydown', function (e) {
    var r = el.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    if (e.key === 'ArrowRight') book.flipNext();
    if (e.key === 'ArrowLeft') book.flipPrev();
  });
})();
