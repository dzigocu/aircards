from flask import Flask, jsonify, render_template, send_from_directory, request
import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'ok',
        'message': 'API работает',
    })

@app.route('/api/cards')
def api_cards():
    cards = [
        {
            'id': 1,
            'airline': 'Aeroflot',
            'route': 'MOW → LED',
            'depart': '2026-07-10 08:30',
            'arrive': '2026-07-10 10:00',
            'duration': '1h 30m',
            'price': '6,500 ₽'
        },
        {
            'id': 2,
            'airline': 'S7 Airlines',
            'route': 'MOW → VKO',
            'depart': '2026-07-11 12:20',
            'arrive': '2026-07-11 14:15',
            'duration': '1h 55m',
            'price': '7,200 ₽'
        },
        {
            'id': 3,
            'airline': 'Pobeda',
            'route': 'MOW → KUF',
            'depart': '2026-07-12 06:15',
            'arrive': '2026-07-12 08:05',
            'duration': '1h 50m',
            'price': '4,980 ₽'
        },
    ]
    return jsonify(cards)


@app.route('/api/fetch_cards')
def api_fetch_cards():
    """Fetch and heuristically extract card-like items from a provided URL.
    Usage: /api/fetch_cards?url=https://example.com/page
    """
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url parameter'}), 400
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'http://' + url
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        items = []
        # First try: elements with class names that suggest listings
        candidates = soup.find_all(class_=lambda x: x and any(k in x.lower() for k in ['card', 'ticket', 'offer', 'flight', 'fare', 'result', 'item']))

        if not candidates:
            # Fallback: search for price-like patterns in text
            text = soup.get_text(separator='\n')
            prices = re.findall(r'\d{1,3}(?:[ ,\.\u00A0]\d{3})*(?:[\.,]\d{2})?\s*(?:USD|EUR|RUB|R\$|\$|€|₽)?', text)
            for i, p in enumerate(prices[:20]):
                items.append({'id': i + 1, 'name': 'Result', 'price': p.strip()})
        else:
            for idx, el in enumerate(candidates[:50]):
                text = el.get_text(separator=' ', strip=True)
                # try to extract a price inside this element
                price_match = re.search(r'\d[\d\.,\s]*\d', text)
                price = price_match.group(0).strip() if price_match else ''
                name = text[:200]
                items.append({'id': idx + 1, 'name': name, 'price': price})

        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:filename>')
def static_files(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return 'Файл не найден', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
 