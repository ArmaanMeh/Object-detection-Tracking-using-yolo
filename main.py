"""
Soccer Ball Detection and Tracking using YOLOv8 and CSRT
========================================================

This module implements a hybrid object detection and tracking system that uses:
- YOLOv8 Nano for efficient real-time object detection
- OpenCV's CSRT tracker for continuous tracking between detections

The system detects soccer balls (COCO class 32) and tracks them throughout video frames.
Blue bounding box indicates detection, green indicates tracking, red indicates tracking failure.

Usage:
    python main.py
    
Press 'Q' to quit the application.
"""

import cv2
import numpy as np
from ultralytics import YOLO
import sys


def main():
    """Main execution function for the soccer ball tracker."""
    
    # 1. Setup Models and Video
    # Using YOLOv8n (nano) for maximum speed to beat TLD's performance
    try:
        model = YOLO('yolo_files/yolov8n.pt')
    except FileNotFoundError:
        print("ERROR: yolov8n.pt not found in yolo_files/ directory")
        print("Please ensure the model file exists at: yolo_files/yolov8n.pt")
        sys.exit(1)
    
    video_path = "Output/soccer-ball.mp4"
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {video_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        print("Please ensure soccer-ball.mp4 is in the Output/ directory")
        sys.exit(1)

    # Initialize OpenCV CSRT Tracker
    tracker = cv2.TrackerCSRT_create()
    tracking_active = False
    bbox = None

    print("--- Soccer Ball Tracker (YOLOv8 + CSRT) ---")
    print("Blue Box: Detection (YOLO)")
    print("Green Box: Tracking (CSRT)")
    print("Red Text: Tracking Lost/Searching")
    print("Press 'Q' to quit")
    print("-" * 45)

    frame_count = 0
    detection_count = 0
    tracking_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        display_text = "Status: "
        status_color = (255, 255, 255)  # White

        if not tracking_active:
            # --- DETECTION PHASE (BLUE BOX) ---
            # We only look for 'sports ball' (COCO class 32)
            results = model(frame, classes=[32], verbose=False)
            
            for r in results:
                boxes = r.boxes.xywh.cpu().numpy()
                if len(boxes) > 0:
                    # Get the first detected ball
                    x, y, w, h = boxes[0]
                    # Convert XYWH to top-left format for OpenCV
                    bbox = (int(x - w/2), int(y - h/2), int(w), int(h))
                    
                    # Initialize Tracker
                    tracker = cv2.TrackerCSRT_create()
                    tracker.init(frame, bbox)
                    tracking_active = True
                    detection_count += 1
                    
                    # Draw Blue Box for Detection
                    cv2.rectangle(frame, (bbox[0], bbox[1]), 
                                (bbox[0]+bbox[2], bbox[1]+bbox[3]), (255, 0, 0), 2)
                    display_text += "DETECTING (YOLO)"
                    status_color = (255, 0, 0)  # Blue
                    break
            else:
                display_text += "SEARCHING..."
                status_color = (200, 200, 0)  # Cyan
        
        else:
            # --- TRACKING PHASE (GREEN BOX) ---
            success, bbox = tracker.update(frame)
            
            if success:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)
                display_text += "TRACKING (CSRT)"
                status_color = (0, 255, 0)  # Green
                tracking_count += 1
            else:
                # --- TRACKING FAILURE (RED TEXT) ---
                tracking_active = False
                display_text += "TRACKING FAILED - RE-DETECTING"
                status_color = (0, 0, 255)  # Red

        # UI Overlay
        cv2.putText(frame, display_text, (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, f"Frame: {frame_count}", (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("Soccer Ball Fusion Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("-" * 45)
    print(f"Video processed: {frame_count} frames")
    print(f"Detections: {detection_count}")
    print(f"Tracking frames: {tracking_count}")
    print("Done!")


if __name__ == "__main__":
    main()
