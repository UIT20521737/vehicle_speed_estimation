import cv2
import os

# Hàm thực hiện resize video
def resize_video(input_video_path, output_video_path, width=1920, height=1080):
    # Đọc video
    video_capture = cv2.VideoCapture(input_video_path)
    
    # Lấy thông số video (kích thước, fps)
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    
    # Tạo video writer để ghi video với kích thước mới
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # Sử dụng codec XVID
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Resize frame về kích thước mới
        resized_frame = cv2.resize(frame, (width, height))
        
        # Ghi frame vào video mới
        video_writer.write(resized_frame)
    
    # Giải phóng tài nguyên
    video_capture.release()
    video_writer.release()

# Thư mục chứa tất cả các tập tin video
root_folder = './dataset/subset01/video01/'

# Lặp qua tất cả các thư mục và tập tin trong cấu trúc thư mục
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('H264'):  # Chỉ xử lý các tập tin có đuôi .mov
            input_video_path = os.path.join(dirpath, filename)
            output_video_path = os.path.join('./dataset/subset01/video01/', 'resized_' + filename)  # Đặt tên cho video mới
            
            # Thực hiện resize và export video
            resize_video(input_video_path, output_video_path)
