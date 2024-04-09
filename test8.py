from PIL import Image
# import cv2
# import mtcnn
# detector = mtcnn.MTCNN()
# # img = cv2.imread("./190.jpg")
# img = cv2.imread("./images.jpg")


# faces = detector.detect_faces(img)
# [x, y, w, h] = faces[0]['box']
# img = img[ y:y+h, x:x+w]
# cv2.imwrite("goc.jpg",img)

# cv2.imwrite("gr_cv.jpg",cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))



    # ọc ảnh
def image_to_txt(image_path, txt_path):
    image = Image.open(image_path)
    # width, height = image.size
    # image = image.resize((width//3, height//3))
    width, height = image.size
    print(f"{ width, height}")
    # Mở file để ghi dữ liệu
    with open(txt_path, 'w') as txt_file:
        # Lặp qua từng pixel và ghi vào file
        for y in range(height):
            for x in range(width):
            
                # Lấy giá trị RGB của pixel
                r, g, b = image.getpixel((x, y))
                
                # Chuyển đổi thành biểu diễn 24-bit và ghi vào file
                pixel_value = (r << 16) | (g << 8) | b
                txt_file.write(f"{pixel_value:06X}\n")

# Đường dẫn của file ảnh đầu vào
input_image_path = 'face.jpg'


output_txt_path = 'output_image.txt'

# Chuyển đổi file ảnh thành file văn bản 24-bit
image_to_txt(input_image_path, output_txt_path)
