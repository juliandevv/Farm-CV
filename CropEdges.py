import cv2
import numpy as np
import LineDetector as detector
import matplotlib.pyplot as plt

def ResizeImage(img, scale):
    scale_percent = scale # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def GreenFilter(img):
    lower_green = np.array([50,100,50])
    upper_green = np.array([70,255,255])

    #Green filter
    mask_green = cv2.inRange(img, (0, 70, 50), (10, 255, 255))
    greenImage = cv2.bitwise_and(img, img, mask=mask_green)
    return greenImage

def RedFilter(img):
    mask_green = cv2.inRange(img, (0, 70, 50), (10, 255, 255))

    #redImage = cv2.bitwise_and(img, img, mask=mask_)
    #greenRedImage = cv2.bitwise_and(img, redImage, mask=mask_green)
    return redImage


image = ResizeImage(cv2.imread("Pictures/OldSala.jpg"), 30)
width, height = image.shape[:2]
cropFactor = 200
slopeTolerance = 1
croppedImage = image[cropFactor:height, 0:width]
#redImage = RedFilter(croppedImage)
greenImage = GreenFilter(croppedImage)

grayImage = cv2.cvtColor(greenImage, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(grayImage, threshold1=50, threshold2=150, L2gradient=True, apertureSize=3)

lines = detector.DetectLines(greenImage, 400)

avgLine = detector.AverageLines(lines)
#cv2.line(image, (avgLine[0]), (avgLine[1]), thickness=3, color=(0, 0, 255))

for i in range(len(lines)):
    for x1, y1, x2, y2 in lines[i]:
            if x1 == x2:
                continue
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))

    if slope > -slopeTolerance and slope < slopeTolerance:
        lines[i] = 0

    pts = lines[i][0]
    cv2.line(image, (pts[0], pts[1]+cropFactor), (pts[2], pts[3]+cropFactor), (0, 255, 0))

while True:

    #cv2.imshow("Red Filter", redImage)
    cv2.imshow("Green Filter", greenImage)
    cv2.imshow("Original", image)
    cv2.imshow("Edges", edges)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cv2.imwrite("Lines2.jpg", image)
# imgPlot = plt.imshow(edges)
# plt.show()