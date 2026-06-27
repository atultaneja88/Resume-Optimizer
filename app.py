from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static')
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt'}), 400

        response = model.generate_content(data['prompt'])
        return jsonify({'text': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
