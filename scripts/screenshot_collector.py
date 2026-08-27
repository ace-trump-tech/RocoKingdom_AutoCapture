#!/usr/bin/env python3
"""
Batch screenshot collector for training data.
Press 'c' to capture, 'q' to quit.
"""
import cv2
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.capture.screen_grabber import ScreenGrabber

def main():
    grabber = ScreenGrabber()
    save_dir = "collected_screenshots"
    os.makedirs(save_dir, exist_ok=True)

    print("Press 'c' to capture screenshot, 'q' to quit.")
    count = 0
    while True:
        img = grabber.capture()
        cv2.imshow("Screen Capture", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            filename = os.path.join(save_dir, f"capture_{count:04d}.png")
            cv2.imwrite(filename, img)
            print(f"Saved {filename}")
            count += 1
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
