import cv2
import numpy as np

src = cv2.imread("./190.jpg", cv2.IMREAD_COLOR)
print(src.shape)
new_height = 360
new_width = 640
old_height, old_width, _ = src.shape

# Resize the image to new dimensions
dst = cv2.resize(src, (src.shape[1]//3, src.shape[0]//3), src)

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

for x in range(new_width):
    for n in range(new_height):
        px = (n + 0.5) * (old_height / new_height) - 0.5
        addr = int(px)
        px -= addr
        if addr + 1 < old_height and x < old_width:
            for k in range(3):
                drawing2[n, x, k] = drawing[addr, x, k] * (1 - px) + drawing[addr + 1, x, k] * px


# Display images
cv2.imshow('Original Image', src)
cv2.imshow('Resized Image', dst)
cv2.imshow('Interpolated Image', drawing2)
cv2.waitKey(0)
cv2.destroyAllWindows()
