from flask import Flask, request, jsonify, render_template
import requests
from flask_swagger_ui import get_swaggerui_blueprint
import json
import string
from trie import Trie

app = Flask(__name__)

SWAGGER_URL = '/docs'
API_URL = '/static/openapi.yaml'  
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Flask Emoji API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

trie = Trie()
trie.load_from_json('./static/emojis.json')

@app.route('/')
def home():
    return render_template('index.html')


def get_predictions(text):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator).lower()
    return " ".join(trie.search(str(text)))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.data.decode('utf-8')
    predictions = get_predictions(data)
    return predictions

@app.route('/integrate', methods=['GET'])
def integrate():
    return render_template('integrate.html')
    

@app.route('/send', methods=['POST'])
def to_discord():
    data = request.json
    config = data.get('config', {})
    content = data.get('telex_content', {})

    channels = config['channels']
    message = content['message']

    emoji_message = get_predictions(message)

    for chan in channels:
        webhook_url = chan['webhook_url']
        requests.post(webhook_url, json={"content": emoji_message})

    return jsonify({"status": "Messages sent"})

if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0')