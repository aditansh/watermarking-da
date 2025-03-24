import os
import cv2
import numpy as np
from pywt import dwt2, idwt2
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def add_binary_watermark(image_path, binary_watermark):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    coeffs = dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    U, S, Vt = np.linalg.svd(LL, full_matrices=False)
    
    binary_watermark_list = list(binary_watermark)
    for i in range(len(binary_watermark_list)):
        if binary_watermark_list[i] == '1':
            S[i % len(S)] += 10 
    
    LL_watermarked = np.dot(U, np.dot(np.diag(S), Vt))
    
    watermarked_image = idwt2((LL_watermarked, (LH, HL, HH)), 'haar')
    watermarked_image = np.clip(watermarked_image, 0, 255).astype(np.uint8)
    
    return watermarked_image

def extract_binary_watermark(image_path, original_image_path, watermark_length):
    watermarked_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    
    coeffs_watermarked = dwt2(watermarked_image, 'haar')
    LL_watermarked, _ = coeffs_watermarked
    
    coeffs_original = dwt2(original_image, 'haar')
    LL_original, _ = coeffs_original
    
    U_w, S_w, Vt_w = np.linalg.svd(LL_watermarked, full_matrices=False)
    U_o, S_o, Vt_o = np.linalg.svd(LL_original, full_matrices=False)
    
    extracted_watermark = ''
    for i in range(watermark_length):
        if S_w[i % len(S_w)] > S_o[i % len(S_o)]:
            extracted_watermark += '1'
        else:
            extracted_watermark += '0'
    
    return extracted_watermark

def calculate_metrics(original_image_path, watermarked_image_path):
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    watermarked_image = cv2.imread(watermarked_image_path, cv2.IMREAD_GRAYSCALE)
    
    psnr_value = psnr(original_image, watermarked_image)
    ssim_value, _ = ssim(original_image, watermarked_image, full=True)
    
    return psnr_value, ssim_value

data_folder = 'data/images'
watermarked_folder = 'watermarked_data'
os.makedirs(watermarked_folder, exist_ok=True)

watermark_text = "Sample"
binary_watermark = text_to_binary(watermark_text)
print(f"Binary watermark: {binary_watermark}\n")

for file_name in os.listdir(data_folder):
    if file_name.endswith('.bmp'):
        image_path = os.path.join(data_folder, file_name)
        watermarked_image = add_binary_watermark(image_path, binary_watermark)
        output_path = os.path.join(watermarked_folder, file_name)
        cv2.imwrite(output_path, watermarked_image)

print("Watermarking completed. Watermarked images are saved in 'watermarked_data' folder.\n")

for file_name in os.listdir(watermarked_folder):
    if file_name.endswith('.bmp'):
        watermarked_image_path = os.path.join(watermarked_folder, file_name)
        original_image_path = os.path.join(data_folder, file_name)
        extracted_binary_watermark = extract_binary_watermark(watermarked_image_path, original_image_path, len(binary_watermark))
        # extracted_watermark = ''.join([chr(int(extracted_binary_watermark[i:i+8], 2)) for i in range(0, len(extracted_binary_watermark), 8)])
        # print(f"Extracted binary watermark from {file_name}: {extracted_watermark}")
        print(f"{file_name}:\n{binary_watermark}\n{extracted_binary_watermark}\n")

metrics = {}

for file_name in os.listdir(watermarked_folder):
    if file_name.endswith('.bmp'):
        watermarked_image_path = os.path.join(watermarked_folder, file_name)
        original_image_path = os.path.join(data_folder, file_name)
        psnr_value, ssim_value = calculate_metrics(original_image_path, watermarked_image_path)
        metrics[file_name] = {'PSNR': psnr_value, 'SSIM': ssim_value}

print("Metrics for watermarked images:")
for file_name, metric in metrics.items():
    print(f"{file_name}: PSNR = {metric['PSNR']}, SSIM = {metric['SSIM']}")
