#!/usr/bin/env python3
# Import required libraries
import rosbag
import cv2
import numpy as np
import os

# Define input and output paths
bag_path   = "/home/ubuntu/catkin_ws/src/vehicle_detection/bags/2026-02-02-17-57-27.bag"
output_dir = "/home/ubuntu/catkin_ws/src/vehicle_detection/extracted_frames"
os.makedirs(output_dir, exist_ok=True)

print("Opening bag...")
bag = rosbag.Bag(bag_path)

# Display all topics available in the bag file for debugging/information
print("Topics in bag:")
for topic, info in bag.get_type_and_topic_info()[1].items():
    print(f"  {topic} ({info.msg_type})")

count = 0
# Iterate through all messages in the bag file
for topic, msg, t in bag.read_messages():
    if "image" in topic.lower():
        try:
            np_arr  = np.frombuffer(msg.data, np.uint8)
            cv_img  = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if cv_img is None:
                continue
            cv2.imwrite(f"{output_dir}/frame_{count:04d}.jpg", cv_img)
            count += 1
            if count % 50 == 0:
                print(f"  Extracted {count} frames...")
        except Exception as e:
            print(f"  Error: {e}")

# Print final statistics
print(f"\nTotal frames extracted: {count}")
if count > 0:
    print(f"Image size: {cv_img.shape}")
bag.close() # Always close the bag file to free resources
