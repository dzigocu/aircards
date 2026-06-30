function renderCards(cards) {
  var container = document.getElementById('cards');
  if (!container) return;

  // очистить старое содержимое
  container.innerHTML = '';

  if (!cards || cards.length === 0) {
    var emptyText = document.createElement('p');
    emptyText.textContent = 'No cards available.';
    container.appendChild(emptyText);
    return;
  }

  for (var i = 0; i < cards.length; i++) {
    var card = cards[i];

    var cardBlock = document.createElement('div');
    cardBlock.className = 'card';

    var title = document.createElement('h3');
    title.textContent = card.name;

    var price = document.createElement('p');
    price.textContent = 'Price: $' + card.price;

    cardBlock.appendChild(title);
    cardBlock.appendChild(price);
    container.appendChild(cardBlock);
  }
}

function fetchCards() {
  fetch('/api/cards')
    .then(function (response) {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(function (data) {
      renderCards(data);
    })
    .catch(function (error) {
      console.error('Failed to load cards:', error);
      var container = document.getElementById('cards');
      if (container) {
        container.innerHTML = '<p>Error loading cards.</p>';
      }
    });
}

document.addEventListener('DOMContentLoaded', fetchCards);

