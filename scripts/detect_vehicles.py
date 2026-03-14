#!/usr/bin/env python3
import cv2
import os
from ultralytics import YOLO

input_dir  = "/home/ubuntu/catkin_ws/src/vehicle_detection/extracted_frames"
output_dir = "/home/ubuntu/catkin_ws/src/vehicle_detection/detection_results"
os.makedirs(output_dir, exist_ok=True)

model = YOLO('yolov8n.pt')
print("YOLOv8 model loaded.")

frames = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])
print(f"Processing {len(frames)} frames...")

for i, img_file in enumerate(frames):
    img = cv2.imread(os.path.join(input_dir, img_file))
    results = model(img, classes=[2, 5, 7], verbose=False, device='cpu')

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls  = model.names[int(box.cls[0])]
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, f"{cls} {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imwrite(os.path.join(output_dir, img_file), img)
    if (i+1) % 50 == 0:
        print(f"Processed {i+1}/{len(frames)} frames")

print("Detection complete!")
