from flask import Flask, request, jsonify, send_from_directory
import anthropic
import os

app = Flask(__name__, static_folder='static')
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt'}), 400

        message = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=4000,
            messages=[{'role': 'user', 'content': data['prompt']}]
        )
        return jsonify({'text': message.content[0].text})

    except anthropic.AuthenticationError:
        return jsonify({'error': 'Invalid API key — check your ANTHROPIC_API_KEY env variable'}), 401
    except anthropic.RateLimitError:
        return jsonify({'error': 'Rate limit hit — please wait and try again'}), 429
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
