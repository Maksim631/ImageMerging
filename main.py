from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters


def get_str_index(i):
    strI = str(i)
    if i < 10:
        strI = "0" + strI
    if i < 100:
        strI = "0" + strI
    return strI


translations = []
current_translation_x = 0
current_translation_y = 0

i = 10

result = Image.open('img/IX-01-61737_0029_0' + get_str_index(i) + '.JPG')

while i > 4:
    img1 = Image.open('img/IX-01-61737_0029_0' + get_str_index(i) + '.JPG')
    img2 = Image.open('img/IX-01-61737_0029_0' + get_str_index(i + 1) + '.JPG')
    translations.append(get_merge_parameters(img1, img2))
    print(i)
    i -= 1

i = 9
index = 0
while i > 3:
    current_translation_x += translations[index][0]
    current_translation_y += translations[index][1]
    result = merge_with_parameters(result, Image.open('img/IX-01-61737_0029_0' + get_str_index(i) + '.JPG'),
                                   (current_translation_x, current_translation_y))
    index += 1
    i -= 1
pyplot.imshow(result)
pyplot.show()
