"""
Test Image Generator

Creates simple test images with known text for evaluation testing.
Run this script to generate sample test images.
"""

import os
import sys

# Check if PIL/Pillow is available
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed. Install with: pip install Pillow")
    print("Alternatively, create test images manually and place them in test_data/images/")
    sys.exit(1)


def create_test_image(text: str, filename: str, output_dir: str, 
                      size: tuple = (800, 400), font_size: int = 24):
    """
    Create a test image with the given text.
    
    Args:
        text: Text to render on the image
        filename: Output filename
        output_dir: Output directory
        size: Image size (width, height)
        font_size: Font size
    """
    # Create white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a standard font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw text
    y_position = 30
    for line in text.split('\n'):
        draw.text((30, y_position), line, fill='black', font=font)
        y_position += font_size + 10
    
    # Save image
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"Created: {filepath}")
    return filepath


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'test_data', 'images')
    
    # Sample 1: Simple text
    text1 = """Hello World
This is a sample document.
Testing OCR accuracy.
Numbers: 12345
Date: 2024-01-15"""
    create_test_image(text1, 'sample1.png', images_dir)
    
    # Sample 2: Invoice-like text
    text2 = """Invoice Number: INV-2024-001
Customer: John Smith
Total Amount: $150.00
Tax: $12.50"""
    create_test_image(text2, 'sample2.png', images_dir)
    
    print(f"\nTest images created in: {images_dir}")
    print("Ground truth files should be in: test_data/ground_truth/")


if __name__ == '__main__':
    main()
