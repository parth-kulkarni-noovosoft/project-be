from flask import Flask, render_template, request, jsonify
import json
import sys
sys.path.append('..')
from extractors.main import fetch_data
from util.sentimentAnalysis import load_sentiwordnet, update_date_with_polarity
from model.nb import predict, load_model

app = Flask(__name__)
load_sentiwordnet()
load_model()

url_data = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-results', methods=['POST'])
def get_results():
    data = request.json
    url = data.get('url', '')
    if url is None or url == '':
        return jsonify({ 'error': 'No URL provided' }), 400
    try:
        if (url in url_data):
            results = url_data[url]
        else:
            results = fetch_data(url)
            url_data[url] = results
        data_with_sentiment = update_date_with_polarity(results.get('reviews', []))
        return jsonify(predict(data_with_sentiment)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
