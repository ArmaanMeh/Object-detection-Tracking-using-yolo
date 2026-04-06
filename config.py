# Project Configuration File
# 
# This file contains default constants and configuration values
# for the Soccer Ball Tracker project.

import os

# ============== Model Configuration ==============
# YOLOv8 Model settings
YOLOV8_MODEL_PATH = "yolo_files/yolov8n.pt"
YOLOV8_CONFIDENCE_THRESHOLD = 0.5

# YOLOv3 Model settings  
YOLOV3_CFG_PATH = "yolo_files/yolov3.cfg"
YOLOV3_WEIGHTS_PATH = "yolo_files/yolov3.weights"
YOLOV3_CONFIDENCE_THRESHOLD = 0.4
YOLOV3_NMS_THRESHOLD = 0.4
YOLOV3_INPUT_WIDTH = 416
YOLOV3_INPUT_HEIGHT = 416

# ============== COCO Classes ==============
# The class we're interested in tracking
TARGET_CLASS = 32  # sports ball
TARGET_CLASS_NAME = "sports ball"

# ============== Video Configuration ==============
VIDEO_PATH = "Output/soccer-ball.mp4"
OUTPUT_PATH = "Output/"

# ============== CSRT Tracker Configuration ==============
# OpenCV CSRT tracker (no hyperparameters - uses defaults)

# ============== UI Configuration ==============
WINDOW_NAME = "Soccer Ball Fusion Tracker"
DISPLAY_STATS = True

# Detection visualization
DETECTION_COLOR = (255, 0, 0)    # Blue (BGR format)
DETECTION_THICKNESS = 2
DETECTION_TEXT = "DETECTION"

# Tracking visualization
TRACKING_COLOR = (0, 255, 0)     # Green (BGR format)
TRACKING_THICKNESS = 2
TRACKING_TEXT = "TRACKING"

# Failure visualization
FAILURE_COLOR = (0, 0, 255)      # Red (BGR format)
FAILURE_THICKNESS = 2
FAILURE_TEXT = "TRACKING LOST"

# UI text
SEARCHING_TEXT = "SEARCHING..."
RE_DETECTING_TEXT = "RE-DETECTING"
STATUS_FONT = "cv2.FONT_HERSHEY_SIMPLEX"
STATUS_FONT_SCALE = 0.7
STATUS_THICKNESS = 2

# ============== Keymap ==============
QUIT_KEY = 'q'  # Press 'Q' to quit

# ============== Paths ==============
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
YOLO_FILES_DIR = os.path.join(PROJECT_ROOT, "yolo_files")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Output")
