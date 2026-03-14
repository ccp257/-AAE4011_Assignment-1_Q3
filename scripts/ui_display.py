#!/usr/bin/env python3
import cv2
import os

result_dir = "/home/ubuntu/catkin_ws/src/vehicle_detection/detection_results"
frames = sorted([f for f in os.listdir(result_dir) if f.endswith('.jpg')])

print(f"Found {len(frames)} frames. Press Q to quit.")

for f in frames:
    img = cv2.imread(os.path.join(result_dir, f))
    cv2.putText(img, f"Frame: {f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.imshow("Vehicle Detection", img)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
