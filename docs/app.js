'use strict';
(() => {
  const languageButton = document.getElementById('language');
  let language = 'en';
  const setLanguage = (next) => {
    language = next;
    document.documentElement.lang = next === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en][data-zh]').forEach((el) => {
      el.textContent = el.dataset[next];
    });
    document.querySelectorAll('[data-language]').forEach((el) => {
      el.hidden = el.dataset.language !== next;
    });
    languageButton.textContent = next === 'zh' ? 'EN' : '中文';
    languageButton.setAttribute('aria-label', next === 'zh' ? 'Switch to English' : '切换为中文');
    document.title = document.getElementById('name').textContent + (next === 'zh' ? ' | 具身智能研究' : ' | Embodied Intelligence');
    try { localStorage.setItem('homepage-language', next); } catch (_) {}
  };
  languageButton.addEventListener('click', () => setLanguage(language === 'en' ? 'zh' : 'en'));
  try { if (localStorage.getItem('homepage-language') === 'zh') setLanguage('zh'); } catch (_) {}
})();
