# Changelog

All notable changes to the Soccer Ball Tracker project will be documented in this file.

## [1.0.0] - 2026-04-06

### Added
- Initial release of Soccer Ball Tracker
- YOLOv8 Nano implementation for fast real-time detection (`main.py`)
- YOLOv3 implementation for accurate detection (`submission.py`)
- CSRT tracker for continuous object tracking
- Hybrid detection-tracking architecture with automatic failure recovery
- Real-time visualization with color-coded bounding boxes
  - Blue: Detection (YOLO)
  - Green: Tracking (CSRT)
  - Red: Tracking failure/searching
- Comprehensive error handling and validation
- Unit testing framework
- Complete documentation in README.md
- Contributing guidelines in CONTRIBUTING.md
- Configuration system in config.py
- Setup script for easy installation

### Technical Details
- Targets COCO class 32 (sports ball) for detection
- Uses square bounding boxes for scale-invariant tracking
- Supports both CPU and GPU processing
- Tested with Python 3.8+
- Compatible with Windows, macOS, and Linux

### Performance
- Main.py (YOLOv8n): ~30-60 FPS on CPU
- Submission.py (YOLOv3): ~15-30 FPS on CPU
- GPU acceleration available with CUDA-enabled PyTorch

### Known Limitations
- Requires `soccer-ball.mp4` in Output/ directory
- Model files must be pre-downloaded due to size constraints
- Currently optimized for soccer ball detection only
- CPU-based processing may be slower on low-end systems

## Future Improvements

### Planned for v1.1.0
- [ ] Custom model training capability
- [ ] Multi-object tracking support
- [ ] Video output export functionality
- [ ] Real-time FPS counter
- [ ] Configurable detection confidence threshold
- [ ] Support for different video formats

### Planned for v2.0.0
- [ ] Web interface for easy usage
- [ ] REST API for remote inference
- [ ] Mobile app support
- [ ] Cloud deployment options
- [ ] Advanced analytics and statistics

---

For more information, see [README.md](README.md)
