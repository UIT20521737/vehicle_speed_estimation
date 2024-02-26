import cv2
import numpy as np
import math



# url = './dataset/video.mp4'
url = './dataset/subset01/video03/video.h264'
cap = cv2.VideoCapture(url)
ret, frame = cap.read()
# frame = cv2.resize(frame, (frame.shape[1]//3, frame.shape[0]//3), frame)
frame = cv2.line(frame, (85,10), (frame.shape[1]-195, 10), (0,0,255), thickness= 1)
frame = cv2.line(frame, (48,101), (frame.shape[1]-130, 101), (0,0,255), thickness= 1)

print(frame.shape)
cv2.imshow("frame",frame)
cv2.waitKey(0)
