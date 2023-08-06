import cv2
import numpy as np

def DetectLines(img, maxLineGap, lineThreshold):
    #grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lines = []
    rho = 1              #Distance resolution of the accumulator in pixels.
    theta = np.pi/180    #Angle resolution of the accumulator in radians.
    threshold = lineThreshold       #Only lines that are greater than threshold will be returned.
    minLineLength = 20   #Line segments shorter than that are rejected.
    maxLineGap = maxLineGap     #Maximum allowed gap between points on the same line to link them
    lines = cv2.HoughLinesP(img, rho = rho, theta = theta, threshold = threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)
    if lines is None: return []
    return lines
    

# def AverageLines(lines, img):
#     slopesAndIntercepts = []
#     lengths = []
#     width, height = img.shape[:2]

#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             if x1 == x2:
#                 continue
#             slope = (y2 - y1) / (x2 - x1)
#             intercept = y1 - (slope * x1)
#             length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
            
#             slopesAndIntercepts.append((slope, intercept))
#             lengths.append(length)
    
#     avgline = np.dot(lengths, slopesAndIntercepts) / np.sum(lengths)
    
#     y1 = img.shape[0]
#     y2 = 0

#     slope, intercept = avgline
#     x1 = int((y1 - intercept)/slope)
#     x2 = int((y2 - intercept)/slope)
#     y1 = int(y1)
#     y2 = int(y2)
#     return ((x1, y1), (x2, y2))

def AverageLines(lines):
    x1s = []
    x2s = []
    y1s = []
    y2s = []

    n = len(lines)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            x1s.append(x1)
            x2s.append(x2)
            y1s.append(y1)
            y2s.append(y2)

    avgx1 = np.sum(x1s) / n
    avgx2 = np.sum(x2s) / n
    avgy1 = np.sum(y1s) / n
    avgy2 =np.sum(y2s) / n

    return ((int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)))

def SlopeFilter(lines, slopeTolerance):
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
                # if x1 == x2:
                #     continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - (slope * x1)
                length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))

        if slope > -slopeTolerance and slope < slopeTolerance:
            lines[i] = 0
    return lines
    
