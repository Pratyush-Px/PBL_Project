"""
Text Comparison Module

Utilities for comparing OCR output with ground truth text.
Handles text normalization, tokenization, and similarity calculations.
"""

import re
from typing import List, Tuple, Optional
from difflib import SequenceMatcher


class TextComparator:
    """
    Compare OCR text with ground truth using various methods.
    """
    
    def __init__(self, ignore_case: bool = True, ignore_punctuation: bool = True,
                 ignore_whitespace: bool = True):
        """
        Initialize comparator with normalization settings.
        
        Args:
            ignore_case: Convert to lowercase before comparison
            ignore_punctuation: Remove punctuation before comparison
            ignore_whitespace: Normalize whitespace before comparison
        """
        self.ignore_case = ignore_case
        self.ignore_punctuation = ignore_punctuation
        self.ignore_whitespace = ignore_whitespace
    
    def normalize(self, text: str) -> str:
        """
        Normalize text according to comparator settings.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        result = text
        
        if self.ignore_case:
            result = result.lower()
        
        if self.ignore_punctuation:
            # Remove punctuation except apostrophes in contractions
            result = re.sub(r"[^\w\s']", " ", result)
            result = re.sub(r"(?<!\w)'|'(?!\w)", " ", result)
        
        if self.ignore_whitespace:
            # Normalize all whitespace to single spaces
            result = " ".join(result.split())
        
        return result.strip()
    
    def get_word_difference(self, ocr_text: str, ground_truth: str) -> dict:
        """
        Get detailed word-level difference between OCR and ground truth.
        
        Args:
            ocr_text: OCR extracted text
            ground_truth: Reference text
            
        Returns:
            Dictionary with:
            - matched_words: Words correctly found
            - missing_words: Words in ground truth but not in OCR
            - extra_words: Words in OCR but not in ground truth
        """
        ocr_normalized = self.normalize(ocr_text)
        gt_normalized = self.normalize(ground_truth)
        
        ocr_words = set(ocr_normalized.split()) if ocr_normalized else set()
        gt_words = set(gt_normalized.split()) if gt_normalized else set()
        
        return {
            'matched_words': list(ocr_words & gt_words),
            'missing_words': list(gt_words - ocr_words),
            'extra_words': list(ocr_words - gt_words)
        }
    
    def sequence_similarity(self, ocr_text: str, ground_truth: str) -> float:
        """
        Calculate sequence similarity using difflib's SequenceMatcher.
        
        This preserves word order in comparison, unlike word-bag approaches.
        
        Args:
            ocr_text: OCR extracted text
            ground_truth: Reference text
            
        Returns:
            Similarity ratio between 0.0 and 1.0
        """
        ocr_normalized = self.normalize(ocr_text)
        gt_normalized = self.normalize(ground_truth)
        
        if not gt_normalized and not ocr_normalized:
            return 1.0
        if not gt_normalized or not ocr_normalized:
            return 0.0
        
        return SequenceMatcher(None, ocr_normalized, gt_normalized).ratio()
    
    def line_by_line_comparison(self, ocr_text: str, ground_truth: str) -> List[dict]:
        """
        Compare texts line by line.
        
        Args:
            ocr_text: OCR extracted text
            ground_truth: Reference text
            
        Returns:
            List of dictionaries with line-level comparison results
        """
        ocr_lines = ocr_text.split('\n') if ocr_text else []
        gt_lines = ground_truth.split('\n') if ground_truth else []
        
        results = []
        max_lines = max(len(ocr_lines), len(gt_lines))
        
        for i in range(max_lines):
            ocr_line = ocr_lines[i] if i < len(ocr_lines) else ""
            gt_line = gt_lines[i] if i < len(gt_lines) else ""
            
            ocr_norm = self.normalize(ocr_line)
            gt_norm = self.normalize(gt_line)
            
            similarity = SequenceMatcher(None, ocr_norm, gt_norm).ratio() if (ocr_norm or gt_norm) else 1.0
            
            results.append({
                'line_number': i + 1,
                'ground_truth': gt_line,
                'ocr_output': ocr_line,
                'similarity': similarity,
                'is_match': ocr_norm == gt_norm
            })
        
        return results


def load_ground_truth(file_path: str, encoding: str = 'utf-8') -> str:
    """
    Load ground truth text from a file.
    
    Args:
        file_path: Path to the ground truth text file
        encoding: File encoding (default: utf-8)
        
    Returns:
        Ground truth text content
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def find_ground_truth_file(image_path: str, gt_directory: str, 
                           extension: str = '.txt') -> Optional[str]:
    """
    Find the ground truth file corresponding to an image.
    
    Assumes ground truth files have the same name as images but with .txt extension.
    
    Args:
        image_path: Path to the image file
        gt_directory: Directory containing ground truth files
        extension: Extension of ground truth files
        
    Returns:
        Path to ground truth file or None if not found
    """
    import os
    
    # Get image filename without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Build ground truth path
    gt_filename = image_name + extension
    gt_path = os.path.join(gt_directory, gt_filename)
    
    if os.path.exists(gt_path):
        return gt_path
    
    return None
