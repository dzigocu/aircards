from flask import Flask, jsonify, render_template, send_from_directory
import os

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
        {'id': 1, 'name': 'Aircard A', 'price': 100},
        {'id': 2, 'name': 'Aircard B', 'price': 200},
        {'id': 3, 'name': 'Aircard C', 'price': 300},
    ]
    return jsonify(cards)

@app.route('/<path:filename>')
def static_files(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return 'Файл не найден', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
 