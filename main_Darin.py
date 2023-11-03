import cv2
import numpy as np #import lib numpy, allow work with array and matrix
from time import sleep

width_min = 300 #Minimum rectangle width (largura_min=80)
height_min = 300 #Minimum rectangle height (altura_min=80)

delay= 60 #video FPS

detec = []
"""
def take_center(x, y, w, h):  
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy
"""
url = './dataset/subset01/video03/video.h264'
cap = cv2.VideoCapture(url)
n = 0
subtract = cv2.createBackgroundSubtractorMOG2()
while True:
    #======= PRE-PROCESSING ========
    ret , frame1 = cap.read() #Read a frame from video and save on "frame", "ret" is True if frame will be read successful and False if opposite
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("grey" , grey)
    # sobelx = cv2.Sobel(grey, -1, 1, 0, ksize=3)
    # cv2.imshow("sobelx",sobelx)
    blur = cv2.GaussianBlur(grey,(3,3),0)
    #cv2.imshow("blur" , blur)
    img_sub = subtract.apply(blur)
    #img_sub = cv2.medianBlur(img_sub,7)
    #cv2.imshow('img_sub',img_sub)
    #cv2.imwrite(f'PicDetect/sub{i}.jpg', img_sub)
    #i += 1
    ret2,th2 = cv2.threshold(img_sub,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow('Binary',th2)
    dilation = cv2.dilate(th2,np.ones((3,3)))
    #cv2.imshow('dilation',dilation)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilation1 = cv2.morphologyEx (dilation, cv2.MORPH_CLOSE , kernel)
    #cv2.imshow('dilation1',dilation1)
    dilation2 = cv2.morphologyEx (dilation1, cv2.MORPH_CLOSE , kernel)
    #cv2.imshow('dilation2',dilation2)
    
    #======= FIND BOUNDING BOX ========
    #=== Fine line in image and loop ===
    bounding, h=cv2.findContours(dilation2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(bounding):
        # if cv2.contourArea(c) < 20000:
        #     continue
        (x,y,w,h) = cv2.boundingRect(c)
        #=== define border in threshold of min width and min height ===
        bounding_box = (w >= width_min and w < 600) and (h >= height_min and h < 600)
        if not bounding_box:
            continue
        #==== Draw bounding box and caculate the center ====
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        #center = take_center(x, y, w, h)
        #==== Save "center" in list "detect"
        #detec.append(center)

        #======= EXPORT OBJECT'S IMAGE ======= 
        object_image = frame1[y:y+h, x:x+w]
        #cv2.imshow('Object {}'.format(i), object_image)
        # Save the object image
        # cv2.imwrite('PicDetect/object_{}.jpg'.format(i+115), object_image)

        #======= LICENSE PLATE EXTRACTION =======
        gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("IMG",gray)
        closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((1,15)))
        #cv2.imshow("closing",closing)
        sub = cv2.subtract(closing, gray)
        #cv2.imshow("sub",sub)
        _, binary_img = cv2.threshold(sub, 0, 255, cv2.THRESH_OTSU)
        #cv2.imshow("binary_img",binary_img)
        closing1 = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, np.ones((3,3)))
        #cv2.imshow("cl1",closing1)

        #===== background cleaning =====
        closing2 = cv2.morphologyEx(closing1, cv2.MORPH_CLOSE, np.ones((5,10)))
        #cv2.imshow("cl2",closing2)
        opening = cv2.morphologyEx(closing2, cv2.MORPH_OPEN, np.ones((6,10)))
        #cv2.imshow("opening",opening)
        dilated = cv2.dilate(opening, np.ones((3,7)))
        #cv2.imshow("dilated",dilated)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_vertical_edges = 0
        image_with_max_edges = None
        xt = 0
        yt = 0
        wt = 0
        ht = 0
        for(i,c) in enumerate(contours):
            (x,y,w,h) = cv2.boundingRect(c)
            aspect_ratio = w / float(h)
            if (2 < aspect_ratio <= 7) and (100 < cv2.contourArea(c) < 1000):
                #boxes.append((x, y, w, h))
                #cv2.rectangle(object_image,(x - 5, y - 5),(x + w + 5, y + h + 5),(0,0,255),1)
                plate_candidate = object_image[y:y+h, x:x+w]
                #cv2.imshow('NP{}'.format(i), num_plate)
                gray_np = cv2.cvtColor(plate_candidate, cv2.COLOR_BGR2GRAY)
                _, binary_img = cv2.threshold(gray_np, 0, 255, cv2.THRESH_OTSU)
               
                #======= Find number plate with max vertical edges ========
                sobelx = cv2.Sobel(binary_img, -1, 1, 0, ksize=3)
                # threshold create binary image
                threshold = 100
                edges = cv2.threshold(np.abs(sobelx), threshold, 255, cv2.THRESH_BINARY)[1]
                #cv2.imshow("edges" , edges)
                # Caculate number of vertical edges
                vertical_edges_count = np.sum(edges > 0)
                #cv2.imshow('vertical_edges_y{}'.format(i),vertical_edges_count)
                if vertical_edges_count > max_vertical_edges:
                    max_vertical_edges = vertical_edges_count
                    image_with_max_edges = plate_candidate
                    xt = x
                    yt = y
                    wt = w
                    ht = h
        cv2.rectangle(object_image,(xt - 5, yt - 5),(xt + wt + 5, yt + ht + 5),(255,0,0),2)
        number_plate = object_image[yt:yt+ht, xt:xt+wt]
        if number_plate is not None and number_plate.size > 0:
            new_image = cv2.resize(number_plate,(200, 80))
            gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
            _,num_thrs = cv2.threshold(gray,0.0,255.0,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
            #erodethresh = cv2.erode(num_thrs, np.ones((5, 5)))
            cv2.imwrite('PicDetect/object_{}.jpg'.format(n), num_thrs)
    n = n + 1  
    
    cv2.imshow("Video dilate" , frame1)
    if cv2.waitKey(1) == 27:
        break

cap.release()
