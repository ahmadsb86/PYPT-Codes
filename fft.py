
import ffmpeg
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Extract audio from MP4 using ffmpeg
def extract_audio_from_mp4(mp4_file, audio_file="audio.wav"):
    ffmpeg.input(mp4_file).output(audio_file).run()

# Step 2: Load audio using librosa
def load_audio(audio_file):
    y, sr = librosa.load(audio_file, sr=None)  # y: audio signal, sr: sample rate
    return y, sr

# Step 3: Find dominant frequencies
def find_dominant_frequencies(y, sr, n_top=100):
    # Perform Short-Time Fourier Transform (STFT)
    S = np.abs(librosa.stft(y))
    frequencies = librosa.fft_frequencies(sr=sr)

    # Average the power spectrum over time
    power_spectrum = np.mean(S, axis=1)

    # Find the indices of the top n_top frequencies
    top_indices = np.argsort(power_spectrum)[-n_top:][::-1]
    dominant_frequencies = frequencies[top_indices]
    amplitudes = power_spectrum[top_indices]

    return dominant_frequencies, amplitudes

# Step 4: Plot the dominant frequencies
def plot_dominant_frequencies(frequencies, amplitudes):
    plt.figure(figsize=(8, 6))
    plt.bar(frequencies, amplitudes, color="skyblue")
    plt.title("Dominant Frequencies")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

# Main process
mp4_file = "input2.mp4"  # Replace with your MP4 file path
audio_file = "audio.wav"

# Extract audio from MP4
extract_audio_from_mp4(mp4_file, audio_file)

# Load the extracted audio
y, sr = load_audio(audio_file)

# Find the dominant frequencies
n_top = 5  # Number of top frequencies to find
dominant_frequencies, amplitudes = find_dominant_frequencies(y, sr, n_top=n_top)

# Print the dominant frequencies
print("Dominant Frequencies (Hz):", dominant_frequencies)
print("Amplitudes:", amplitudes)

# Plot the dominant frequencies
plot_dominant_frequencies(dominant_frequencies, amplitudes)
