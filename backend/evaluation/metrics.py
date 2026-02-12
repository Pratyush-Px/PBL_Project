"""
OCR Metrics Module

This module provides functions to calculate various OCR evaluation metrics:
- Character Accuracy: Character-level accuracy using edit distance
- Word Accuracy: Percentage of correctly recognized words
- Precision: Fraction of OCR words that are correct
- Recall: Fraction of ground truth words that were found
- F1-Score: Harmonic mean of precision and recall
"""

from difflib import SequenceMatcher
from typing import Dict, List, Tuple
import re


class OCRMetrics:
    """
    Calculate OCR evaluation metrics comparing OCR output to ground truth.
    """
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """
        Calculate Levenshtein (edit) distance between two strings.
        Uses dynamic programming for efficient computation.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Integer edit distance
        """
        if len(s1) < len(s2):
            return OCRMetrics.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def character_accuracy(ocr_text: str, ground_truth: str) -> float:
        """
        Calculate character-level accuracy using Levenshtein distance.
        
        Character Accuracy = 1 - (edit_distance / max_length)
        
        This metric is sensitive to:
        - Character substitutions (e.g., 'O' vs '0')
        - Missing characters
        - Extra characters
        
        Args:
            ocr_text: Text extracted by OCR
            ground_truth: Reference ground truth text
            
        Returns:
            Float between 0.0 and 1.0 (1.0 = perfect match)
        """
        if not ground_truth and not ocr_text:
            return 1.0
        if not ground_truth or not ocr_text:
            return 0.0
            
        distance = OCRMetrics.levenshtein_distance(ocr_text, ground_truth)
        max_len = max(len(ocr_text), len(ground_truth))
        
        return 1.0 - (distance / max_len)
    
    @staticmethod
    def tokenize(text: str, lowercase: bool = True) -> List[str]:
        """
        Tokenize text into words, removing punctuation.
        
        Args:
            text: Input text
            lowercase: Whether to convert to lowercase
            
        Returns:
            List of word tokens
        """
        if lowercase:
            text = text.lower()
        # Split on whitespace and remove punctuation
        words = re.findall(r'\b\w+\b', text)
        return words
    
    @staticmethod
    def word_accuracy(ocr_text: str, ground_truth: str, lowercase: bool = True) -> float:
        """
        Calculate word-level accuracy.
        
        Word Accuracy = matching_words / total_ground_truth_words
        
        A word is only counted as correct if it exactly matches.
        
        Args:
            ocr_text: Text extracted by OCR
            ground_truth: Reference ground truth text
            lowercase: Whether to perform case-insensitive comparison
            
        Returns:
            Float between 0.0 and 1.0
        """
        gt_words = OCRMetrics.tokenize(ground_truth, lowercase)
        ocr_words = OCRMetrics.tokenize(ocr_text, lowercase)
        
        if not gt_words:
            return 1.0 if not ocr_words else 0.0
        
        # Count matching words (order-independent, using multiset)
        from collections import Counter
        gt_counter = Counter(gt_words)
        ocr_counter = Counter(ocr_words)
        
        # Count matches (minimum of counts for each word)
        matches = sum((gt_counter & ocr_counter).values())
        
        return matches / len(gt_words)
    
    @staticmethod
    def precision_recall_f1(ocr_text: str, ground_truth: str, 
                            lowercase: bool = True) -> Tuple[float, float, float]:
        """
        Calculate Precision, Recall, and F1-Score at word level.
        
        Precision = True Positives / (True Positives + False Positives)
                  = correctly_found_words / total_ocr_words
        
        Recall = True Positives / (True Positives + False Negatives)
               = correctly_found_words / total_ground_truth_words
        
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        
        Args:
            ocr_text: Text extracted by OCR
            ground_truth: Reference ground truth text
            lowercase: Whether to perform case-insensitive comparison
            
        Returns:
            Tuple of (precision, recall, f1_score)
        """
        gt_words = OCRMetrics.tokenize(ground_truth, lowercase)
        ocr_words = OCRMetrics.tokenize(ocr_text, lowercase)
        
        if not gt_words and not ocr_words:
            return (1.0, 1.0, 1.0)
        if not ocr_words:
            return (0.0, 0.0, 0.0)
        if not gt_words:
            return (0.0, 0.0, 0.0)
        
        from collections import Counter
        gt_counter = Counter(gt_words)
        ocr_counter = Counter(ocr_words)
        
        # True positives: words correctly identified
        true_positives = sum((gt_counter & ocr_counter).values())
        
        # Precision: Of all words OCR produced, how many are correct
        precision = true_positives / len(ocr_words)
        
        # Recall: Of all ground truth words, how many did OCR find
        recall = true_positives / len(gt_words)
        
        # F1-Score: Harmonic mean
        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        
        return (precision, recall, f1)
    
    @staticmethod
    def compute_all_metrics(ocr_text: str, ground_truth: str, 
                           lowercase: bool = True) -> Dict[str, float]:
        """
        Compute all OCR metrics at once.
        
        Args:
            ocr_text: Text extracted by OCR
            ground_truth: Reference ground truth text
            lowercase: Whether to perform case-insensitive comparison
            
        Returns:
            Dictionary with all metrics
        """
        char_acc = OCRMetrics.character_accuracy(ocr_text, ground_truth)
        word_acc = OCRMetrics.word_accuracy(ocr_text, ground_truth, lowercase)
        precision, recall, f1 = OCRMetrics.precision_recall_f1(ocr_text, ground_truth, lowercase)
        
        return {
            'character_accuracy': char_acc,
            'word_accuracy': word_acc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }


def compute_aggregate_metrics(metrics_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Compute aggregate (average) metrics from a list of per-image metrics.
    
    Args:
        metrics_list: List of metric dictionaries from compute_all_metrics
        
    Returns:
        Dictionary with averaged metrics
    """
    if not metrics_list:
        return {
            'character_accuracy': 0.0,
            'word_accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0
        }
    
    n = len(metrics_list)
    aggregate = {}
    
    for key in ['character_accuracy', 'word_accuracy', 'precision', 'recall', 'f1_score']:
        aggregate[key] = sum(m[key] for m in metrics_list) / n
    
    return aggregate
