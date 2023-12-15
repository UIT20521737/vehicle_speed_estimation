import cv2
import xml.etree.ElementTree as ET

# Đọc tập tin XML
tree = ET.parse('./dataset/subset01/video01/vehicles.xml')
root = tree.getroot()

# Đọc video
video_path = './dataset/subset01/video01/video.h264'
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Lặp qua các phương tiện trong tập tin XML
    for vehicle in root.findall('.//vehicle'):
        region = vehicle.find('region')
        if region is not None and 'x' in region.attrib:
            x = int(region.attrib['x'])
            y = int(region.attrib['y'])
            w = int(region.attrib['w'])
            h = int(region.attrib['h'])
            print(f"x: {x}, y: {y}, w: {w}, h: {h}")

            # Vẽ hình chữ nhật lên bức hình copy
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Hiển thị ảnh với các hình chữ nhật đã vẽ
    cv2.imshow('Result',frame)

    # Nếu bạn muốn thoát khi nhấn 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Giải phóng các tài nguyên
cap.release()
cv2.destroyAllWindows()
