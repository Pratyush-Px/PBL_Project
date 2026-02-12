import cv2
import numpy as np

class ImagePreprocessor:
    """
    Handles image preprocessing to improve OCR accuracy.
    Techniques: Grayscale, Noise Reduction, Adaptive Thresholding.
    """

    def __init__(self, debug=False):
        self.debug = debug

    def load_image(self, image_path):
        """Loads an image from path."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image at {image_path}")
        return img

    def to_grayscale(self, image):
        """Converts image to grayscale."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def remove_noise(self, image):
        """
        Applies Bilateral Filter to remove noise while keeping edges sharp.
        Good for scanning artifacts and low ISO noise.
        """
        # d=9, sigmaColor=75, sigmaSpace=75 are standard good starting points
        return cv2.bilateralFilter(image, 9, 75, 75)

    def adaptive_thresholding(self, image):
        """
        Applies adaptive thresholding to handle varying lighting conditions.
        Returns a binary image (black and white).
        """
        # Adaptive Gaussian Thresholding
        # Block size: 11, C: 2
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
    
    def apply_dilation(self, image, kernel_size=(1, 1)):
        """
        Optional: Dilate to connect broken text segments.
        Use with caution, can merge characters.
        """
        kernel = np.ones(kernel_size, np.uint8)
        return cv2.dilate(image, kernel, iterations=1)
    
    def apply_erosion(self, image, kernel_size=(1, 1)):
        """
        Optional: Erode to thin out bold text.
        """
        kernel = np.ones(kernel_size, np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    def preprocess(self, image_path, mode='standard'):
        """
        Runs the full preprocessing pipeline.
        Modes:
        - standard: Grayscale -> Noise Reduction
        - threshold: Grayscale -> Noise Reduction -> Thresholding
        """
        original = self.load_image(image_path)
        gray = self.to_grayscale(original)
        reduced_noise = self.remove_noise(gray)

        if mode == 'threshold':
            processed = self.adaptive_thresholding(reduced_noise)
        else:
            processed = reduced_noise
            
        return processed
