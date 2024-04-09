import random
def create_list():
    random_list = []
    length = 7
    # Lặp qua 49 lần để thêm số ngẫu nhiên vào danh sách
    while len(random_list) < length:
        # Tạo một số ngẫu nhiên từ 1 đến length
        random_number = random.randint(1, length)
        # Kiểm tra xem số đã được thêm vào danh sách chưa
        if random_number not in random_list:
            # Nếu chưa thêm vào danh sách
            random_list.append(random_number)
    return random_list
def sort_2(a, b):
    return (a, b) if a > b else (b, a)
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
i=0
count = 0
while i < 10000:
    random_list = create_list()
    a, b, c, d, e, f, g = sort_7(*random_list)

    print(f'{random_list = }')
    print(f'{(a, b, c, d, e, f, g) == (7, 6, 5, 4, 3, 2, 1) }')
    if (a, b, c, d, e, f, g) == (7, 6, 5, 4, 3, 2, 1):
        count += 1
    i += 1
print(count)
# a = 1
# b = 2
# c = 3
# d = 4
# e = 5
# f = 6
# g = 7
# a, b, c, d, e, f, g = sort_7(a, b, c, d, e, f, g)
# print(a, b, c, d, e, f, g)