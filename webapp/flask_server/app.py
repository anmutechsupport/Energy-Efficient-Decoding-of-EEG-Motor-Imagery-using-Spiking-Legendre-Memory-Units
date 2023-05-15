from flask import Flask, Response, request, jsonify, session
from flask_cors import CORS, cross_origin
import json 
from helpers import *
import os 
import tempfile

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

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
    epochs, labels, fs = preprocess(file.read())
    epochs_data = epochs.get_data()
    # epochs_data = {'test': 'test'}
    # predictions = make_prediction(data)
    print(epochs_data.shape)
    print(labels.shape)
    # merged_epochs = np.moveaxis(epochs_data, 1, 0).reshape(epochs_data.shape[1], -1)
    # print(merged_epochs.shape)
    transformed_epochs = np.array([csp_transform(epoch) for epoch in epochs_data])
    print(transformed_epochs.shape)

    M, S, K = init_params(transformed_epochs, fs)
    stft_data, f, t = spectro_data(transformed_epochs, fs, M, S)
    # combined_data = [stft_data, f, t]
    # np.save('mock_data.npy', stft_data)
    # with open('arrays.pkl', 'wb') as file:
    #     pickle.dump(combined_data, file)

     # Store data in a temporary file
    # with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as temp_file:
    #     temp_filename = temp_file.name
    #     np.save(temp_file, stft_data)

    #     # Save the temporary file path in the session
    #     session['data_file'] = temp_filename
    preds = inference(stft_data, f)
    
    response = {
        # 'epochs_data': merged_epochs.tolist(),
        'epochs_transformed': transformed_epochs.tolist(),
        'stft_data': stft_data.tolist(),
        'true_labels': labels.tolist(),
        'pred_labels': preds.tolist()
    }
    
    return jsonify(response)
    # return jsonify({"hit": "hit"})

@app.route('/spectro', methods=['POST'])
def spectro():
    # Get the temporary file path from the session
    # data_file = session['data_file']

    # if data_file is None:
    #     return 'No data', 400
    sampleIdx = request.json['sampleIdx']

    # Load the data
    data = np.load('mock_data.npy')
    meanSample = np.mean(data[sampleIdx], axis=0)
    print(meanSample.shape)

    # Create the plot
    plot_url = spectro_gen(meanSample)

    # Return the plot data
    return jsonify(plot_url)

