import argparse
import os
import sys
from src.preprocessing import ImagePreprocessor
from src.ocr_engine import OCREngine
from src.utils import clean_text, save_to_file

def main():
    parser = argparse.ArgumentParser(description="High-Accuracy OCR System")
    parser.add_argument('image_path', help="Path to the input image")
    parser.add_argument('--output', '-o', help="Path to save the output text file", default=None)
    parser.add_argument('--preprocess', '-p', choices=['standard', 'threshold', 'none'], default='standard',
                        help="Preprocessing mode: standard (noise reduction), threshold (adaptive thresholding), none")
    parser.add_argument('--psm', type=int, default=6, help="Tesseract PSM mode (default 6: Uniform block)")
    parser.add_argument('--whitelist', help="whitelist characters (e.g. '0123456789')", default=None)
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose output")
    
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found at {args.image_path}")
        sys.exit(1)

    print(f"Processing {args.image_path}...")

    # 1. Preprocessing
    preprocessor = ImagePreprocessor()
    if args.preprocess == 'none':
        image = preprocessor.load_image(args.image_path)
        processed_image = preprocessor.to_grayscale(image) # Tesseract prefers grayscale anyway
        print("Skipping advanced preprocessing.")
    else:
        print(f"Applying {args.preprocess} preprocessing...")
        processed_image = preprocessor.preprocess(args.image_path, mode=args.preprocess)

    # 2. OCR Extraction
    print(f"Running OCR (PSM: {args.psm})...")
    ocr = OCREngine()
    try:
        raw_text = ocr.extract_text(processed_image, psm=args.psm, whitelist=args.whitelist)
    except Exception as e:
        print(f"OCR Error: {e}")
        print("Ensure Tesseract is installed and in your PATH.")
        sys.exit(1)

    # 3. Post-processing
    cleaned_text = clean_text(raw_text)

    # Output
    print("\n--- Extracted Text ---\n")
    print(cleaned_text)
    print("\n----------------------\n")

    if args.output:
        save_to_file(cleaned_text, args.output)
    elif args.verbose:
        # If no output file, maybe save to a default one? 
        # Requirement said "Option to save extracted text to a .txt file", so if not provided, just print.
        pass

if __name__ == "__main__":
    main()