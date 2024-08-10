import numpy as np
from scipy.io import wavfile

# Generate chaotic sequence using logistic map
def logistic_map(x, r):
    return r * x * (1 - x)

# Encryption function
def encrypt_audio(input_file, output_file, r, intensity):
    # Read audio file
    fs, audio_data = wavfile.read(input_file)
    
    # Flatten the audio data
    audio_data_flattened = audio_data.flatten()
    
    # Generate chaotic sequence
    chaotic_sequence = np.zeros(len(audio_data_flattened))
    x = 0.5  # Initial value of logistic map
    for i in range(len(audio_data_flattened)):
        x = logistic_map(x, r)
        chaotic_sequence[i] = x
    
    # Apply XOR operation with adjusted intensity
    encrypted_data = np.bitwise_xor(audio_data_flattened, (intensity * chaotic_sequence * 32767).astype(np.int16))
    
    # Reshape encrypted data
    encrypted_audio = encrypted_data.reshape(audio_data.shape)
    
    # Write encrypted audio to file
    wavfile.write(output_file, fs, encrypted_audio)

# Test encryption
if __name__ == "__main__":
    input_audio = input("Enter the path to the input .wav file: ")
    output_audio = input("Enter the path to save the encrypted .wav file: ")
    r = 3.8  # Control parameter for logistic map
    intensity = 8  # Adjust intensity here
    
    # Encrypt the audio
    encrypt_audio(input_audio, output_audio, r, intensity)
