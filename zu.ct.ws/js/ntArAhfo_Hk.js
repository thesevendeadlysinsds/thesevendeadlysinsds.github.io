function loadTurnstile() {
    const container = document.getElementById('turnstile-container');
    const siteKey = '0x4AAAAAAA4UmNngQZwXxNEN'; 
    container.innerHTML = '';
    if (window.innerWidth < 350) {
        container.innerHTML = `<div class="cf-turnstile" data-sitekey="${siteKey}" data-size="compact"></div>`;
    } else {
        container.innerHTML = `<div class="cf-turnstile" data-sitekey="${siteKey}"></div>`;
    }
    if (typeof Turnstile !== 'undefined') {
        Turnstile.render();
    }
}
loadTurnstile();
window.addEventListener('resize', () => {
    var gyiuop = document.querySelector('button[x="x"]');
    gyiuop.style.display = 'block';
});
