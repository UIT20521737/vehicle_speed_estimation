import imageio
import os

def create_video(image_folder, video_name='outputvideo/output_video.mp4', fps=25):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

    with imageio.get_writer(video_name, fps=fps) as writer:
        for image in images:
            img_path = os.path.join(image_folder, image)
            writer.append_data(imageio.imread(img_path))

# Thay đổi đường dẫn đến thư mục chứa ảnh của bạn
image_folder = 'output_frame/set1/video2'
create_video(image_folder)

# import cv2

# video_path = './dataset/subset01/video03/video.h264'

# # Mở video để đọc thông tin
# cap = cv2.VideoCapture(video_path)

# # Lấy số khung hình mỗi giây
# fps = cap.get(cv2.CAP_PROP_FPS)

# print(f"Số khung hình mỗi giây (FPS) của video là: {fps}")

# # Đóng video
# cap.release()