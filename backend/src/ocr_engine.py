import pytesseract
import sys
import os

class OCREngine:
    """
    Wrapper class for PyTesseract.
    """
    def __init__(self, tesseract_cmd=None):
        """
        Initialize the OCR engine.
        :param tesseract_cmd: Optional path to the tesseract executable.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        # Check if tesseract is available in path usually
        try:
             pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            # Fallback for common windows paths if not in PATH
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Users\AppData\Local\Tesseract-OCR\tesseract.exe" 
            ]
            for path in common_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break

    def extract_text(self, image, psm=6, whitelist=None):
        """
        Extracts text from the preprocessed image.
        :param image: The image array (from cv2).
        :param psm: Page Segmentation Mode (default 6: assume single uniform block of text).
               3 is fully automatic. 4 is single column. 6 is uniform block.
        :param whitelist: Optional string of characters to whitelist (e.g. "0123456789.")
        :return: Extracted text string.
        """
        config_params = f"--psm {psm}"
        if whitelist:
            config_params += f" -c tessedit_char_whitelist={whitelist}"
        
        # Standard configuration for english
        # oem 3 = Default OCR Engine Mode (LSTM + Legacy)
        config_params += " --oem 3"

        return pytesseract.image_to_string(image, config=config_params, lang='eng')

    def get_data(self, image):
        """
        Returns verbose data including bounding boxes, confidences, etc.
        """
        return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
