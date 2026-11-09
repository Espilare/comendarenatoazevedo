(() => {
  const invitation = document.getElementById('invitation');
  const tribute = document.getElementById('tribute');
  const button = document.getElementById('open-invitation');
  const title = document.getElementById('title');
  if (!invitation || !tribute || !button || !title) return;

  // Without JavaScript the complete letter remains available.
  tribute.hidden = true;
  invitation.hidden = false;
  invitation.addEventListener('click', () => {
    button.disabled = true;
    invitation.classList.add('is-opening');
    const reveal = () => {
      invitation.hidden = true;
      tribute.hidden = false;
      tribute.classList.add('tribute-revealed');
      title.tabIndex = -1;
      window.scrollTo({ top: 0, behavior: 'instant' });
      title.focus({ preventScroll: true });
    };
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) reveal();
    else window.setTimeout(reveal, 650);
  }, { once: true });
})();
