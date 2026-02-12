"""
OCR Evaluator Module

Main evaluation pipeline that orchestrates:
1. Loading test images and ground truth
2. Running OCR with different preprocessing modes
3. Computing metrics per image and aggregates
4. Extracting confidence scores
5. Generating visualizations
6. Exporting results
"""

import os
import sys
import json
import csv
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import ImagePreprocessor
from src.ocr_engine import OCREngine
from src.utils import clean_text

from .metrics import OCRMetrics, compute_aggregate_metrics
from .comparison import TextComparator, load_ground_truth, find_ground_truth_file
from .visualization import OCRVisualizer


class OCREvaluator:
    """
    Complete OCR evaluation pipeline.
    
    Compares OCR output against ground truth, computes metrics,
    and generates visualizations.
    """
    
    def __init__(self, output_dir: str = './results'):
        """
        Initialize the evaluator.
        
        Args:
            output_dir: Directory to save results and plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.preprocessor = ImagePreprocessor()
        self.ocr_engine = OCREngine()
        self.comparator = TextComparator()
        self.visualizer = OCRVisualizer(output_dir)
        
        self.results = {
            'per_image_results': [],
            'aggregate_metrics': {},
            'all_confidence_scores': [],
            'mode_comparison': {},
            'precision_recall_points': {'precision': [], 'recall': [], 'thresholds': []},
            'evaluation_timestamp': None
        }
    
    def run_ocr_on_image(self, image_path: str, preprocess_mode: str = 'standard',
                         psm: int = 6) -> Tuple[str, List[Dict]]:
        """
        Run OCR on a single image.
        
        Args:
            image_path: Path to the image
            preprocess_mode: Preprocessing mode ('standard', 'threshold', 'none')
            psm: Tesseract page segmentation mode
            
        Returns:
            Tuple of (extracted text, word data with confidence scores)
        """
        # Preprocess
        if preprocess_mode == 'none':
            image = self.preprocessor.load_image(image_path)
            processed = self.preprocessor.to_grayscale(image)
        else:
            processed = self.preprocessor.preprocess(image_path, mode=preprocess_mode)
        
        # Extract text
        text = self.ocr_engine.extract_text(processed, psm=psm)
        cleaned = clean_text(text)
        
        # Get detailed data with confidence scores
        word_data = self.ocr_engine.get_data(processed)
        
        return cleaned, word_data
    
    def extract_confidence_scores(self, word_data: Dict) -> List[float]:
        """
        Extract confidence scores from OCR word data.
        
        Args:
            word_data: Dictionary from pytesseract.image_to_data
            
        Returns:
            List of confidence scores (0-100)
        """
        confidences = []
        
        if 'conf' in word_data:
            for conf, text in zip(word_data['conf'], word_data.get('text', [])):
                # Filter out empty entries and -1 (which indicates no word)
                if conf != -1 and text and text.strip():
                    confidences.append(float(conf))
        
        return confidences
    
    def evaluate_single_image(self, image_path: str, ground_truth_text: str,
                               preprocess_mode: str = 'standard') -> Dict:
        """
        Evaluate OCR performance on a single image.
        
        Args:
            image_path: Path to image file
            ground_truth_text: Reference text content
            preprocess_mode: Preprocessing mode to use
            
        Returns:
            Dictionary with image name and all metrics
        """
        image_name = os.path.basename(image_path)
        
        try:
            ocr_text, word_data = self.run_ocr_on_image(image_path, preprocess_mode)
            
            # Compute metrics
            metrics = OCRMetrics.compute_all_metrics(ocr_text, ground_truth_text)
            
            # Extract confidence scores
            confidences = self.extract_confidence_scores(word_data)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                'image_name': image_name,
                'image_path': image_path,
                'preprocess_mode': preprocess_mode,
                'ocr_text': ocr_text,
                'ground_truth': ground_truth_text,
                'character_accuracy': metrics['character_accuracy'],
                'word_accuracy': metrics['word_accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1_score': metrics['f1_score'],
                'confidence_scores': confidences,
                'avg_confidence': avg_confidence,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'image_name': image_name,
                'image_path': image_path,
                'preprocess_mode': preprocess_mode,
                'status': 'error',
                'error_message': str(e),
                'character_accuracy': 0.0,
                'word_accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'confidence_scores': [],
                'avg_confidence': 0.0
            }
    
    def evaluate_batch(self, image_paths: List[str], ground_truth_dir: str,
                       preprocess_mode: str = 'standard',
                       verbose: bool = True) -> List[Dict]:
        """
        Evaluate multiple images against their ground truth files.
        
        Args:
            image_paths: List of paths to image files
            ground_truth_dir: Directory containing .txt ground truth files
            preprocess_mode: Preprocessing mode to use
            verbose: Print progress information
            
        Returns:
            List of per-image result dictionaries
        """
        results = []
        
        for i, image_path in enumerate(image_paths):
            if verbose:
                print(f"[{i+1}/{len(image_paths)}] Processing: {os.path.basename(image_path)}")
            
            # Find corresponding ground truth
            gt_path = find_ground_truth_file(image_path, ground_truth_dir)
            
            if gt_path is None:
                if verbose:
                    print(f"  WARNING: No ground truth found for {os.path.basename(image_path)}")
                results.append({
                    'image_name': os.path.basename(image_path),
                    'image_path': image_path,
                    'status': 'skipped',
                    'error_message': 'No ground truth file found',
                    'character_accuracy': 0.0,
                    'word_accuracy': 0.0,
                    'precision': 0.0,
                    'recall': 0.0,
                    'f1_score': 0.0,
                    'confidence_scores': [],
                    'avg_confidence': 0.0
                })
                continue
            
            gt_text = load_ground_truth(gt_path)
            result = self.evaluate_single_image(image_path, gt_text, preprocess_mode)
            results.append(result)
            
            if verbose:
                print(f"  Character Accuracy: {result['character_accuracy']*100:.1f}%")
                print(f"  Word Accuracy: {result['word_accuracy']*100:.1f}%")
        
        return results
    
    def compare_preprocessing_modes(self, image_paths: List[str], ground_truth_dir: str,
                                      modes: List[str] = ['standard', 'threshold'],
                                      verbose: bool = True) -> Dict[str, Dict]:
        """
        Compare OCR performance across different preprocessing modes.
        
        Args:
            image_paths: List of image paths
            ground_truth_dir: Directory with ground truth files
            modes: List of preprocessing modes to compare
            verbose: Print progress
            
        Returns:
            Dictionary with aggregate metrics per mode
        """
        mode_results = {}
        
        for mode in modes:
            if verbose:
                print(f"\n=== Evaluating with '{mode}' preprocessing ===")
            
            results = self.evaluate_batch(image_paths, ground_truth_dir, mode, verbose)
            
            # Filter successful results for aggregation
            successful = [r for r in results if r['status'] == 'success']
            
            if successful:
                metrics_list = [{
                    'character_accuracy': r['character_accuracy'],
                    'word_accuracy': r['word_accuracy'],
                    'precision': r['precision'],
                    'recall': r['recall'],
                    'f1_score': r['f1_score']
                } for r in successful]
                
                mode_results[mode] = compute_aggregate_metrics(metrics_list)
            else:
                mode_results[mode] = {
                    'character_accuracy': 0.0,
                    'word_accuracy': 0.0,
                    'precision': 0.0,
                    'recall': 0.0,
                    'f1_score': 0.0
                }
        
        return mode_results
    
    def run_full_evaluation(self, test_dir: str, ground_truth_dir: str,
                            preprocess_mode: str = 'standard',
                            compare_modes: bool = False,
                            verbose: bool = True) -> Dict:
        """
        Run complete evaluation pipeline.
        
        Args:
            test_dir: Directory containing test images
            ground_truth_dir: Directory containing ground truth .txt files
            preprocess_mode: Default preprocessing mode
            compare_modes: If True, compare standard vs threshold modes
            verbose: Print progress information
            
        Returns:
            Complete evaluation results dictionary
        """
        self.results['evaluation_timestamp'] = datetime.now().isoformat()
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        image_paths = []
        
        for filename in os.listdir(test_dir):
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                image_paths.append(os.path.join(test_dir, filename))
        
        if not image_paths:
            raise ValueError(f"No image files found in {test_dir}")
        
        if verbose:
            print(f"Found {len(image_paths)} test images")
            print(f"Ground truth directory: {ground_truth_dir}")
        
        # Run evaluation
        per_image_results = self.evaluate_batch(
            image_paths, ground_truth_dir, preprocess_mode, verbose
        )
        
        self.results['per_image_results'] = per_image_results
        
        # Collect all confidence scores
        for result in per_image_results:
            if result['status'] == 'success':
                self.results['all_confidence_scores'].extend(result['confidence_scores'])
        
        # Compute aggregate metrics
        successful_results = [r for r in per_image_results if r['status'] == 'success']
        if successful_results:
            metrics_list = [{
                'character_accuracy': r['character_accuracy'],
                'word_accuracy': r['word_accuracy'],
                'precision': r['precision'],
                'recall': r['recall'],
                'f1_score': r['f1_score']
            } for r in successful_results]
            
            self.results['aggregate_metrics'] = compute_aggregate_metrics(metrics_list)
            
            # Store precision-recall points for curve
            self.results['precision_recall_points'] = {
                'precision': [r['precision'] for r in successful_results],
                'recall': [r['recall'] for r in successful_results],
                'thresholds': [r['image_name'] for r in successful_results]
            }
        
        # Compare modes if requested
        if compare_modes:
            self.results['mode_comparison'] = self.compare_preprocessing_modes(
                image_paths, ground_truth_dir, ['standard', 'threshold'], verbose
            )
        
        return self.results
    
    def generate_visualizations(self) -> Dict[str, str]:
        """
        Generate all visualizations from current results.
        
        Returns:
            Dictionary mapping plot names to file paths
        """
        return self.visualizer.generate_all_plots(self.results)
    
    def export_results(self, format: str = 'json') -> str:
        """
        Export results to file.
        
        Args:
            format: 'json' or 'csv'
            
        Returns:
            Path to exported file
        """
        if format == 'json':
            # Create a serializable version (exclude non-serializable items)
            export_data = {
                'evaluation_timestamp': self.results['evaluation_timestamp'],
                'aggregate_metrics': self.results['aggregate_metrics'],
                'mode_comparison': self.results.get('mode_comparison', {}),
                'per_image_results': []
            }
            
            for r in self.results['per_image_results']:
                export_data['per_image_results'].append({
                    'image_name': r['image_name'],
                    'status': r['status'],
                    'character_accuracy': r['character_accuracy'],
                    'word_accuracy': r['word_accuracy'],
                    'precision': r['precision'],
                    'recall': r['recall'],
                    'f1_score': r['f1_score'],
                    'avg_confidence': r['avg_confidence']
                })
            
            filepath = os.path.join(self.output_dir, 'evaluation_results.json')
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
        elif format == 'csv':
            filepath = os.path.join(self.output_dir, 'evaluation_results.csv')
            
            fieldnames = ['image_name', 'status', 'character_accuracy', 'word_accuracy',
                          'precision', 'recall', 'f1_score', 'avg_confidence']
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for r in self.results['per_image_results']:
                    writer.writerow({
                        'image_name': r['image_name'],
                        'status': r['status'],
                        'character_accuracy': f"{r['character_accuracy']:.4f}",
                        'word_accuracy': f"{r['word_accuracy']:.4f}",
                        'precision': f"{r['precision']:.4f}",
                        'recall': f"{r['recall']:.4f}",
                        'f1_score': f"{r['f1_score']:.4f}",
                        'avg_confidence': f"{r['avg_confidence']:.2f}"
                    })
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filepath
    
    def print_summary(self):
        """Print a summary of evaluation results."""
        print("\n" + "="*60)
        print("OCR EVALUATION SUMMARY")
        print("="*60)
        
        agg = self.results.get('aggregate_metrics', {})
        print(f"\nOverall Metrics (averaged across all images):")
        print(f"  Character Accuracy: {agg.get('character_accuracy', 0)*100:.2f}%")
        print(f"  Word Accuracy:      {agg.get('word_accuracy', 0)*100:.2f}%")
        print(f"  Precision:          {agg.get('precision', 0)*100:.2f}%")
        print(f"  Recall:             {agg.get('recall', 0)*100:.2f}%")
        print(f"  F1-Score:           {agg.get('f1_score', 0)*100:.2f}%")
        
        if self.results.get('mode_comparison'):
            print(f"\nPreprocessing Mode Comparison:")
            for mode, metrics in self.results['mode_comparison'].items():
                print(f"\n  {mode.upper()}:")
                print(f"    Character Accuracy: {metrics['character_accuracy']*100:.2f}%")
                print(f"    Word Accuracy:      {metrics['word_accuracy']*100:.2f}%")
        
        total = len(self.results['per_image_results'])
        success = sum(1 for r in self.results['per_image_results'] if r['status'] == 'success')
        print(f"\nProcessed {success}/{total} images successfully")
        print("="*60)
