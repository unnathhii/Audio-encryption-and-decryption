from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
import pyaudio
import wave
import os

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
AES_KEY_SIZE = 32  

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return private_key, public_key

def encrypt_audio(audio_data, key):
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(audio_data) + encryptor.finalize()

    return iv + encrypted_data

def decrypt_audio(encrypted_data, key):
    iv = encrypted_data[:16]
    data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    return decrypted_data

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("* Recording audio...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)

def save_audio(filename, audio_data):
    desktop_path=os.path.join(os.path.expanduser("~"), "Desktop", filename)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)
        print(f"File saved at: {desktop_path}")

if __name__ == "__main__":
    # Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair()

    # Generate a random symmetric key for AES
    audio_key = os.urandom(AES_KEY_SIZE)

    # Record audio
    audio_data = record_audio()

    # Encrypt audio data using AES
    encrypted_audio_data = encrypt_audio(audio_data, audio_key)

    # Save encrypted audio to a WAV file
    save_audio("encrypted_audio.wav", encrypted_audio_data)

    print("Encrypted audio saved to 'encrypted_audio.wav'")

    # Decrypt audio data using AES
    decrypted_audio_data = decrypt_audio(encrypted_audio_data, audio_key)

    # Save decrypted audio to a WAV file
    save_audio("decrypted_audio.wav", decrypted_audio_data)

    print("Decrypted audio saved to 'decrypted_audio.wav'")
