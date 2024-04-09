import cv2
import numpy as np
import math
from tracking import cap_nhap, tracking_points
import tracking
def findcontours_copy(binary, y, x):
    #print("--------------START----------------")
    #print(y, x)
    # ymin = y
    # ymax = y
    # xmin = x
    # xmax = x
    binary[y, x] = 100
    while (binary[y-1,x-1] == 255 or binary[y-1,x] == 255 or binary[y-1,x+1] == 255 or
           binary[y,x-1] == 255 or binary[y,x+1] == 255 or
           binary[y+1,x-1] == 255 or binary[y+1,x] == 255 or binary[y+1,x+1] == 255
           ):
            #print("Start IF: ")
            if binary[y-1,x-1] == 255 and binary[y,x-1] == 0:
                x = x-1
                y = y-1
                #print("1",y, x)
            elif binary[y-1,x] == 255 and binary[y-1,x-1] == 0:
                y = y-1
                #print("2",y, x)
            elif binary[y-1,x+1] == 255 and binary[y-1,x] == 0:
                x = x+1
                y = y-1
                #print("3",y, x)
            elif binary[y,x-1] == 255 and binary[y+1,x-1] == 0:
                x = x-1
                #print("4",y, x)
            elif binary[y,x+1] == 255 and binary[y-1,x+1] == 0:
                x = x+1
                #print("6",y, x)
            elif binary[y+1,x-1] == 255 and binary[y+1,x] == 0:
                x = x-1
                y = y+1
                #print("7",y, x)
            elif binary[y+1,x] == 255 and binary[y+1,x+1] == 0:
                x = x
                y = y+1
                #print("8",y, x)
            elif binary[y+1,x+1] == 255 and binary[y,x+1] == 0:
                x = x+1
                y = y+1
                #print("9",y, x)
            else:
                break
            binary[y,x] = 100
            #print("---------------END IF: ")                                       
    binary[y,x] = 100
    return binary#, ymin, ymax, xmin, xmax
def find_center(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    xc = x + x1
    yc = y + y1
    return (xc, yc)
for i in range(1,2):
    for j in range (1,2):
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
        w_max = 270
        h_max = 310
        w_limit = 60
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
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,3))
        while True:
            ret, frame = cap.read()
            
            count += 1
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
            blur = cv2.GaussianBlur(median, (5,5), 0)
        
            roi = blur
            roi_frame = frame
            mask = object_detector.apply(roi)
            _, mask = cv2.threshold(mask, 120, 255, cv2.THRESH_BINARY)
            dilation = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((15,15)))
            dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)   
            dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_ERODE, np.ones((15,15)))
            
            # dilation = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_DILATE, np.ones((5,5)))
            # dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_CLOSE, kernel)
                
            # dilation2 = cv2.dilate(dilation1, np.ones((5,5)))
            # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((1,15)))
            
            
            print(f"Frame {frame_count}: ")
            center_points_cur_frame = []
            
            for y in range(2, dilation2.shape[0]-2):
                for x in range(2, dilation2.shape[1]-2):
                    if (dilation2[y,x] == 255 and dilation2[y,x-1] == 0) :
                            dilation2 = findcontours_copy(dilation2, y, x)
                            x,y,w,h = cv2.boundingRect(dilation2)
                            if w_max >= w >= w_limit  and h_max >= h >= h_limit and y >= 30:
                                cv2.rectangle(roi_frame, (x,y), (x+w,y+h), (0,255,0), 5)
                    # with open('w.txt', 'a',  encoding='UTF-8') as file:
                    #     file.write(f'{w}\n')
                    # with open('h.txt', 'a',  encoding='UTF-8') as files:
                    #     files.write(f'{h}\n')
                    # for point in tracking_points:
                    #     with open('wh.txt', 'a',  encoding='UTF-8') as filess:
                    #         filess.write(f"{point['id']}_{w*h}\n")
                    # bounding = roi_frame[y:y+h,x:x+w]
                    # cv2.rectangle(roi_frame, (x, y), (w, h), (0,255,0), 5)
                    # # cv2.imshow('car', mask[y:y+h,x:x+w])
                    # car += 1
                    # center = find_center(x, y, w, h)
                    # print(">>> center",center)
                    # center_points_cur_frame.append(center) 
            cap_nhap(center_points_cur_frame)        
                    
            
            for point in tracking_points:
                # print(point)
                cv2.circle(roi_frame, point['point'],5, (0,0,255), -1)
                cv2.putText(roi_frame, f"#id {point['id']}", (point['point'][0]-10,point['point'][1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,color =(0,0,255), thickness = 2)
                
                # with open('ketquaspeed.txt', 'a',  encoding='UTF-8') as file:
                #     file.write(f"xe id: {point['id']} speed: {speed}\n")
                
                
                if frame_count % 50 ==0 or point["speed"] == 0:
                    x = point['distance']
                    point["speed"] = (x * fps * 0.03 * 3.6)
                    point["speed"] = round(point["speed"], 2)
                if x <300:
                    cv2.putText(frame, f"#speed {point['speed']}", (point['point'][0]-40,point['point'][1]-40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,color =(0,255,255), thickness = 2)
        
            # print(frame.shape)    
            roi_frame = cv2.line(roi_frame, (0,30), (roi_frame.shape[1], 30), (0,0,255), thickness= 3)
            roi_frame = cv2.line(roi_frame, (0,300), (roi_frame.shape[1], 300), (0,0,255), thickness= 3)
           
            cv2.imwrite(f"output_frame/SET{i}/video{j}/{frame_count}.jpg", frame)
            # cv2.imshow(f"gray", gray)
            cv2.imshow(f"video{j}", frame)
            # cv2.imshow('mask', dilation2)
            frame_count += 1
            center_points_prev_frame = center_points_cur_frame.copy()
        print("tong so phuong tien: {j}", tracking.id)
        # with open('ketqua.txt', 'a',  encoding='UTF-8') as file:
        #     file.write(f'tong so phuong tien của set{i} video {j}: {tracking.id}\n')
        tracking.id = 0
        cap.release()
        cv2.destroyAllWindows()