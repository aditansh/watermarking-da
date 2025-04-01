import os
import numpy as np
import wave

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def embed_echo_hiding(audio_path, binary_msg, output_path, d0=150, d1=200, alpha=0.3):    
    # Read source audio
    with wave.open(audio_path, 'rb') as wav:
        params = wav.getparams()
        frames = np.frombuffer(wav.readframes(-1), dtype=np.int16)
    
    modified = frames.copy().astype(np.float32)
    frame_length = len(frames) // len(binary_msg)
    
    # Embed each bit with echo kernel
    for i, bit in enumerate(binary_msg):
        start = i * frame_length
        end = start + frame_length
        delay = d0 if bit == '0' else d1
        
        # Create echo kernel
        kernel = np.zeros(delay)
        kernel[0] = 1.0
        kernel[-1] = alpha
        
        # Apply convolution with type casting
        modified[start:end] += np.convolve(frames[start:end], kernel, 'same')
    
    # Save with original parameters
    with wave.open(output_path, 'wb') as out:
        out.setparams(params)
        out.writeframes(np.int16(modified).tobytes())

def extract_echo_hiding(stego_path, text_length, d0=150, d1=200):
    with wave.open(stego_path, 'rb') as wav:
        frames = np.frombuffer(wav.readframes(-1), dtype=np.int16)
    
    binary = []
    frame_length = len(frames) // (text_length * 8)
    
    for i in range(text_length * 8):
        segment = frames[i*frame_length : (i+1)*frame_length]
        cepstrum = np.fft.irfft(np.log(np.abs(np.fft.rfft(segment)) + 1e-10))
        
        # Find peak responses
        peak0 = np.argmax(cepstrum[d0-5:d0+5]) + d0-5
        peak1 = np.argmax(cepstrum[d1-5:d1+5]) + d1-5
        binary.append('1' if cepstrum[peak1] > cepstrum[peak0] else '0')
    
    return ''.join(binary)

# Configuration
input_folder = "data/audio"
output_folder = "output_audio"
os.makedirs(output_folder, exist_ok=True)

secret_text = "HelloWorld"
binary_text = text_to_binary(secret_text)
print(f"Binary text: {binary_text}")

# Embed text in all WAV files
for fname in os.listdir(input_folder):
    if fname.endswith(".wav"):
        in_path = os.path.join(input_folder, fname)
        out_path = os.path.join(output_folder, fname)
        embed_echo_hiding(in_path, binary_text, out_path)

        
print("Embedding complete.")

# Extract and verify from processed files
for fname in os.listdir(output_folder):
    if fname.endswith(".wav"):
        stego_path = os.path.join(output_folder, fname)
        extracted_binary_text = extract_echo_hiding(stego_path, len(secret_text))
        extracted_watermark = ''.join([chr(int(extracted_binary_text[i:i+8], 2)) for i in range(0, len(extracted_binary_text), 8)])
        print(f"Extracted binary watermark from {fname}: {extracted_watermark}")
        # print(f"{fname}:\n{binary_text}\n{extracted_binary_text}\n")
