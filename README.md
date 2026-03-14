# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

**Student Name:** Cheung Chun Pang | **Student ID:** 24036721D | **Date:** 14/3/2026

---

## 1. Overview

This project implements a complete ROS-based vehicle detection pipeline. Applies YOLOv8 object detection to identify vehicles, and visualises the results with bounding boxes and confidence scores through an OpenCV interface.

---

## 2. Detection Method

**Model:** YOLOv8n (You Only Look Once, version 8 — Nano variant)

YOLOv8 was selected because:
- Single-pass architecture enables real-time inference
- Pre-trained on COCO dataset, natively supporting car, bus, and truck classes
- Simple Python API via `ultralytics` library for easy ROS integration
- Lightweight nano variant suitable for resource-constrained drone platforms

Detection targets COCO classes: car (2), bus (5), truck (7).

---

## 3. Repository Structure

    vehicle_detection/
    |-- bags/                          |-- 2026-02-02-17-57-27.bag
    |-- demo_video/                    |-- Video 1
    |-- extracted_frames/              # Raw frames from Video 1
    |-- detection_results/             # Frames with bounding boxes
    |-- scripts/
    |   |-- extract_images.py          # Extract frames from Video 1
    |   |-- detect_vehicles.py         # Run YOLOv8 vehicle detection
    |   |-- ui_display.py              # Display detection results
    |-- README.md                      # Project documentation (this file)

---

## 4. Prerequisites

| Requirement | Version |
|---|---|
| OS | Ubuntu 20.04 |
| ROS | Noetic |
| Python | 3.8 |
| ultralytics | Latest |
| opencv-python | Latest |
| numpy | Latest |

Install all dependencies:

    pip3 install ultralytics opencv-python numpy
    sudo apt install ros-noetic-cv-bridge

---

## 5. How to Run

**Step 1: Clone the repository**

    cd ~/catkin_ws/src
    git clone https://github.com/[your-username]/vehicle_detection.git

**Step 2: Install dependencies**

    pip3 install ultralytics opencv-python numpy

**Step 3: Build the ROS package**

    cd ~/catkin_ws
    catkin_make
    source devel/setup.bash

**Step 4: Place the rosbag file**

    mkdir -p ~/catkin_ws/src/vehicle_detection/bags
    cp /path/to/2026-02-02-17-57-27.bag ~/catkin_ws/src/vehicle_detection/bags/

**Step 5: Launch the pipeline**

Terminal 1 — Start ROS Master:

    roscore

Terminal 2 — Extract frames from rosbag:

    python3 ~/catkin_ws/src/vehicle_detection/scripts/extract_images.py

Terminal 2 — Run YOLOv8 detection:

    python3 ~/catkin_ws/src/vehicle_detection/scripts/detect_vehicles.py

Terminal 3 — Display results UI:

    python3 ~/catkin_ws/src/vehicle_detection/scripts/ui_display.py

Press Q to quit the display window.

---

## 6. Sample Results

### Image Extraction Summary

| Property | Value |
|---|---|
| ROS Topic | /hikcamera/image_2/compressed |
| Message Type | sensor_msgs/CompressedImage |
| Total Frames Extracted | 1142 |
| Image Resolution | 1740 x 2200 pixels |
| Rosbag File Size | 918.5 MB |

### Detection Statistics

| Class | COCO ID | Description |
|---|---|---|
| car | 2 | Passenger vehicles |
| bus | 5 | Large passenger buses |
| truck | 7 | Freight trucks |

Bounding boxes are drawn with class label and confidence score on each detected vehicle. Results are saved as JPEG images in detection_results/.



---

## 7. Video Demonstration

Video Link: https://www.youtube.com/watch?v=YOHBc9Yaw98

The video demonstrates:
- (a) Launching the ROS package and running the detection pipeline
- (b) The UI displaying detection results with bounding boxes on rosbag images
- (c) A brief explanation of the detection results and observations

---

## 8. Reflection & Critical Analysis

### (a) What Did You Learn?
First, I learned what rosbag is. When a robot is running, various sensors (cameras, LiDAR, GPS, etc.) and algorithms constantly publish data (images, laser scans, coordinates, etc.). A rosbag file captures all of this streaming data and saves it to disk. This deepened my understanding of how ROS handles different sensor data formats.

Second, I gained practical experience in structuring and building a complete ROS catkin package from scratch, including writing a valid extract_images.py, ui_display.py, detect_vehicles.py, and launch files. Deploying a deep learning model (YOLOv8) as part of a ROS node gave me insight into integrating modern AI frameworks within robotics middleware.

### (b) How Did You Use AI Tools?

I used Perplexity AI as an assistant throughout this assignment to help generate code scaffolding, debug errors, and explain ROS concepts.
### (c) How to Improve Accuracy?

**Strategy 1 - Use a larger YOLOv8 model:**
Replacing yolov8n.pt with yolov8m.pt or yolov8l.pt would improve detection accuracy, particularly for small or partially occluded vehicles. The nano model trades accuracy for speed; medium and large variants have significantly more parameters, enabling better feature extraction for challenging cases such as distant vehicles or overlapping bounding boxes.

**Strategy 2 - Fine-tune on aerial/drone imagery:**
The COCO-pretrained model was trained on ground-level photographs. The rosbag camera captures a top-down aerial perspective, which differs substantially from training data. Fine-tuning YOLOv8 on a drone-specific dataset such as VisDrone would adapt the model to match this viewpoint, reducing false negatives for vehicles that appear small or foreshortened from above.

### (d) Real-World Challenges

**Challenge 1 - Onboard computational constraints:**
Deploying this pipeline on an actual drone requires real-time inference on embedded hardware such as an NVIDIA Jetson module. Processing 1740x2200 resolution frames on CPU is far too slow for real-time use. Even with GPU acceleration, hardware-software compatibility issues (as encountered in this assignment with CUDA versions) are a significant practical challenge. Solutions include model quantisation (INT8), image downscaling before inference, and TensorRT-optimised model exports.

**Challenge 2 - Motion blur and dynamic lighting:**
A drone in flight experiences constant vibration and rapid movement, introducing motion blur that degrades image quality and reduces detection confidence. Outdoor environments also have rapidly changing lighting conditions including shadows, direct sunlight glare, and varying illumination. Mitigation strategies include gimbal stabilisation, adaptive image preprocessing (CLAHE), and temporal tracking algorithms such as Kalman filter or DeepSORT to maintain vehicle identity across frames even when individual detections fail.

---

## 9. References

- Ultralytics YOLOv8: https://github.com/ultralytics/ultralytics
- ROS Noetic Documentation: https://wiki.ros.org/noetic
