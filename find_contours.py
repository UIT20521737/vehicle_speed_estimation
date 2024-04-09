import cv2
import numpy as np
import time

def minmax(y,x, ymin, ymax, xmin, xmax):
    if y < ymin:
        ymin =y
    if y > ymax:
        ymax =y
    if x < xmin:
        xmin =x
    if x > xmax:
        xmax =x
    return ymin, ymax, xmin, xmax
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
url1 = './dataset/tainghe.jpg'
url2 = './dataset/nen1.jpg'
frame1 = cv2.imread(url2)
frame2 = cv2.imread(url1)
frame1 = cv2.resize(frame1, (frame1.shape[1]//5, frame1.shape[0]//5), frame1)
frame2 = cv2.resize(frame2, (frame2.shape[1]//5, frame2.shape[0]//5), frame2)
frame = frame2 - frame1
# contours, hierarchy = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
color_contours = (0, 255, 0) # green - color for contours
color = (255, 0, 0) # blue - color for convex hull
binary = frame[:,:]
binary[binary < 135] = 0
binary[binary >= 135] = 255
drawing = np.zeros((binary.shape[0], binary.shape[1]), np.uint8)
# cv2.imshow('thresh', thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(thresh[0:50, 50:100])
start = time.time()
for y in range(2, binary.shape[0]-2):
    for x in range(2, binary.shape[1]-2):
        if (binary[y,x] == 255 and binary[y,x-1] == 0) :
                binary = findcontours_copy(binary, y, x)
binary[binary != 100] = 0
binary[binary == 100] = 255
#cv2.imwrite("binary_fc.jpg")
#print(binary.shape)
end_t = time.time()
t = end_t - start 
print("Time = ",t)
cv2.imshow(binary)