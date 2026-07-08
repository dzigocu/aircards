// Removed invalid RapidAPI stub. This page loads cards from the local API instead.
// Fetch cards from local API and render into the page
fetch('/api/cards', { method: 'GET' })
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status} ${response.statusText}`);
    return response.json();
  })
  .then(cards => {
    const container = document.getElementById('cards');
    if (!container) return console.warn('Cards container not found');
    container.innerHTML = '';
    cards.forEach(card => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `<h3>${card.name}</h3><p>Price: ${card.price}</p>`;
      container.appendChild(el);
    });
  })
  .catch(err => {
    console.error('Failed to load cards:', err);
  });

// Wire up fetch-from-URL UI
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('fetchBtn');
  const input = document.getElementById('sourceUrl');
  const status = document.getElementById('fetchStatus');
  if (!btn || !input) return;
  btn.addEventListener('click', () => {
    const url = input.value.trim();
    if (!url) return;
    status.textContent = 'loading...';
    fetch(`/api/fetch_cards?url=${encodeURIComponent(url)}`)
      .then(r => r.json())
      .then(data => {
        status.textContent = '';
        if (data.error) return console.error(data.error);
        const container = document.getElementById('cards');
        container.innerHTML = '';
        data.forEach(card => {
          const el = document.createElement('div');
          el.className = 'card';
          el.innerHTML = `<h3>${card.name}</h3><p>Price: ${card.price}</p>`;
          container.appendChild(el);
        });
      })
      .catch(err => {
        status.textContent = 'failed';
        console.error(err);
      });
  });
});