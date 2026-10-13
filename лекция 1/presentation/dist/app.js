const slides = [...document.querySelectorAll('.slide')];
const dots = [...document.querySelectorAll('.dot')];
let current = 0;

function show(index, updateHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, i) => { slide.hidden = i !== current; });
  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === current);
    if (i === current) dot.setAttribute('aria-current', 'step');
    else dot.removeAttribute('aria-current');
  });
  const number = value => String(value).padStart(2, '0');
  document.getElementById('counter').textContent = `${number(current + 1)} / ${number(slides.length)}`;
  document.getElementById('progress').style.width = `${(current + 1) / slides.length * 100}%`;
  if (updateHash) history.replaceState(null, '', `#${current + 1}`);
  window.scrollTo(0, 0);
}
function readHash() {
  const index = Number(location.hash.slice(1));
  show(Number.isInteger(index) && index >= 1 && index <= slides.length ? index - 1 : 0, false);
}
dots.forEach((dot, i) => dot.addEventListener('click', () => show(i)));
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest('input,textarea,select,[contenteditable="true"]')) return;
  if (['ArrowRight', 'PageDown'].includes(event.key) || (event.key === ' ' && !event.target.closest('button,a'))) {
    event.preventDefault(); show(current + 1);
  }
  if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); show(current - 1); }
  if (event.key === 'Home') { event.preventDefault(); show(0); }
  if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
  if (event.key.toLowerCase() === 'f') toggleFullscreen();
});
async function toggleFullscreen() {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
  } catch { /* Fullscreen remains available through the browser menu. */ }
}
window.addEventListener('hashchange', readHash);
readHash();

// OBS browser source follows the private speaker controller on the local server.
if (new URLSearchParams(location.search).get('obs') === '1') {
  let polling = false;
  const sync = async () => {
    if (polling) return;
    polling = true;
    try {
      const response = await fetch('/presenter-state', {cache: 'no-store'});
      if (!response.ok) return;
      const state = await response.json();
      if (Number.isInteger(state.slide) && state.slide !== current) show(state.slide);
    } catch { /* Keep the current slide if the controller is unavailable. */ }
    finally { polling = false; }
  };
  sync();
  setInterval(sync, 300);
}
