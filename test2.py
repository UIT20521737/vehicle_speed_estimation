import cv2
import numpy as np
import math
from tracking import cap_nhap, tracking_points
import tracking


def find_center(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    xc = x + x1
    yc = y + y1
    return (xc, yc)

# url = './dataset/video.mp4'
# url = './dataset/subset02/subset02a/video05/video.h264'
# url = './dataset/subset02/subset02b/video-005.h264'q
url = 'img1.jpg'
frame = cv2.imread(url)

object_detector = cv2.createBackgroundSubtractorMOG2(history=5)

kernel = np.ones((5, 5), np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

# blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
# blur = cv2.GaussianBlur(gray, (11,11), 0)
roi = blur
mask = object_detector.apply(roi)
_, mask = cv2.threshold(mask, 120, 255, cv2.THRESH_BINARY)
dilation = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, np.ones((15,15)))

cv2.imshow("Frame", dilation)
    
cv2.waitKey(0)