# Watermarking Project

This project implements image watermarking using **DWT-SVD Image Watermarking** and audio steganography using **Echo Hiding.**

## Project Structure

### Files

- **`dwt-svd.py`**: Implements image watermarking using Discrete Wavelet Transform (DWT) and Singular Value Decomposition (SVD).
- **`echo-hiding.py`**: Implements audio watermarking using the Echo Hiding technique.
- **`data/`**: Contains input images and audio files.
- **`output_audio/`**: Stores audio files with embedded watermarks.
- **`watermarked_data/`**: Stores images with embedded watermarks.

## Requirements

Install the required Python libraries using:

```bash
pip install numpy opencv-python pywavelets scikit-image
```

## Usage

### 1. Image Watermarking (`dwt-svd.py`)

#### Embedding Watermark

1. Place the images to be watermarked in the `data/images/` folder.
2. Run the script:
   ```
   python dwt-svd.py
   ```
3. Watermarked images will be saved in the `watermarked_data/` folder.

#### Extracting Watermark

The script automatically extracts the watermark from the watermarked images and compares it with the original watermark.

#### Metrics

The script calculates **PSNR** and **SSIM** metrics to evaluate the quality of the watermarked images.

### 2. Audio Steganography (`echo-hiding.py`)

#### Embedding Text

1. Place the audio files to be watermarked in the `data/audio/` folder.
2. Run the script:
   ```
   python echo-hiding.py
   ```
3. Embedded audio files will be saved in the `output_audio/` folder.

#### Extracting Text

The script automatically extracts the text from the watermarked audio files and verifies it against the original text.

## Example Outputs

### Image Watermarking

* **Binary Watermark** : `010100110110000101101101011100000110110001100101`
* **Metrics** : `0000.bmp: PSNR = 35.67, SSIM = 0.98`

### Audio Watermarking

* **Binary Watermark** : `01001000011001010110110001101100011011110101011101101111011100100110110001100100`
* **Extracted Watermark** : `HelloWorld`

## Notes

* Ensure the input files are in the correct format (`.bmp` for images, `.wav` for audio).
* Modify the watermark text in the scripts as needed.
* The `output_audio/` and `watermarked_data/` folders are automatically created if they do not exist.
