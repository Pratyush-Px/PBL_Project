# High-Accuracy OCR System Instructions

## Setup
1. **Activate the Virtual Environment**:
   ```powershell
   .\myenv\Scripts\activate
   ```
   *(If you are already in the environment, you can skip this)*

2. **Dependencies**:
   Ensure `Tesseract-OCR` is installed on your Windows machine and allowed in your PATH. If not, the script tries to find it in common default locations.

## Running the OCR
The main entry point is `main.py`.

### Basic Usage
Run on an image and print text to console:
```bash
python main.py image.jpg
```

### Save Output to File
```bash
python main.py image.jpg --output result.txt
```

### Preprocessing Modes
The system has different preprocessing modes to handle different image qualities:

1. **Standard (Default)**: Best for good quality scans/photos. Uses noise reduction.
   ```bash
   python main.py image.jpg --preprocess standard
   ```

2. **Threshold**: Best for images with uneven lighting or shadows. Uses adaptive thresholding.
   ```bash
   python main.py image.jpg --preprocess threshold
   ```

3. **None**: No preprocessing (just grayscale).
   ```bash
   python main.py image.jpg --preprocess none
   ```

### Specific Options
- **Whitelist**: To extract *only* numbers (useful for prices/dates):
  ```bash
  python main.py receipt.jpg --whitelist "0123456789."
  ```
- **PSM Modes**: Change how Tesseract segments the page.
  - `--psm 6` (Default): Assume a single uniform block of text.
  - `--psm 4`: Assume a single column of text of variable sizes (good for spreadsheets).
  - `--psm 3`: Fully automatic page segmentation (no OSD).

## Examples
**Run on `ReceiptSwiss.jpg` and save to file:**
```bash
python main.py ReceiptSwiss.jpg --output receipt_text.txt --preprocess standard
```

**Run on a noisy image with thresholding:**
```bash
python main.py noisy_doc.jpg --output clean_doc.txt --preprocess threshold
```
