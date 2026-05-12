(function () {
  'use strict';

  // Auto-translates Chinese phrases inside achievement <li>s.
  function autoTranslate(html) {
    let s = html;

    // Punctuation
    s = s.replace(/、/g, ' · ');
    s = s.replace(/（/g, ' (').replace(/）/g, ')');

    // Multi-char proper nouns / phrases (run first, longest first)
    const phrases = [
      ['南加州青少年发展锦标赛', 'SoCal Junior Development Championship'],
      ['美国全国青少年锦标赛', 'USA Junior Nationals'],
      ['青少年国际锦标赛', 'Junior International Championship'],
      ['青少年锦标赛', 'Junior Championship'],
      ['第九届 H-Mart 锦标赛', '9th H-Mart Championship'],
      ['第九届', '9th'],
      ['锦标赛', 'Championship'],
      ['(波士顿)', '(Boston)'],
      ['西雅图', 'Seattle'],
      ['北加', 'NorCal'],
      ['全部 第1', 'all 1st'],
    ];
    for (const [zh, en] of phrases) {
      if (s.indexOf(zh) !== -1) s = s.split(zh).join(en);
    }

    // Event categories
    const events = [
      ['男单附加赛', "Men's Singles Consolation"],
      ['男双附加赛', "Men's Doubles Consolation"],
      ['女单附加赛', "Women's Singles Consolation"],
      ['女双附加赛', "Women's Doubles Consolation"],
      ['混双附加赛', 'Mixed Doubles Consolation'],
      ['男单', "Men's Singles"],
      ['女单', "Women's Singles"],
      ['男双', "Men's Doubles"],
      ['女双', "Women's Doubles"],
      ['混双', 'Mixed Doubles'],
    ];
    for (const [zh, en] of events) {
      s = s.split(zh).join(' ' + en + ' ');
    }

    // Medal / placement words
    const placements = [
      ['冠军', 'Champion'],
      ['亚军', 'Runner-up'],
      ['季军', '2nd Runner-up'],
      ['金牌', 'Gold'],
      ['银牌', 'Silver'],
      ['铜牌', 'Bronze'],
      ['前八', 'Top 8'],
      ['8强', 'Top 8'],
      ['16强', 'Top 16'],
    ];
    for (const [zh, en] of placements) {
      s = s.split(zh).join(' ' + en + ' ');
    }

    // Ordinals
    s = s.replace(/第\s*([1-9])\s*名/g, ' $1 ');
    s = s.replace(/第一/g, ' 1st ').replace(/第二/g, ' 2nd ').replace(/第三/g, ' 3rd ')
         .replace(/第四/g, ' 4th ').replace(/第五/g, ' 5th ');
    s = s.replace(/第\s*1/g, ' 1st ').replace(/第\s*2/g, ' 2nd ')
         .replace(/第\s*3/g, ' 3rd ').replace(/第\s*4/g, ' 4th ');

    // Group designations (E组, D组, C组, etc.)
    s = s.replace(/([A-Z])组/g, '$1 Group');
    s = s.replace(/组/g, ' Group ');

    s = s.replace(/名/g, '');
    s = s.replace(/与/g, ' & ');

    // Tidy spaces and stray separators
    s = s.replace(/\s*·\s*/g, ' · ');
    s = s.replace(/[ \u3000]{2,}/g, ' ');
    s = s.replace(/\s+\)/g, ')').replace(/\(\s+/g, '(');
    s = s.replace(/·\s*·/g, '·');
    s = s.trim();

    return s;
  }

  function snapshot() {
    document.querySelectorAll('[data-en]').forEach((el) => {
      if (!el.hasAttribute('data-zh')) {
        el.setAttribute('data-zh', el.innerHTML);
      }
    });
    document.querySelectorAll('.achievements li').forEach((el) => {
      if (!el.hasAttribute('data-zh')) {
        el.setAttribute('data-zh', el.innerHTML);
        el.setAttribute('data-en-auto', autoTranslate(el.innerHTML));
      }
    });
  }

  function apply(lang) {
    document.querySelectorAll('[data-en]').forEach((el) => {
      el.innerHTML = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-zh');
    });
    document.querySelectorAll('.achievements li').forEach((el) => {
      el.innerHTML = lang === 'en' ? el.getAttribute('data-en-auto') : el.getAttribute('data-zh');
    });
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    const btn = document.getElementById('lang-toggle');
    if (btn) btn.textContent = lang === 'en' ? '中' : 'EN';
    try { localStorage.setItem('wzq.lang', lang); } catch (e) {}
  }

  function init() {
    snapshot();
    let lang = 'zh';
    try { lang = localStorage.getItem('wzq.lang') || 'zh'; } catch (e) {}
    const btn = document.getElementById('lang-toggle');
    if (btn) {
      btn.addEventListener('click', () => {
        const cur = document.documentElement.lang === 'en' ? 'en' : 'zh';
        apply(cur === 'en' ? 'zh' : 'en');
      });
    }
    apply(lang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
