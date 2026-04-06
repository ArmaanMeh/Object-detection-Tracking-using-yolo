#!/usr/bin/env python
"""
Setup script for Soccer Ball Tracker
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="soccer-ball-tracker",
    version="1.0.0",
    author="OpenCV University Project",
    description="Real-time soccer ball detection and tracking using YOLOv8/YOLOv3 and CSRT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/soccer-ball-tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "soccer-tracker-yolov8=main:main",
            "soccer-tracker-yolov3=submission:main",
        ],
    },
)
