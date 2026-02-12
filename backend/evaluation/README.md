# OCR Evaluation Module - Usage Guide

## Quick Start

### Single Image Evaluation
Evaluate one image against its ground truth text file:
 python ocr1/evaluate.py --image ocr1/test_data/images/sample1.png --gt ocr1/test_data/ground_truth/sample1.txt
```bash
python evaluate.py --image <image_path> --gt <ground_truth_path>
```

**Example:**
```bash
python evaluate.py --image ./test_data/images/sample1.png --gt ./test_data/ground_truth/sample1.txt
```

---

### Batch Evaluation (Multiple Images)
Evaluate all images in a directory:
$ python ocr1/evaluate.py --test-dir ocr1/test_data/images --ground-truth ocr1/test_data/ground_truth --compare-modes
```bash
python evaluate.py --test-dir <images_folder> --ground-truth <ground_truth_folder>
```

**Example:**
```bash
python evaluate.py --test-dir ./test_data/images --ground-truth ./test_data/ground_truth
```

> **Note:** Ground truth files must have the same name as images (e.g., `sample1.png` → `sample1.txt`)

---

## Options

| Argument | Short | Description |
|----------|-------|-------------|
| `--image` | `-i` | Single image file path |
| `--gt` | | Ground truth text file (for single mode) |
| `--test-dir` | `-t` | Directory of test images (for batch mode) |
| `--ground-truth` | `-g` | Directory of ground truth files (for batch mode) |
| `--preprocess` | `-p` | Preprocessing: `standard`, `threshold`, or `none` |
| `--compare-modes` | `-c` | Compare standard vs threshold modes |
| `--output` | `-o` | Output directory (default: `./results`) |
| `--export-format` | `-f` | Export format: `json`, `csv`, or `both` |
| `--no-plots` | | Skip generating charts |
| `--quiet` | `-q` | Suppress verbose output |

---

## Examples

### Compare Preprocessing Modes
```bash
python evaluate.py --test-dir ./test_data/images --ground-truth ./test_data/ground_truth --compare-modes
```

### Use Threshold Preprocessing
```bash
python evaluate.py --image ./receipt.jpg --gt ./receipt.txt --preprocess threshold
```

### Export Results to CSV
```bash
python evaluate.py --test-dir ./images --ground-truth ./gt --export-format both
```

---

## Output Files

Results are saved to the `./results/` folder:

| File | Description |
|------|-------------|
| `evaluation_results.json` | All metrics in JSON format |
| `evaluation_results.csv` | All metrics in CSV format |
| `metrics_summary.png` | Bar chart of overall metrics |
| `char_accuracy_per_image.png` | Per-image accuracy breakdown |
| `accuracy_by_mode.png` | Standard vs Threshold comparison |
| `precision_recall_curve.png` | Precision-Recall trade-off |
| `confidence_distribution.png` | OCR confidence histogram |

---

## Metrics Explained

| Metric | What It Measures |
|--------|-----------------|
| **Character Accuracy** | % of characters correctly recognized |
| **Word Accuracy** | % of complete words correctly recognized |
| **Precision** | Of OCR words, how many are in ground truth |
| **Recall** | Of ground truth words, how many did OCR find |
| **F1-Score** | Balance between precision and recall |

---

## Folder Structure

```
ocr1/
├── evaluate.py              ← Run this script
├── test_data/
│   ├── images/              ← Put test images here
│   │   ├── sample1.png
│   │   └── sample2.png
│   └── ground_truth/        ← Put matching .txt files here
│       ├── sample1.txt
│       └── sample2.txt
└── results/                 ← Output appears here
    ├── evaluation_results.json
    └── *.png charts
```
