import cv2
import numpy as np
from object_tracker import CentroidTracker
import math

def find_center(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    xc = x + x1
    yc = y + y1
    return (xc, yc)

# url = './dataset/video.mp4'
url = './dataset/subset02/subset02a/video04/video.h264'
# url = './dataset/subset01/video04/video.h264'
cap = cv2.VideoCapture(url)

object_detector = cv2.createBackgroundSubtractorMOG2()
cen = CentroidTracker()

frame_i = 0
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)
output = cv2.VideoWriter('./output_video/output.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), 30, frame_size)

kernel = np.ones((5, 5), np.uint8)


count_id = 0
max_limit = 700

w_limit = 300
h_limit = 300
# max_limit = 150

# w_limit = 60
# h_limit = 60
count = 0
center_points_prev_frame = []
tracking_objects = {}
track_id = 0
frame_count = 0
while True:
    
    ret, frame = cap.read()
    count += 1
    key = cv2.waitKey(10)
    if not ret or key == ord('q'):
        break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width, _ = frame.shape
    # print(height, width)
    # blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    roi = blur
    roi_frame = frame
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 120, 255, cv2.THRESH_BINARY)
    dilation = cv2.dilate(mask, np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((1,15)))
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Frame {frame_i}: ")
    center_points_cur_frame = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # print(x, y, w, h)
        if max_limit >= w >= w_limit  and max_limit >= h >= h_limit:
            # cv2.drawContours(roi_frame, [cnt], 0, (0,255,0), 2)
            bounding = roi_frame[y:y+h,x:x+w]
            cv2.rectangle(roi_frame, (x, y), (x+w, y+h), (0,255,0), 2)
            # print( (x, y), (x+w, y+h))
            cv2.imwrite(f'./img/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            cv2.imshow('roi frame', mask[y:y+h,x:x+w])
            cv2.imwrite(f'./new_mask/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            center = find_center(x, y, w, h)
            center_points_cur_frame.append(center)
    cv2.imshow("Frame", frame)
    cv2.imshow('mask', dilation2)
    cv2.imwrite(f'output/{frame_count}.jpg', roi_frame)
    frame_count += 1
    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()
    
cap.release()
cv2.destroyAllWindows()