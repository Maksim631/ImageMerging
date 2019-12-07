import cv2
from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters

START_INDEX = 2
END_INDEX = 3

def get_str_index(i):
    strI = str(i)
    # if i < 10:
    #     strI = "0" + strI
    # if i < 100:
    #     strI = "0" + strI
    return strI


translations = []
current_translation_x = 0
current_translation_y = 0


i = START_INDEX

result = Image.open('box/' + get_str_index(i) + '.jpg')

while i < END_INDEX:
    picture1 = cv2.imread('box/' + get_str_index(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
    picture2 = cv2.imread('box/' + get_str_index(i + 1) + '.jpg', cv2.IMREAD_GRAYSCALE)
    translations.append(get_merge_parameters(picture1, picture2))
    print(i)
    i += 1

i = START_INDEX + 1
index = 0
while i < END_INDEX + 1:
    current_translation_x += translations[index][0][0]
    current_translation_y += translations[index][0][1]
    scale = translations[index][1]
    angle = translations[index][2]
    result = merge_with_parameters(result, Image.open('box/' + get_str_index(i) + '.jpg'),
                                   (current_translation_x, current_translation_y, scale, angle))
    index += 1
    i += 1
pyplot.imshow(result)
pyplot.show()
