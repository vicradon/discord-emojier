from flask import Flask, request, jsonify, render_template
import requests
from transformers import pipeline

pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emoji")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def get_predictions(text):
    text_parts = text.split(".")
    predictions = pipe(text_parts)
    sorted_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)
    return " ".join([pred['label'] for pred in sorted_predictions])

@app.route('/predict', methods=['POST'])
def predict():
    data = str(request.data)
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