#!/usr/bin/env python3
"""
Simple labeling tool for bounding boxes.
Usage: python label_tool.py --images collected_screenshots/
"""
import cv2
import os
import argparse
import json

class LabelTool:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]
        self.current_idx = 0
        self.boxes = []  # list of (x1, y1, x2, y2, label)

    def run(self):
        cv2.namedWindow("LabelTool")
        cv2.setMouseCallback("LabelTool", self.mouse_callback)
        self.drawing = False
        self.start = None
        self.end = None

        while self.current_idx < len(self.image_paths):
            img = cv2.imread(self.image_paths[self.current_idx])
            self.display = img.copy()
            self.draw_boxes()
            cv2.imshow("LabelTool", self.display)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('s'):
                self.save_labels()
                self.current_idx += 1
                self.boxes.clear()
            elif key == ord('n'):
                self.current_idx += 1
                self.boxes.clear()
            elif key == ord('q'):
                break
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start = (x, y)
            self.end = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.end = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.boxes.append((self.start[0], self.start[1], self.end[0], self.end[1], "sprite"))
            self.start = None
            self.end = None

    def draw_boxes(self):
        for box in self.boxes:
            x1, y1, x2, y2, label = box
            cv2.rectangle(self.display, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(self.display, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    def save_labels(self):
        label_file = os.path.join(self.image_dir, "labels.json")
        existing = []
        if os.path.exists(label_file):
            with open(label_file, 'r') as f:
                existing = json.load(f)
        existing.append({
            "image": os.path.basename(self.image_paths[self.current_idx]),
            "boxes": self.boxes
        })
        with open(label_file, 'w') as f:
            json.dump(existing, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, help="Directory containing screenshots")
    args = parser.parse_args()
    tool = LabelTool(args.images)
    tool.run()
