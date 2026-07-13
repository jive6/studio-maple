/* ============================================================
   site.js ― Studio Maple demo
   ① 流入経路（?src=）を保持して、問い合わせ導線に引き継ぐ
   ② 固定バナーの高さぶんだけ body の下余白を確保する
   ③ 応募フォームの擬似送信（完了画面の表示）
   ============================================================ */
(function () {
  'use strict';

  /* ---------- ① 流入経路の保持 ---------- */
  var KEY = 'sm_src';
  var q = new URLSearchParams(location.search).get('src');
  if (q) { try { sessionStorage.setItem(KEY, q); } catch (e) {} }

  var src = q;
  if (!src) { try { src = sessionStorage.getItem(KEY); } catch (e) {} }
  if (!src) src = 'direct';

  // サイト内リンクに src を引き継ぐ（回遊しても経路が消えない）
  document.querySelectorAll('a[href$=".html"]').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href || href.indexOf('//') === 0 || /^https?:/i.test(href)) return;
    var u = new URL(href, location.href);
    u.searchParams.set('src', src);
    a.setAttribute('href', u.pathname.split('/').pop() + u.search + u.hash);
  });

  // 外部リンク（studiomaple.jp）に src を付与
  document.querySelectorAll('a[href*="studiomaple.jp"]').forEach(function (a) {
    try {
      var u = new URL(a.href);
      u.searchParams.set('src', src);
      a.href = u.toString();
    } catch (e) {}
  });

  // mailto の本文に経路を埋め込む（＝届いたメールを見れば経路がわかる）
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
    var sep = a.getAttribute('href').indexOf('?') > -1 ? '&' : '?';
    a.setAttribute('href', a.getAttribute('href') + sep +
      'body=' + encodeURIComponent('\n\n----------\n参照元：' + src + '（自動付与）'));
  });

  // GA4 を入れる場合はここで送る
  // if (window.gtag) gtag('event', 'demo_view', { src: src });

  /* ---------- ② 固定バナーの高さを body に反映 ---------- */
  var banner = document.querySelector('.sample-banner');
  if (banner) {
    document.body.classList.add('has-banner');
    var sync = function () {
      document.body.style.setProperty('--banner-h', banner.offsetHeight + 8 + 'px');
    };
    sync();
    window.addEventListener('resize', sync);
    if (window.ResizeObserver) new ResizeObserver(sync).observe(banner);
  }

  /* ---------- ③ 応募フォームの擬似送信 ---------- */
  var form = document.getElementById('entryForm');
  var thanks = document.getElementById('thanks');
  if (form && thanks) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();          // 実送信はしない（required でブラウザが先に検証する）
      form.hidden = true;
      thanks.hidden = false;
      thanks.scrollIntoView({ block: 'center', behavior: 'smooth' });
      thanks.focus();
    });
    var again = document.getElementById('reAgain');
    if (again) {
      again.addEventListener('click', function () {
        thanks.hidden = true;
        form.hidden = false;
        form.reset();
        form.scrollIntoView({ block: 'center', behavior: 'smooth' });
      });
    }
  }
})();
