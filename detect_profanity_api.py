from flask import Flask, request, jsonify
from profanity_check import predict
import os

app = Flask(__name__)


@app.route('/detect', methods=['POST'])
def detect_words():
    try:
        # Get the text from the request JSON
        data = request.get_json()
        text = data.get('text')

        if not text:
            return jsonify({'error': 'Missing text in request JSON'}), 400

        # Detect profanity in the text
        profanity_score = predict([text])[0]

        # Determine whether the text contains profanity
        contains_profanity = profanity_score > 0.5

        # Censor the text if it contains profanity
        if contains_profanity:
            # Replace profanity with asterisks
            censored_text = text
            for word in text.split():
                if predict([word])[0] > 0.5:
                    censored_text = censored_text.replace(word, '*' * len(word))

        else:
            censored_text = text

        # Prepare the response JSON object
        response_data = {
            'text': censored_text,
            'contains_profanity': contains_profanity
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=True)
