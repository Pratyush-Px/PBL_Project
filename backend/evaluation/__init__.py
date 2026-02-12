# Evaluation module for OCR performance assessment
from .metrics import OCRMetrics
from .comparison import TextComparator
from .visualization import OCRVisualizer
from .evaluator import OCREvaluator

__all__ = ['OCRMetrics', 'TextComparator', 'OCRVisualizer', 'OCREvaluator']
