import random

# # Tạo một danh sách trống để chứa các số
# random_list = []

# # Lặp qua 49 lần để thêm số ngẫu nhiên vào danh sách
# while len(random_list) < 49:
#     # Tạo một số ngẫu nhiên từ 1 đến 49
#     random_number = random.randint(1, 49)
#     # Kiểm tra xem số đã được thêm vào danh sách chưa
#     if random_number not in random_list:
#         # Nếu chưa thêm vào danh sách
#         random_list.append(random_number)

# # In ra danh sách đã tạo
# print(random_list)
def create_list():
    random_list = []
    length = 49
   
    # Lặp qua 49 lần để thêm số ngẫu nhiên vào danh sách
    while len(random_list) < length:
        # Tạo một số ngẫu nhiên từ 1 đến length
        random_number = random.randint(0, 1000)
        # Kiểm tra xem số đã được thêm vào danh sách chưa
        if random_number not in random_list:
            # Nếu chưa thêm vào danh sách
            random_list.append(random_number)
            
    return random_list
def sort_2(a, b):
    return (a, b) if a > b else (b, a)
 
def sort_3(a, b, c):
    a, b = sort_2(a, b)
    b, c = sort_2(b, c)
    a, b = sort_2(a, b)
    return a, b, c

def sort_7(a, b, c, d, e, f, g):
    a,b = sort_2(a,b)
    b,c = sort_2(b,c)
    a,b = sort_2(a,b)
    
    d,e = sort_2(d,e)
    f,g = sort_2(f,g)
    d,f = sort_2(d,f)
    e,g = sort_2(e,g)
    e,f = sort_2(f,e)
    
    a,d = sort_2(a,d)
    b,e = sort_2(b,e)
    b,d = sort_2(d,b)
    c,f = sort_2(c,f)
    f,g = sort_2(f,g)
    c,e = sort_2(e,c)
    e,f = sort_2(e,f)
    c,d = sort_2(d,c)
    d,e = sort_2(d,e)
    return a, b, c, d, e, f, g
