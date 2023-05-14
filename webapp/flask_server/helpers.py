from mne import Epochs, pick_types, events_from_annotations, EpochsArray, create_info
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
from mne.time_frequency import psd_array_welch, psd_array_multitaper, stft
import numpy as np 
import pandas as pd 
import tempfile

csp_filters = np.load('../../ml/preprocessed_data/csp_filters.npy')

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
        epochs_data = epochs.get_data()
    return epochs_data, labels 

def csp_transform(epochs_data, filter_len=4):
    return np.dot(csp_filters.T[:4], epochs_data)

# def csp_timeseries_plot(epochs_transformed):

#     return

def spectro_gen(epochs_transformed):
    source_stft = []

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
    print(source_stft.shape)

