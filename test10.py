import cv2
img1 = cv2.imread('test_gray/gr_cv.jpg')
img2 = cv2.imread('test_gray/gr_tt.jpg')
cv2.imshow("",img1 - img2)
cv2.waitKey(0)