def sort_49(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26, a27, a28, a29, a30, a31, a32, a33, a34, a35, a36, a37, a38, a39, a40, a41, a42, a43, a44, a45, a46, a47, a48, a49):
    #sắp theo thứ 4
    a1, a2, a3, a4, a5, a6, a7 = sort_7(a1, a2, a3, a4, a5, a6, a7)
    a8, a9, a10, a11, a12, a13, a14 = sort_7(a8, a9, a10, a11, a12, a13, a14)
    a15, a16, a17, a18, a19, a20, a21 = sort_7( a15, a16, a17, a18, a19, a20, a21)
    a22, a23, a24, a25, a26, a27, a28 = sort_7( a22, a23, a24, a25, a26, a27, a28)
    a29, a30, a31, a32, a33, a34, a35 = sort_7( a29, a30, a31, a32, a33, a34, a35)
    a36, a37, a38, a39, a40, a41, a42 = sort_7(a36, a37, a38, a39, a40, a41, a42)
    a43, a44, a45, a46, a47, a48, a49 = sort_7( a43, a44, a45, a46, a47, a48, a49)
    #chon ra lon
    a1, a8, a15, a22, a29, a36, a43 = sort_7(a1, a8, a15, a22, a29, a36, a43)
    a2, a9, a16, a23, a30, a37, a44 = sort_7(a2, a9, a16, a23, a30, a37, a44)
    a3, a10, a17, a24, a31, a38, a45 = sort_7(a3, a10, a17, a24, a31, a38, a45)
    a4, a11, a18, a25, a32, a39, a46 = sort_7(a4, a11, a18, a25, a32, a39, a46)
    a5, a12, a19, a26, a33, a40, a47 = sort_7(a5, a12, a19, a26, a33, a40, a47)
    a6, a13, a20, a27, a34, a41, a48 = sort_7(a6, a13, a20, a27, a34, a41, a48)
    a7, a14, a21, a28, a35, a42, a49 = sort_7(a7, a14, a21, a28, a35, a42, a49)
    #4 trên 3 dưới
    a2, a9, a16, a23, a29, a36, a43 = sort_7(a2, a9, a16, a22, a29, a36, a43)
    a3, a10, a17, a23, a30, a37, a44 = sort_7(a3, a10, a17, a23, a30, a37, a44)
    a4, a11, a18, a24, a31, a38, a45 = sort_7(a4, a11, a18, a24, a31, a38, a45)
    a5, a12, a19, a25, a32, a39, a46 = sort_7(a5, a12, a19, a25, a32, a39, a46)
    a6, a13, a20, a26, a33, a40, a47 = sort_7(a6, a13, a20, a26, a33, a40, a47)
    a7, a14, a21, a27, a34, a41, a48 = sort_7(a7, a14, a21, a27, a34, a41, a48)
    #3 trên 4 dưới
    a3, a10, a17, a23, a29, a36, a43 = sort_7(a3, a10, a17, a23, a29, a36, a43)
    a4, a11, a18, a24, a30, a37, a44 = sort_7(a4, a11, a18, a24, a30, a37, a44)
    a5, a12, a19, a25, a31, a38, a45 = sort_7( a5, a12, a19, a25, a31, a38, a45)
    a6, a13, a20, a26, a32, a39, a46 = sort_7( a6, a13, a20, a26, a32, a39, a46)
    a7, a14, a21, a27, a33, a40, a47 = sort_7(a7, a14, a21, a27, a33, a40, a47)
    #4  trên 3 dưới
    a4, a11, a18, a23, a29, a36, a43 = sort_7(a4, a11, a18, a23, a29, a36, a43)
    a5, a12, a19, a24, a30, a37, a44 = sort_7( a5, a12, a19, a24, a30, a37, a44)
    a6, a13, a20, a25, a31, a38, a45 = sort_7(  a6, a13, a20, a25, a31, a38, a45)
    a7, a14, a21, a26, a32, a39, a46 = sort_7( a7, a14, a21, a26, a32, a39, a46)
    #3 trên 4 dưới
    a5, a12, a19, a24, a29, a36, a43 = sort_7(a5, a12, a19, a24, a29, a36, a43)
    a6, a13, a20, a25, a30, a37, a44 = sort_7(a6, a13, a20, a25, a30, a37, a44)
    a7, a14, a21, a26, a31, a38, a45 = sort_7(a7, a14, a21, a26, a31, a38, a45)
    #4  trên 3 dưới
    a5, a12, a19, a24, a29, a36, a43 = sort_7(a6, a13, a20, a24, a29, a36, a43)
    a6, a13, a20, a25, a30, a37, a44 = sort_7( a7, a14, a21, a25, a30, a37, a44)
    #3 trên 4 dưới
    a6, a13, a20, a25, a29, a36, a43 = sort_7(a6, a13, a20, a25, a29, a36, a43)
    return a25
# a1 = 25
# a2 = 2
# a3 = 3
# a4 = 4
# a5 = 5
# a6 = 6
# a7 = 7
# a8 = 8
# a9 = 9
# a10 = 10
# a11 = 11
# a12 = 12
# a13 = 13
# a14 = 14
# a15 = 15
# a16 = 16
# a17 = 17
# a18 = 18
# a19 = 19
# a20 = 20
# a21 = 21
# a22 = 22
# a23 = 23
# a24 = 24
# a25 = 49
# a26 = 26
# a27 = 27
# a28 = 28
# a29 = 29
# a30 = 30
# a31 = 31
# a32 = 32
# a33 = 33
# a34 = 34
# a35 = 35
# a36 = 36
# a37 = 37
# a38 = 38
# a39 = 39
# a40 = 40
# a41 = 41
# a42 = 42
# a43 = 43
# a44 = 44
# a45 = 45
# a46 = 46
# a47 = 47
# a48 = 48
# a49 = 1
i = 0
count = 0
while i < 1000000:
    random_list = create_list()
    a25 = sort_49(*random_list)
    a = sorted(random_list)
    print(f'{i = }, {a25 = }, {a[24] = }')
    with open('list.txt', 'a',  encoding='UTF-8') as file:
        file.write(f'{i = }, {a25 = }, {a[24] = }\n')
    if a25 == a[24]:
        count += 1
    # print(f'{sorted(random_list) = }')
    # print(f'{random_list = }')
    # print(f'{ a25 = }')
    i += 1
print(f'{count = }')
