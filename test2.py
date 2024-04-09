import cv2
import numpy as np
import math


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
url1 = './dataset/tainghe.jpg'
url2 = './dataset/nen1.jpg'
frame1 = cv2.imread(url2)
frame2 = cv2.imread(url1)
frame1 = cv2.resize(frame1, (frame1.shape[1]//5, frame1.shape[0]//5), frame1)
frame2 = cv2.resize(frame2, (frame2.shape[1]//5, frame2.shape[0]//5), frame2)
frame = frame2 - frame1
cv2.imshow("Frame", frame)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,3))
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
median = cv2.medianBlur(gray, 7)
blur = cv2.GaussianBlur(median, (5,5), 0)
roi = blur
roi_frame = frame2
_, mask = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
dilation = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((15,15)))
dilation1 = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)   
dilation2 = cv2.morphologyEx(dilation1, cv2.MORPH_ERODE, np.ones((15,15)))
contours,_ = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(roi_frame, (x,y), (x+w,y+h), (0,255,0), 5)
# for y in range(2, dilation2.shape[0]-2):
#     for x in range(2, dilation2.shape[1]-2):
#         if (dilation2[y,x] == 255 and dilation2[y,x-1] == 0) :
#                 dilation2 = findcontours_copy(dilation2, y, x)
#                 x,y,w,h = cv2.boundingRect(dilation2)
#                 cv2.rectangle(roi_frame, (x,y), (x+w,y+h), (0,255,0), 5)
cv2.imshow("dilation", dilation2)
cv2.imshow("Frame", roi_frame)
    
cv2.waitKey(0)