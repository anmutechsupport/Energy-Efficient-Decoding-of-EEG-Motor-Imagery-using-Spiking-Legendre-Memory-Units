from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
import json 
from helpers import *

app = Flask(__name__)
CORS(app)

# @app.before_first_request
# def startup():
#     # global raw_bytes 
#     # global epochs_data
#     # global epochs_transformed
#     return

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
    merged_epochs = np.moveaxis(epochs_data, 1, 0).reshape(epochs_data.shape[1], -1)
    print(merged_epochs.shape)
    transformed_epochs = np.array([csp_transform(epoch) for epoch in epochs_data])
    print(transformed_epochs.shape)
    init_params(epochs_data)
    
    response = {
        'epochs_data': merged_epochs.tolist(),
        'epochs_transformed': transformed_epochs.tolist()[:2],
        'labels': labels.tolist(),
    }
    
    return jsonify(response)
    # return jsonify({"hit": "hit"})

