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

def GreenRedFilter(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
    mask_red = cv2.inRange(hsv, (30,150,50), (255,255,180))

    mask = cv2.bitwise_or(mask_green, mask_red)
    filtered = cv2.bitwise_and(img, img, mask=mask)

    return filtered

def Morph(img, width):
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(width / 30), 1))
    dilatingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 7))
    openingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilating = cv2.dilate(img, dilatingKernel)
    #closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(dilating, cv2.MORPH_OPEN, openingKernel)

    return opening


def PreFilter(image):
    greenImage = GreenRedFilter(image)
    grayImage = cv2.cvtColor(greenImage, cv2.COLOR_BGR2GRAY)
    return grayImage