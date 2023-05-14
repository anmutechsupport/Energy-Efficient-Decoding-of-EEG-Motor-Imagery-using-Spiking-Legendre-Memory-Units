from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json 
from helpers import *

app = Flask(__name__)
CORS(app)

@app.before_first_request
def startup():
    global raw_bytes 
    global epochs_data
    global epochs_transformed

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    print(file)
    epochs_data, labels = preprocess(file.read())
    # epochs_data = {'test': 'test'}
    # predictions = make_prediction(data)
    print(epochs_data.shape)
    print(labels.shape)
    
    response = {
        'epochs_data': epochs_data.tolist(),
        'labels': labels.tolist(),
    }
    
    return jsonify(response)
    # return jsonify({"hit": "hit"})

