import cv2
import numpy as np
import LineDetector as detector
import os
import PreFiltering as filter

def DrawLines(image, lines):
    for i in range(len(lines)):
        pts = lines[i][0]
        cv2.line(image, (pts[0], pts[1]), (pts[2], pts[3]), (0, 255, 0))

def ProcessFrame(frame):
    frame = filter.ResizeImage(frame, 30)
    width, height = frame.shape[:2]
    frame = frame[300:height, :width]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    filtered = filter.PreFilter(frame)
    edges = cv2.Canny(filtered, 100, 200)
    morphed = filter.Morph(edges, width)
    lines = detector.DetectLines(morphed, 400, 20)
    lines = detector.SlopeFilter(lines, 1)
    DrawLines(frame, lines)

videoCapture = cv2.VideoCapture("Videos/Carrots.avi")

while videoCapture.isOpened():

    success, frame = videoCapture.read()

    if success:
        cv2.imshow("Frame1", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

        elif key == 32:

            while True:
                ProcessFrame(frame)
                #cv2.imshow("Processed Frame", frame)

                key = cv2.waitKey(1)
                if key == 32:
                    #cv2.destroyWindow("Paused Frame")
                    break

    else:
        break

videoCapture.release()
cv2.destroyAllWindows()