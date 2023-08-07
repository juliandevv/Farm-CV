import cv2
import numpy as np
import LineDetector as detector
import os
import PreFiltering as filter

def LoadFromFolder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def DrawLines(image, lines):
    for i in range(len(lines)):
        pts = lines[i][0]
        cv2.line(image, (pts[0], pts[1]), (pts[2], pts[3]), (0, 255, 0))

displayImages = LoadFromFolder("Pictures")

maxLineGap = 400
slopeTolerance = 1
lineThreshold = 20
edgeThreshold1 = 100
edgeThreshold2 = 200

for image in displayImages:
    image = filter.ResizeImage(image, 50)
    width, height = image.shape[:2]
    image = image[10:height, 10:width]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    filtered = filter.PreFilter(image)
    edges = cv2.Canny(filtered, edgeThreshold1, edgeThreshold2)
    morphed = filter.Morph(edges, width)
    lines = detector.DetectLines(morphed, maxLineGap, lineThreshold)
    lines = detector.SlopeFilter(lines, slopeTolerance)
    DrawLines(image, lines)
 
    while True:
        cv2.imshow("Pre Filter", filtered)
        cv2.imshow("Morphed", morphed)
        cv2.imshow("Edges", edges)
        cv2.imshow("Lines", image)
        cv2.imshow("HSV", hsv)
        key = cv2.waitKey(1)
        if key == 32: break
        elif key == 27: break
    if key == 27: break
    