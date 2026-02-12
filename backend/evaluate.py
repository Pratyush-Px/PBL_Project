#!/usr/bin/env python3
"""
OCR Evaluation CLI

Command-line interface for evaluating OCR performance against ground truth.

Usage:
    # Evaluate single image
    python evaluate.py --image ./test.png --gt ./test.txt

    # Evaluate directory of images
    python evaluate.py --test-dir ./test_data/images --ground-truth ./test_data/ground_truth

This will:
1. Run OCR on the image(s)
2. Compare results against ground truth text
3. Compute Character/Word Accuracy, Precision, Recall, F1-Score
4. Generate visualization charts (for batch mode)
5. Export results to JSON/CSV
"""

import argparse
import os
import sys

# Ensure the evaluation module is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluation import OCREvaluator
from evaluation.metrics import OCRMetrics
from evaluation.comparison import load_ground_truth
from evaluation.visualization import OCRVisualizer


def evaluate_single_file(image_path: str, gt_path: str, preprocess_mode: str = 'standard',
                         output_dir: str = './results'):
    """Evaluate a single image against its ground truth."""
    evaluator = OCREvaluator(output_dir=output_dir)
    
    # Load ground truth
    gt_text = load_ground_truth(gt_path)
    
    # Run evaluation
    result = evaluator.evaluate_single_image(image_path, gt_text, preprocess_mode)
    
    # Print results
    print("="*60)
    print("OCR EVALUATION - Single Image")
    print("="*60)
    print(f"Image:        {os.path.basename(image_path)}")
    print(f"Ground Truth: {os.path.basename(gt_path)}")
    print(f"Preprocess:   {preprocess_mode}")
    print("="*60)
    
    if result['status'] == 'success':
        print(f"\nMetrics:")
        print(f"  Character Accuracy: {result['character_accuracy']*100:.2f}%")
        print(f"  Word Accuracy:      {result['word_accuracy']*100:.2f}%")
        print(f"  Precision:          {result['precision']*100:.2f}%")
        print(f"  Recall:             {result['recall']*100:.2f}%")
        print(f"  F1-Score:           {result['f1_score']*100:.2f}%")
        print(f"  Avg Confidence:     {result['avg_confidence']:.1f}%")
        
        print(f"\n--- OCR Output ---")
        print(result['ocr_text'][:500] + ('...' if len(result['ocr_text']) > 500 else ''))
        print("="*60)
        
        # Generate visualization
        visualizer = OCRVisualizer(output_dir)
        metrics = {
            'character_accuracy': result['character_accuracy'],
            'word_accuracy': result['word_accuracy'],
            'precision': result['precision'],
            'recall': result['recall'],
            'f1_score': result['f1_score']
        }
        
        # Generate single image metrics chart
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        chart_path = visualizer.plot_metrics_summary(metrics, f'{image_name}_metrics.png')
        print(f"\nVisualization saved to: {chart_path}")
        
        # Try to open the chart
        try:
            import subprocess
            subprocess.Popen(['start', '', chart_path], shell=True)
            print("Opening chart...")
        except:
            pass
    else:
        print(f"\nError: {result.get('error_message', 'Unknown error')}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate OCR performance against ground truth',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Single image evaluation:
    python evaluate.py --image ./sample.png --gt ./sample.txt

  Batch evaluation (directory):
    python evaluate.py --test-dir ./test_images --ground-truth ./ground_truth

  Compare preprocessing modes:
    python evaluate.py --test-dir ./test_images --ground-truth ./ground_truth --compare-modes

Metrics Explained:
  - Character Accuracy: Character-level match using edit distance
  - Word Accuracy: Percentage of correctly recognized words
  - Precision: Of OCR words, how many are in ground truth
  - Recall: Of ground truth words, how many did OCR find
  - F1-Score: Harmonic mean of precision and recall
        """
    )
    
    # Single file mode
    parser.add_argument('--image', '-i', help='Single image file to evaluate')
    parser.add_argument('--gt', help='Ground truth text file for the single image')
    
    # Batch mode
    parser.add_argument('--test-dir', '-t', help='Directory containing test images')
    parser.add_argument('--ground-truth', '-g', help='Directory containing ground truth .txt files')
    
    # Common options
    parser.add_argument('--output', '-o', default='./results',
                        help='Output directory for results and plots (default: ./results)')
    parser.add_argument('--preprocess', '-p', choices=['standard', 'threshold', 'none'],
                        default='standard',
                        help='Preprocessing mode (default: standard)')
    parser.add_argument('--compare-modes', '-c', action='store_true',
                        help='Compare standard vs threshold preprocessing modes')
    parser.add_argument('--export-format', '-f', choices=['json', 'csv', 'both'],
                        default='json',
                        help='Export format for results (default: json)')
    parser.add_argument('--no-plots', action='store_true',
                        help='Skip generating visualization plots')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress verbose output')
    
    args = parser.parse_args()
    
    # Determine mode: single file or batch
    single_file_mode = args.image is not None
    batch_mode = args.test_dir is not None
    
    if single_file_mode and batch_mode:
        print("Error: Cannot use both --image and --test-dir. Choose one mode.")
        sys.exit(1)
    
    if not single_file_mode and not batch_mode:
        print("Error: Provide either --image (single file) or --test-dir (batch mode)")
        print("Use --help for usage information.")
        sys.exit(1)
    
    # Single file mode
    if single_file_mode:
        if not args.gt:
            print("Error: --gt (ground truth file) is required with --image")
            sys.exit(1)
        
        if not os.path.isfile(args.image):
            print(f"Error: Image file not found: {args.image}")
            sys.exit(1)
        
        if not os.path.isfile(args.gt):
            print(f"Error: Ground truth file not found: {args.gt}")
            sys.exit(1)
        
        evaluate_single_file(args.image, args.gt, args.preprocess)
        return
    
    # Batch mode (existing logic)
    if not os.path.isdir(args.test_dir):
        print(f"Error: Test directory not found: {args.test_dir}")
        sys.exit(1)
    
    if not os.path.isdir(args.ground_truth):
        print(f"Error: Ground truth directory not found: {args.ground_truth}")
        sys.exit(1)
    
    verbose = not args.quiet
    
    if verbose:
        print("="*60)
        print("OCR EVALUATION")
        print("="*60)
        print(f"Test images:     {os.path.abspath(args.test_dir)}")
        print(f"Ground truth:    {os.path.abspath(args.ground_truth)}")
        print(f"Output:          {os.path.abspath(args.output)}")
        print(f"Preprocess mode: {args.preprocess}")
        print("="*60)
    
    # Run evaluation
    evaluator = OCREvaluator(output_dir=args.output)
    
    try:
        results = evaluator.run_full_evaluation(
            test_dir=args.test_dir,
            ground_truth_dir=args.ground_truth,
            preprocess_mode=args.preprocess,
            compare_modes=args.compare_modes,
            verbose=verbose
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate visualizations
    if not args.no_plots:
        if verbose:
            print("\nGenerating visualizations...")
        
        plots = evaluator.generate_visualizations()
        
        if verbose:
            print(f"Generated {len(plots)} plots:")
            for name, path in plots.items():
                print(f"  - {name}: {path}")
    
    # Export results
    if verbose:
        print(f"\nExporting results...")
    
    if args.export_format in ['json', 'both']:
        json_path = evaluator.export_results('json')
        if verbose:
            print(f"  - JSON: {json_path}")
    
    if args.export_format in ['csv', 'both']:
        csv_path = evaluator.export_results('csv')
        if verbose:
            print(f"  - CSV: {csv_path}")
    
    # Print summary
    evaluator.print_summary()
    
    if verbose:
        print(f"\nResults saved to: {os.path.abspath(args.output)}")


if __name__ == '__main__':
    main()

