from flask import Flask, jsonify, request
import random

app = Flask(__name__)

jokes = [
    {"question": "Why don’t scientists trust atoms?", "options": ["They make up everything", "They split all the time", "They're too small"], "answer": "They make up everything"},
    {"question": "What do you get when you cross a snowman and a vampire?", "options": ["Frostbite", "Cold blood", "Ice spikes"], "answer": "Frostbite"},
    # Add more jokes here
]

@app.route('/get_joke', methods=['GET'])
def get_joke():
    joke = random.choice(jokes)
    return jsonify(joke)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    if data['answer'] == jokes[data['joke_id']]['answer']:
        return jsonify({"correct": True})
    return jsonify({"correct": False})

if __name__ == '__main__':
    app.run(debug=True)
