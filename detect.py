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
url = './dataset/subset02/video05/video.h264'
cap = cv2.VideoCapture(url)

object_detector = cv2.createBackgroundSubtractorMOG2(history=5)

frame_i = 0
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)
output = cv2.VideoWriter('./output_video/output.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), 30, frame_size)

kernel = np.ones((5, 5), np.uint8)


count_id = 0
w_max = 800
h_max = 1000
w_limit = 300
h_limit = 400
# max_limit = 150

# w_limit = 60
# h_limit = 60
count = 0
center_points_prev_frame = []
tracking_objects = {}
track_id = 0
frame_count = 0
cout = 0
car = 0
k = 0
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

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
    # blur = cv2.GaussianBlur(gray, (5,5), 0)
    blur = cv2.GaussianBlur(gray, (11,11), 0)
    roi = blur
    roi_frame = frame
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 120, 255, cv2.THRESH_BINARY)
    # dilation = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((15,2)))
    # dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)   
    # dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_ERODE, np.ones((5,10)))
    dilation = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_DILATE, np.ones((5,5)))
    dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_CLOSE, kernel)
        
    # dilation2 = cv2.dilate(dilation1, np.ones((5,5)))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((1,15)))
    contours, _ = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Frame {frame_count}: ")
    center_points_cur_frame = []
   
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.drawContours(roi_frame,[cnt],-1,color=(0,255,0))
        # print(x, y, w, h)
        if w_max >= w >= w_limit  and h_max >= h >= h_limit and y >= 250:
            bounding = roi_frame[y:y+h,x:x+w]
            cv2.rectangle(roi_frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.imwrite(f'./img/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            cv2.imshow('car', mask[y:y+h,x:x+w])
            cv2.imwrite(f'./new_mask/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            center = find_center(x, y, w, h)
            print(">>> center",center)
            center_points_cur_frame.append(center) 
            
    cap_nhap(center_points_cur_frame)
    for point in tracking_points:
        print(">>> id: ",point['id'],"life_cycle: ",point["life_cycle"])
        cv2.circle(roi_frame, point['point'],5, (0,0,255), -1)
        cv2.putText(roi_frame, f"#id {point['id']}", (point['point'][0]-10,point['point'][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,color =(255,0,255), thickness = 2) 
    # if count == 1500:
    #     break
    roi_frame = cv2.line(roi_frame, (0,150), (roi_frame.shape[1], 150), (0,0,255), thickness= 3)
    roi_frame = cv2.line(roi_frame, (0,430), (roi_frame.shape[1], 430), (0,255,255), thickness= 3)
    
    cv2.imshow("Frame", frame)
    cv2.imshow('mask', dilation2)
    # cv2.imwrite(f'./output_frame/set2/video1/{frame_count}.jpg', roi_frame)
    frame_count += 1
    center_points_prev_frame = center_points_cur_frame.copy()
print("tong so phuong tien: ", tracking.id)
cap.release()
cv2.destroyAllWindows()