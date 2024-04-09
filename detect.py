import cv2
import numpy as np
from tracking import cap_nhap, tracking_points
import tracking


def resize_image(src, new_height, new_width):
    old_height, old_width, _ = src.shape

    # Initialize empty arrays for drawings
    drawing = np.zeros((old_height, new_width, 3), np.uint8)
    drawing2 = np.zeros((new_height, new_width, 3), np.uint8)

    # Calculate the delta value
    delta = np.zeros((new_height, old_width), np.uint8)
    dx = old_width / new_width

    # Perform interpolation along the horizontal axis
    for y in range(old_height):
        for n in range(new_width):
            x = (n + 0.5) * dx - 0.5
            addr = int(x)
            x -= addr
            for k in range(3):
                drawing[y, n, k] = src[y, addr, k] * (1 - x) + src[y, addr + 1, k] * x

    # Perform interpolation along the vertical axis
    for x in range(new_width):
        for n in range(new_height):
            px = (n + 0.5) * (old_height / new_height) - 0.5
            addr = int(px)
            px -= addr
            if addr + 1 < old_height and x < old_width:
                for k in range(3):
                    drawing2[n, x, k] = drawing[addr, x, k] * (1 - px) + drawing[addr + 1, x, k] * px
    
    return drawing2
# for i in range(1,2):
#     for j in range (1,2):
# url = f'./dataset/subset0{i}/video{j:02}/video.h264'
url = './dataset/subset01/video01/video.h264'

cap = cv2.VideoCapture(url)
fps = cap.get(cv2.CAP_PROP_FPS)
object_detector = cv2.createBackgroundSubtractorMOG2(history=5)


frame_i = 0
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)
kernel = np.ones((5, 5), np.uint8)

w_max = 250
h_max = 350
w_limit = 70
h_limit = 140
# max_limit = 150

# w_limit = 60
# h_limit = 60
frame_count = 0
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,15))        
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(10)
    if not ret or key == ord('q'):
        break
    frame = resize_image(frame, 360, 640)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width, _ = frame.shape
    # print(height, width)
    # blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # median = cv2.medianBlur(gray, 7)
    blur = cv2.GaussianBlur(gray, (21,21), 0)

    
    roi_frame = frame
    mask = object_detector.apply(blur)
    _, mask = cv2.threshold(mask, 70, 255, cv2.THRESH_BINARY)
    dilation = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((7,15)))
    dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_ERODE, np.ones((7,15)))
    
    analysis = cv2.connectedComponentsWithStats(dilation2,8, cv2.CV_32S) 
    (totalLabels, label_ids, values, centroid) = analysis 
    

    print(f"Frame {frame_count}: ")
    center_points_cur_frame = []
    for ccl in range(1, totalLabels): 
        area = values[ccl, cv2.CC_STAT_AREA]  
        x = values[ccl, cv2.CC_STAT_LEFT] 
        y = values[ccl, cv2.CC_STAT_TOP] 
        w = values[ccl, cv2.CC_STAT_WIDTH] 
        h = values[ccl, cv2.CC_STAT_HEIGHT]
        if w_max >= w >= w_limit  and h_max >= h >= h_limit and y >= 30 and area <= 40000:  
            cv2.rectangle(roi_frame, (x, y), (x+w, y+h), (0,255,0), 5)
            # cv2.imshow('car', dilation2[y:y+h,x:x+w])
            center_point = (int(centroid[ccl][0]), int(centroid[ccl][1]))
            center_points_cur_frame.append(center_point) 
    cap_nhap(center_points_cur_frame)        
    for point in tracking_points:
        cv2.circle(roi_frame, point['point'],5, (0,0,255), -1)
        cv2.putText(roi_frame, f"#id {point['id']}", (point['point'][0]-10,point['point'][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,color =(0,0,255), thickness = 2)
        # with open('ketquaspeed.txt', 'a',  encoding='UTF-8') as file:
        #     file.write(f"xe id: {point['id']} speed: {speed}\n")
        if frame_count % 50 ==0 or point["speed"] == 0:
            dis = point['distance']
            point["speed"] = (dis * fps * 0.03 * 3.6)
            point["speed"] = round(point["speed"], 2)
        if x <300:
            cv2.putText(frame, f"#speed {point['speed']}", (point['point'][0]-40,point['point'][1]-40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,color =(0,255,255), thickness = 2)

    

    roi_frame = cv2.line(roi_frame, (0,30), (roi_frame.shape[1], 30), (0,0,255), thickness= 3)
    

    # cv2.imwrite(f"output_frame/SET{i}/video{j}/{frame_count}.jpg", frame)
    # cv2.imshow(f"gray", gray)
    
    cv2.imshow('mask', dilation2)
    cv2.imshow("video01", frame)
    frame_count += 1
tracking.id = 0
cap.release()
cv2.destroyAllWindows()