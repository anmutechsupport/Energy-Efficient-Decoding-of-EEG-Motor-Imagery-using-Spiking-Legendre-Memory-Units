from mne import Epochs, pick_types, events_from_annotations, EpochsArray, create_info
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
from mne.time_frequency import psd_array_welch, psd_array_multitaper, stft
import numpy as np 
import pandas as pd 
import tempfile
import scipy.signal as signal
import io, base64, os
import matplotlib.pyplot as plt
plt.switch_backend('Agg') 

csp_filters = np.load('/Users/anushmutyala/Documents/GitHub/Energy-Efficient-Decoding-of-EEG-Motor-Imagery-using-Spiking-Legendre-Memory-Units/ml/preprocessed_data/csp_filters.npy')

def preprocess(file):
    with tempfile.NamedTemporaryFile(suffix=".edf", delete=True) as temp:
        temp.write(file)
        temp.flush()  # Ensure all data is written
      
        event_id = dict(hands=2, feet=3)
        tmin, tmax = -1., 4.
        raw = read_raw_edf(temp.name, preload=True)
        eegbci.standardize(raw)  # set channel names
        montage = make_standard_montage('standard_1005')
        raw.set_montage(montage)
        raw.filter(8., 30., fir_design='firwin', skip_by_annotation='edge') # sensorimotor rhythms

        events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))

        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                        exclude='bads')

        # Read epochs 
        epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                        baseline=None, preload=True)
        labels = epochs.events[:, -1] - 2
        fs = raw.info['sfreq']
    return epochs, labels, fs 

def csp_transform(epochs_data, filter_len=4):
    return np.dot(csp_filters.T[:4], epochs_data)

# def csp_timeseries_plot(epochs_transformed):

#     return
def init_params(data, fs):
    # init params
    N = len(data[0][0]) # length of the signal
    fmin = 2
    fmax = 30
    print('sampling rate', fs)
    M = int((2/fmin)*fs) # window length long enough to cover at least 2 cycles of the lowest frequency of interest
    print('window size', M)
    S = M//2 # window step. 50% overlap is standard
    print('window step', S)
    print('overlap' , (1 - S/M))
    K = (N-M)//S + 1 # number of segments
    print('number of segments', K)
    return M, S, K

def spectro_gen(source_stft):
    # restrict spectrogram to 8-30 Hz
    nf = f[(f >= 8) & (f <= 30)]
    source_stft = source_stft[(f >= 8) & (f <= 30), :]
    plt.figure(figsize=(10, 5))
    plt.title('STFT Magnitude, 1 second interval, 50% Overlap')
    plt.pcolormesh(t, nf, source_stft, cmap='jet')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def spectro_data(epochs_transformed, fs, M, S):
    source_stft = []
    global f, t
    for epoch in epochs_transformed:
        norm_epoch = epoch - np.mean(epoch) # remove DC offset
        w = np.hanning(M)
        s_w = np.sum(w**2)
        f, t, Sxx = signal.spectrogram(
        norm_epoch,                  # Provide the signal,
        window=w,               # ... the window,
        fs=fs,                # ... the sampling frequency,
        nperseg=M,     # ... the length of a segment,
        noverlap=S)     # ... the number of samples to overlap,
        norm_Sxx = 10 * np.log10(Sxx/s_w) 
        source_stft.append(norm_Sxx)

    source_stft = np.array(source_stft)
    # print(source_stft.shape)
    return source_stft, f, t

