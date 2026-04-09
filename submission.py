"""
Soccer Ball Detection and Tracking using YOLOv3 and CSRT
========================================================

This module implements an object detection and tracking system using:
- YOLOv3 for accurate object detection
- OpenCV's CSRT tracker for continuous tracking between detections
- Square bounding box logic for scale-invariant tracking

The system detects soccer balls (COCO class 32) and tracks them throughout video frames.
Blue bounding box indicates detection, green indicates tracking, red indicates tracking failure.

Usage:
    python submission.py
    
Press 'Q' to quit the application.

Note: This implementation uses YOLOv3 which is more accurate but slower than YOLOv8n.
For faster processing, use main.py instead.
"""

import cv2
import numpy as np
import sys

# --- CONFIGURATION ---
confThreshold = 0.4 
nmsThreshold = 0.4
inpWidth = 416      
inpHeight = 416


def getOutputsNames(net):
    """
    Get the names of output layers in the neural network.
    
    Args:
        net: OpenCV DNN network object
        
    Returns:
        list: Names of output layers
    """
    # Get all layer names
    layersNames = net.getLayerNames()
    # Get indices of the output layers
    out_layers = net.getUnconnectedOutLayers()
    
    # Handle different OpenCV version return types for getUnconnectedOutLayers
    if isinstance(out_layers[0], (list, np.ndarray)):
        return [layersNames[i[0] - 1] for i in out_layers]
    else:
        return [layersNames[i - 1] for i in out_layers]


def main():
    """Main execution function for the soccer ball tracker."""
    
    # --- LOAD MODEL ---
    try:
        net = cv2.dnn.readNetFromDarknet("yolo_files/yolov3.cfg", 
                                         "yolo_files/yolov3.weights")
    except cv2.error as e:
        print("ERROR: Failed to load YOLOv3 model")
        print(f"Ensure both yolov3.cfg and yolov3.weights are in yolo_files/ directory")
        print(f"Error: {e}")
        sys.exit(1)
    
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    tracker = None
    tracking_active = False
    
    video_path = "Output/soccer-ball.mp4"
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {video_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        print("Please ensure soccer-ball.mp4 is in the Output/ directory")
        sys.exit(1)

    print("--- Soccer Ball Tracker (YOLOv3 + CSRT) ---")
    print("Blue Box: Detection (YOLO)")
    print("Green Box: Tracking (CSRT)")
    print("Red Text: Tracking Lost/Searching")
    print("Press 'Q' to quit")
    print("-" * 45)

    frame_count = 0
    detection_count = 0
    tracking_count = 0

    while cap.isOpened():
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        
        frame_count += 1
        frameHeight, frameWidth = frame.shape[:2]

        if not tracking_active:
            # --- DETECTION PHASE (BLUE BOX) ---
            # We use swapRB=True because OpenCV reads in BGR, but YOLO was trained on RGB
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (inpWidth, inpHeight), 
                                         swapRB=True, crop=False)
            net.setInput(blob)
            
            try:
                outs = net.forward(getOutputsNames(net))
            except cv2.error as e:
                print("Internal DNN Error: Skipping frame due to shape inconsistency.")
                continue

            best_box = None
            max_conf = 0

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    classId = np.argmax(scores)
                    confidence = scores[classId]
                    
                    # Class 32 = sports ball
                    if classId == 32 and confidence > confThreshold:
                        if confidence > max_conf:
                            max_conf = confidence
                            centerX = int(detection[0] * frameWidth)
                            centerY = int(detection[1] * frameHeight)
                            w = int(detection[2] * frameWidth)
                            h = int(detection[3] * frameHeight)
                            
                            # SQUARE BOX LOGIC: Scale-invariant for far/near balls
                            side = max(w, h)
                            left = int(centerX - side / 2)
                            top = int(centerY - side / 2)
                            best_box = (left, top, side, side)

            if best_box:
                # DETECTION TASK: BLUE BOX FOR DETECTION
                l, t, s, s = best_box
                cv2.rectangle(frame, (l, t), (l+s, t+s), (255, 0, 0), 3)
                cv2.putText(frame, "DETECTION", (l, t-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                
                tracker = cv2.TrackerCSRT_create()
                tracker.init(frame, best_box)
                tracking_active = True
                detection_count += 1
            else:
                cv2.putText(frame, "SEARCHING", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
    
        else:
            # --- TRACKING PHASE (GREEN BOX) ---
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, "TRACKING", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                tracking_count += 1
            else:
                # TRACKING FAILURE: Display and recovery
                tracking_active = False
                cv2.putText(frame, "TRACKING LOST - RE-DETECTING", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Frame counter
        cv2.putText(frame, f"Frame: {frame_count}", (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Soccer Tracker Fusion", frame)
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
