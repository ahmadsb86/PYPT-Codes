

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from sklearn.decomposition import FastICA

# Load the WAV file
file_path = 'audio.wav'  # replace with your file path
sampling_rate, data = wavfile.read(file_path)

# If stereo (2 channels), convert to mono by averaging the channels
if len(data.shape) == 2:
    data = data.mean(axis=1)

# Standardize the data (important for ICA)
data_standardized = (data - np.mean(data)) / np.std(data)

# Reshape data to 2D for ICA
data_reshaped = data_standardized.reshape(-1, 1)  # n_samples, n_features

# Apply ICA
ica = FastICA(n_components=4)
components = ica.fit_transform(data_reshaped)  # ICA components

# Plot the 4 most significant components
plt.figure(figsize=(10, 6))

for i in range(4):
    plt.subplot(4, 1, i+1)
    plt.plot(components[:, i])
    plt.title(f'Independent Component {i+1}')
    plt.tight_layout()

# Show the plots
plt.show()
