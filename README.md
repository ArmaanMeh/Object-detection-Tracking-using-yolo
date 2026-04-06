# Soccer Ball Detection & Tracking using YOLO

A hybrid object detection and tracking system that uses YOLOv8 (fast detection) and CSRT (continuous tracking) to detect and track soccer balls in video sequences.

## Features

- **Hybrid Architecture**: Combines YOLOv8 nano for lightweight detection with OpenCV's CSRT tracker for smooth tracking
- **Real-time Processing**: Optimized for speed with the YOLOv8n (nano) model
- **Dual Visualization**: 
  - Blue bounding box for YOLO detections
  - Green bounding box for CSRT tracking
  - Red status for tracking failures
- **Automatic Recovery**: Falls back to detection when tracking is lost

## Project Structure

```
.
├── main.py                 # YOLOv8-based soccer ball tracker (recommended)
├── submission.py           # YOLOv3-based soccer ball tracker (alternative)
├── requirements.txt        # Python dependencies
├── coco.names.txt         # COCO object class names
├── yolo_files/            # Model weights and configs
│   ├── yolov3.cfg         # YOLOv3 architecture config
│   ├── yolov3.weights     # YOLOv3 pre-trained weights
│   └── yolov8n.pt         # YOLOv8 nano pre-trained weights
├── Output/                # Output videos and results
├── LICENSE                # GNU General Public License v3
└── README.md              # This file
```

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- UltraLytics YOLO (for main.py)
- PyTorch (for YOLO support)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Fundamentals of OPENCV/Project 3"
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the video file:
   - Place `soccer-ball.mp4` in the Output/ directory

## Usage

### Option 1: YOLOv8 Tracker (Recommended - Faster)
```bash
python main.py
```
- Uses YOLOv8 Nano for detection
- Best performance and speed
- Automatically falls back to detection when tracking fails

### Option 2: YOLOv3 Tracker (Alternative - More Accurate)
```bash
python submission.py
```
- Uses YOLOv3 for detection
- More accurate but slower than YOLOv8
- Square-box logic for scale-invariant tracking

### Controls

- **Q key**: Quit the tracker

## How It Works

### Detection Phase (Blue Box)
1. Frame is processed by YOLO model
2. Looks specifically for "sports ball" class (COCO class 32)
3. Returns bounding box when object is detected
4. Blue box is drawn on the frame

### Tracking Phase (Green Box)
1. CSRT tracker is initialized with the detected bounding box
2. Tracker updates on each subsequent frame
3. Green box follows the ball
4. More efficient than running detection every frame

### Failure Recovery (Red Text)
1. If tracker confidence drops or tracking fails
2. System falls back to detection mode
3. Searches for the ball again using YOLO
4. Resumes tracking when ball is re-detected

## Performance

- **Main.py** (YOLOv8n): ~30-60 FPS on CPU
- **Submission.py** (YOLOv3): ~15-30 FPS on CPU
- **GPU**: Significantly faster with CUDA support

## Model Information

### YOLOv8 Nano (`yolov8n.pt`)
- Size: ~13 MB
- Speed: Ultra-fast
- Accuracy: High
- Best for: Real-time applications

### YOLOv3 (`yolov3.cfg` + `yolov3.weights`)
- Size: ~237 MB (weights)
- Speed: Moderate
- Accuracy: Very high
- Best for: Accuracy-critical applications

## Troubleshooting

**Issue**: Video file not found
- **Solution**: Ensure `soccer-ball.mp4` is in the Output/ directory

**Issue**: Model not found
- **Solution**: Verify `yolo_files/` directory contains required model files

**Issue**: Slow processing
- **Solution**: Use main.py with YOLOv8n instead of submission.py
- Ensure you're using GPU if available (configure in code)

**Issue**: Import errors
- **Solution**: Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Dependencies Explained

- **opencv-python**: Core computer vision library
- **opencv-contrib-python**: Additional OpenCV modules (CSRT tracker)
- **numpy**: Numerical computing
- **ultralytics**: YOLOv8 implementation
- **torch**: Deep learning framework required by YOLO

## License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.

## Author

Created as part of the Fundamentals of OpenCV course at OpenCV University.

## References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [COCO Dataset](https://cocodataset.org/)
- [CSRT Tracker Paper](https://arxiv.org/abs/1611.08461)

---

**Last Updated**: April 2026