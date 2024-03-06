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
for i in range(1,2):
    for j in range (1,3):
        url = f'./dataset/subset0{i}/video{j:02}/video.h264'
        cap = cv2.VideoCapture(url)
        fps = cap.get(cv2.CAP_PROP_FPS)
        object_detector = cv2.createBackgroundSubtractorMOG2(history=5)

        
        frame_i = 0
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        frame_size = (frame_width,frame_height)
        output = cv2.VideoWriter('./output_video/output.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), 30, frame_size)
        kernel = np.ones((5, 5), np.uint8)


        count_id = 0
        w_max = 250
        h_max = 350
        w_limit = 70
        h_limit = 140
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
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,15))        


            # dilation = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_DILATE, np.ones((5,5)))
            # dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_CLOSE, kernel)
                
            # dilation2 = cv2.dilate(dilation1, np.ones((5,5)))
            # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((1,15)))
        while True:
            ret, frame = cap.read()
            key = cv2.waitKey(10)
            if not ret or key == ord('q'):
                break
            frame = cv2.resize(frame, (frame.shape[1]//3, frame.shape[0]//3), frame)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width, _ = frame.shape
            # print(height, width)
            # blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            median = cv2.medianBlur(gray, 7)
            blur = cv2.GaussianBlur(median, (9,9), 0)
        
            
            roi_frame = frame
            mask = object_detector.apply(blur)
            _, mask = cv2.threshold(mask, 120, 255, cv2.THRESH_BINARY)
            dilation = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((7,15)))
            dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
            dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_ERODE, np.ones((7,15)))
           
            analysis = cv2.connectedComponentsWithStats(dilation2,8, cv2.CV_32S) 
            (totalLabels, label_ids, values, centroid) = analysis 
            

            print(f"Frame {frame_count}: ")
            center_points_cur_frame = []
            for ccl in range(1, totalLabels): 
                area = values[ccl, cv2.CC_STAT_AREA]   m 
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
            cv2.imshow(f"video{j}", frame)
            frame_count += 1
        tracking.id = 0
        cap.release()
        cv2.destroyAllWindows()