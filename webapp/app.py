from flask import Flask, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import json 

def generate():
    while True:
        # Process a chunk of EEG data and get a prediction
        # data = process_eeg_data()
        # prediction = make_prediction(data)

        data = "hello"
        prediction = "world"

        # Send the processed data and prediction as an SSE message
        yield json.dumps(f"data: {data}, {prediction}\n\n")

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='text/event-stream')
