import cv2
import numpy as np

# Ma trận ban đầu 6x6
matrix_6x6 = np.array([
    [10, 20, 30, 40, 50, 60],
    [15, 25, 35, 45, 55, 65],
    [12, 22, 32, 42, 52, 62],
    [18, 28, 38, 48, 58, 68],
    [14, 24, 34, 44, 54, 64],
    [16, 26, 36, 46, 56, 66]
], dtype=np.uint8)  # Chú ý cung cấp kiểu dữ liệu uint8 cho ma trận

# Chuyển đổi ma trận thành hình ảnh để sử dụng cv2.resize
image = np.uint8(matrix_6x6)

# Resize bằng bilinear interpolation về kích thước 4x4
new_matrix_4x4 = cv2.resize(image, (4, 4), interpolation=cv2.INTER_LINEAR)

print("Ma trận mới 4x4:")
print(new_matrix_4x4)
