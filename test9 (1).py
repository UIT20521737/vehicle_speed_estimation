from PIL import Image

def txt_to_image(txt_path, width, height, output_image_path):
    # Đọc dữ liệu từ file văn bản
    with open(txt_path, 'r') as txt_file:
        data = txt_file.read().splitlines()

    # Tạo một ảnh mới
    new_image = Image.new("L", (width, height))

    # Lặp qua từng pixel và gán giá trị vào ảnh mới
    for y in range(height):
        for x in range(width):
            # Chuyển đổi giá trị pixel từ dạng văn bản sang số nguyên
            # if y * width + x  >= 3162 : break
            pixel_value = int(data[y * width + x])
            # Gán giá trị pixel vào ảnh mới
            new_image.putpixel((x, y), pixel_value)

    # Lưu ảnh mới
    new_image.save(output_image_path)

# Đường dẫn của file văn bản chứa các giá trị pixel
input_txt_path = 'out.txt'

# Chiều rộng và chiều cao của ảnh
image_width = 51
image_height = 62

# Đường dẫn của file ảnh đầu ra
# output_image_path = 'test_gray/gr_tt.jpg'
output_image_path = 'face_tt.jpg'

# Chuyển đổi file văn bản thành ảnh
txt_to_image(input_txt_path, image_width, image_height, output_image_path)
