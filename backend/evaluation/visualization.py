"""
OCR Visualization Module

Generate informative graphs and charts for OCR evaluation results:
- Precision vs Recall curve
- Accuracy vs Preprocessing mode comparison
- Character accuracy per image bar chart
- Confidence distribution histogram
"""

import os
from typing import List, Dict, Optional, Tuple
import numpy as np

# Import matplotlib with non-interactive backend for headless environments
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class OCRVisualizer:
    """
    Generate visualizations for OCR evaluation results.
    """
    
    def __init__(self, output_dir: str = './results', figsize: Tuple[int, int] = (10, 6),
                 style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save generated plots
            figsize: Default figure size (width, height)
            style: Matplotlib style to use
        """
        self.output_dir = output_dir
        self.figsize = figsize
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style (use default if specified style not available)
        try:
            plt.style.use(style)
        except OSError:
            plt.style.use('default')
    
    def plot_precision_recall_curve(self, precision_values: List[float], 
                                     recall_values: List[float],
                                     threshold_labels: Optional[List[str]] = None,
                                     filename: str = 'precision_recall_curve.png') -> str:
        """
        Plot Precision vs Recall curve.
        
        This graph shows the trade-off between precision and recall at different
        confidence thresholds. Higher area under the curve indicates better performance.
        
        WHY USEFUL: Helps determine the optimal confidence threshold for your use case.
        High precision is important when false positives are costly (e.g., legal documents).
        High recall is important when missing information is costly (e.g., medical records).
        
        Args:
            precision_values: List of precision values at different thresholds
            recall_values: List of recall values at different thresholds
            threshold_labels: Optional labels for each threshold point
            filename: Output filename
            
        Returns:
            Path to saved plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Sort by recall for proper curve
        sorted_pairs = sorted(zip(recall_values, precision_values))
        recall_sorted = [p[0] for p in sorted_pairs]
        precision_sorted = [p[1] for p in sorted_pairs]
        
        ax.plot(recall_sorted, precision_sorted, 'b-o', linewidth=2, markersize=8)
        ax.fill_between(recall_sorted, precision_sorted, alpha=0.3)
        
        # Add threshold labels if provided
        if threshold_labels:
            for i, label in enumerate(threshold_labels):
                ax.annotate(label, (recall_values[i], precision_values[i]),
                           textcoords="offset points", xytext=(5, 5), fontsize=9)
        
        ax.set_xlabel('Recall', fontsize=12)
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_title('Precision-Recall Curve', fontsize=14, fontweight='bold')
        ax.set_xlim([0, 1.05])
        ax.set_ylim([0, 1.05])
        ax.grid(True, alpha=0.3)
        
        # Add diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Random')
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return save_path
    
    def plot_accuracy_by_preprocessing(self, mode_metrics: Dict[str, Dict[str, float]],
                                        filename: str = 'accuracy_by_mode.png') -> str:
        """
        Plot bar chart comparing accuracy across preprocessing modes.
        
        WHY USEFUL: Identifies which preprocessing pipeline works best for your document types.
        Standard mode uses noise reduction; threshold mode adds adaptive thresholding.
        This helps optimize your OCR pipeline configuration.
        
        Args:
            mode_metrics: Dictionary with mode names as keys and metrics dict as values
                         e.g., {'standard': {'character_accuracy': 0.95, 'word_accuracy': 0.90}, ...}
            filename: Output filename
            
        Returns:
            Path to saved plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        modes = list(mode_metrics.keys())
        x = np.arange(len(modes))
        width = 0.35
        
        char_acc = [mode_metrics[m].get('character_accuracy', 0) * 100 for m in modes]
        word_acc = [mode_metrics[m].get('word_accuracy', 0) * 100 for m in modes]
        
        bars1 = ax.bar(x - width/2, char_acc, width, label='Character Accuracy', color='#2ecc71')
        bars2 = ax.bar(x + width/2, word_acc, width, label='Word Accuracy', color='#3498db')
        
        ax.set_xlabel('Preprocessing Mode', fontsize=12)
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_title('OCR Accuracy by Preprocessing Mode', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([m.title() for m in modes])
        ax.legend()
        ax.set_ylim([0, 105])
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}%',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return save_path
    
    def plot_character_accuracy_per_image(self, image_results: List[Dict],
                                           filename: str = 'char_accuracy_per_image.png') -> str:
        """
        Plot bar chart of character accuracy for each test image.
        
        WHY USEFUL: Quickly identifies problematic images that need investigation
        or different preprocessing. An outlier image with low accuracy may have
        specific issues like blur, skew, or unusual fonts.
        
        Args:
            image_results: List of dicts with 'image_name' and 'character_accuracy' keys
            filename: Output filename
            
        Returns:
            Path to saved plot
        """
        fig, ax = plt.subplots(figsize=(max(10, len(image_results) * 0.8), 6))
        
        names = [r['image_name'] for r in image_results]
        accuracies = [r['character_accuracy'] * 100 for r in image_results]
        
        # Color bars based on accuracy
        colors = ['#e74c3c' if acc < 70 else '#f39c12' if acc < 90 else '#2ecc71' 
                  for acc in accuracies]
        
        bars = ax.bar(range(len(names)), accuracies, color=colors)
        
        ax.set_xlabel('Test Image', fontsize=12)
        ax.set_ylabel('Character Accuracy (%)', fontsize=12)
        ax.set_title('Character Accuracy per Test Image', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.set_ylim([0, 105])
        
        # Add horizontal reference lines
        ax.axhline(y=90, color='#2ecc71', linestyle='--', alpha=0.5, label='Good (90%)')
        ax.axhline(y=70, color='#f39c12', linestyle='--', alpha=0.5, label='Fair (70%)')
        
        # Add legend for color coding
        legend_elements = [
            mpatches.Patch(color='#2ecc71', label='Good (≥90%)'),
            mpatches.Patch(color='#f39c12', label='Fair (70-90%)'),
            mpatches.Patch(color='#e74c3c', label='Poor (<70%)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            ax.annotate(f'{acc:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return save_path
    
    def plot_confidence_distribution(self, confidence_scores: List[float],
                                      filename: str = 'confidence_distribution.png') -> str:
        """
        Plot histogram of OCR confidence scores.
        
        WHY USEFUL: Reveals the certainty of OCR predictions:
        - High scores clustered near 100%: OCR is confident and likely accurate
        - Bimodal distribution: May indicate two quality levels in documents
        - Many low scores: Document quality issues or OCR struggling
        
        Args:
            confidence_scores: List of confidence scores (0-100)
            filename: Output filename
            
        Returns:
            Path to saved plot
        """
        if not confidence_scores:
            # Create empty plot with message
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No confidence scores available', 
                   ha='center', va='center', fontsize=14)
            ax.set_title('OCR Confidence Distribution', fontsize=14, fontweight='bold')
            save_path = os.path.join(self.output_dir, filename)
            fig.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            return save_path
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create histogram
        n, bins, patches = ax.hist(confidence_scores, bins=20, range=(0, 100),
                                    edgecolor='black', alpha=0.7)
        
        # Color bars based on confidence level
        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i+1]) / 2
            if bin_center < 50:
                patch.set_facecolor('#e74c3c')
            elif bin_center < 80:
                patch.set_facecolor('#f39c12')
            else:
                patch.set_facecolor('#2ecc71')
        
        # Add statistics
        mean_conf = np.mean(confidence_scores)
        median_conf = np.median(confidence_scores)
        
        ax.axvline(mean_conf, color='blue', linestyle='--', linewidth=2,
                   label=f'Mean: {mean_conf:.1f}%')
        ax.axvline(median_conf, color='purple', linestyle=':', linewidth=2,
                   label=f'Median: {median_conf:.1f}%')
        
        ax.set_xlabel('Confidence Score (%)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('OCR Confidence Score Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        ax.set_xlim([0, 100])
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return save_path
    
    def plot_metrics_summary(self, aggregate_metrics: Dict[str, float],
                              filename: str = 'metrics_summary.png') -> str:
        """
        Plot horizontal bar chart summarizing all metrics.
        
        Args:
            aggregate_metrics: Dictionary with metric names and values
            filename: Output filename
            
        Returns:
            Path to saved plot
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        metrics = ['Character Accuracy', 'Word Accuracy', 'Precision', 'Recall', 'F1-Score']
        keys = ['character_accuracy', 'word_accuracy', 'precision', 'recall', 'f1_score']
        values = [aggregate_metrics.get(k, 0) * 100 for k in keys]
        
        colors = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#f39c12']
        
        y_pos = np.arange(len(metrics))
        bars = ax.barh(y_pos, values, color=colors)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics)
        ax.set_xlabel('Score (%)', fontsize=12)
        ax.set_title('OCR Evaluation Metrics Summary', fontsize=14, fontweight='bold')
        ax.set_xlim([0, 105])
        
        # Add value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'{val:.1f}%', va='center', fontsize=10)
        
        plt.tight_layout()
        save_path = os.path.join(self.output_dir, filename)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return save_path
    
    def generate_all_plots(self, evaluation_results: Dict) -> Dict[str, str]:
        """
        Generate all available plots from evaluation results.
        
        Args:
            evaluation_results: Full evaluation results dictionary from OCREvaluator
            
        Returns:
            Dictionary mapping plot names to file paths
        """
        plots = {}
        
        # Per-image character accuracy
        if 'per_image_results' in evaluation_results:
            plots['char_accuracy_per_image'] = self.plot_character_accuracy_per_image(
                evaluation_results['per_image_results']
            )
        
        # Metrics summary
        if 'aggregate_metrics' in evaluation_results:
            plots['metrics_summary'] = self.plot_metrics_summary(
                evaluation_results['aggregate_metrics']
            )
        
        # Confidence distribution
        if 'all_confidence_scores' in evaluation_results:
            plots['confidence_distribution'] = self.plot_confidence_distribution(
                evaluation_results['all_confidence_scores']
            )
        
        # Accuracy by mode (if multiple modes tested)
        if 'mode_comparison' in evaluation_results:
            plots['accuracy_by_mode'] = self.plot_accuracy_by_preprocessing(
                evaluation_results['mode_comparison']
            )
        
        # Precision-recall curve (if threshold analysis done)
        if 'precision_recall_points' in evaluation_results:
            pr_points = evaluation_results['precision_recall_points']
            plots['precision_recall_curve'] = self.plot_precision_recall_curve(
                pr_points['precision'], pr_points['recall'],
                pr_points.get('thresholds')
            )
        
        return plots
