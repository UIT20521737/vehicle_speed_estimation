import cv2
img = cv2.imread('output_frame/118.jpg')
img = cv2.line(img, (1300,0), (1300, img.shape[0]), (255,0,255), thickness= 3)
img = cv2.line(img, (1800,0), (1800, img.shape[0]), (0,0,255), thickness= 3)
cv2.imshow("dsfds",img)
cv2.waitKey(0)