import cv2
import numpy as np
from object_tracker import CentroidTracker


def find_center(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    xc = x + x1
    yc = y + y1
    return (xc, yc)

url = './datasets/video5.mp4'
cap = cv2.VideoCapture(url)

object_detector = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
cen = CentroidTracker()

frame_i = 0
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)
output = cv2.VideoWriter('./output_video/output.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), 30, frame_size)

kernel = np.ones((5, 5), np.uint8)


count_id = 0
max_limit = 15000
min_limit = 2000
w_limit = 120
h_limit = 120
while True:
    ret, frame = cap.read()

    key = cv2.waitKey(10)
    if not ret or key == ord('q'):
        break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width, _ = frame.shape
    # print(height, width)
    # blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11,11), 0)
    roi = blur[200:700,:]
    roi_frame = frame[200:,:]
    
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 70, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((1,15)))
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Frame {frame_i}: ")
    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # print(x, y, w, h)
        if  max_limit >= cv2.contourArea(cnt) >= min_limit or w >= w_limit and h >= h_limit:
            # cv2.drawContours(roi_frame, [cnt], 0, (0,255,0), 2)
            bounding = roi_frame[y:y+h,x:x+w]
            cv2.rectangle(roi_frame, (x, y), (x+w, y+h), (0,255,0), 2)
            # print( (x, y), (x+w, y+h))
            cv2.imwrite(f'./img/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            cv2.imshow('roi frame', mask[y:y+h,x:x+w])
            cv2.imwrite(f'./new_mask/{frame_i}.jpg',  roi_frame[y:y+h,x:x+w])
            center = find_center(x, y, w, h)
            rects.append(center)
            
    cen.objects = cen.update(rects)
    for i in cen.objects:
        cv2.circle(roi_frame, cen.objects[i],5, (0,0,255), -1)
        cv2.putText(roi_frame, f'#id {i}', (cen.objects[i][0]-10,cen.objects[i][1]-10),cv2.FONT_HERSHEY_SIMPLEX, 1,color =(255,0,255), thickness = 2)
    frame_i += 1
            # bounding = roi_frame[y:y+h,x:x+w]
            # bounding = cv2.putText(bounding, str(i), (50, 50), cv2.FONT_HERSHEY_SIMPLEX ,  1, (25,70,255), 1, cv2.LINE_AA) 
            # i+=1
            # gray = cv2.cvtColor(bounding, cv2.COLOR_BGR2GRAY)
            # closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((1,15)))
            # sub = cv2.subtract(closing, gray)
            # _, binary_img = cv2.threshold(sub, 0, 255, cv2.THRESH_OTSU)
            # closing1 = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, np.ones((3,3)))
            # closing2 = cv2.morphologyEx(closing1, cv2.MORPH_CLOSE, np.ones((5,10)))
            # opening = cv2.morphologyEx(closing2, cv2.MORPH_OPEN, np.ones((6,10)))
            # dilated = cv2.dilate(opening, np.ones((3,7)))
            
            # contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # max_vertical_edges = 0
            # image_with_max_edges = None
            # xt = 0
            # yt = 0
            # wt = 0
            # ht = 0
            # count_id+=1
            # for(i,c) in enumerate(contours):
            #     # cv2.drawContours(bounding, [c], 0, (0,255,0), 2)
            #     (x,y,w,h) = cv2.boundingRect(c)
            #     aspect_ratio = w / float(h)
            #     if (2 < aspect_ratio <= 7) and (100 < cv2.contourArea(c) < 1000):
            #         #boxes.append((x, y, w, h))
            #         # cv2.rectangle(bounding,(x - 5, y - 5),(x + w + 5, y + h + 5),(0,0,255),1)
            #         plate_candidate = bounding[y:y+h, x:x+w]
            #         gray_np = cv2.cvtColor(plate_candidate, cv2.COLOR_BGR2GRAY)
            #         sobelx = cv2.Sobel(binary_img, -1, 1, 0, ksize=3)
            #         _, binary_img = cv2.threshold(gray_np, 0, 255, cv2.THRESH_OTSU)
            #         threshold = 100
            #         edges = cv2.threshold(np.abs(sobelx), threshold, 255, cv2.THRESH_BINARY)[1]
            #         vertical_edges_count = np.sum(edges > 0)
            #         print("vertical: ",vertical_edges_count)
            #         if vertical_edges_count > max_vertical_edges:
            #             max_vertical_edges = vertical_edges_count
            #             image_with_max_edges = plate_candidate
            #             xt = x
            #             yt = y
            #             wt = w
            #             ht = h
            #             cv2.rectangle(bounding,(xt - 5, yt - 5),(xt + wt + 5, yt + ht + 5),(255,0,0),2)
                        
            
    cv2.imshow('roi', roi_frame)
    cv2.imshow('frame', frame)
    # cv2.imshow('blur', blur)
    cv2.imshow('mask', mask)
    output.write(frame)
    



cap.release()
cv2.destroyAllWindows()

