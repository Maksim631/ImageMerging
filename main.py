import cv2
from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters
from utils import noisy
import numpy as np


START_INDEX = 6
END_INDEX = 7

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

result = cv2.imread('medium/6.jpg')
img1 = Image.open("111-2.png")
img2 = Image.open("222-2.png")
img3 = merge_with_parameters(img1, img2, get_merge_parameters(img1, img2))

# cv2.imwrite("super_output.png", img3)

# while i < END_INDEX:
#     picture1 = cv2.imread('medium/' + get_str_index(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
#     picture2 = cv2.imread('medium/' + get_str_index(i + 1) + '.jpg', cv2.IMREAD_GRAYSCALE)
#     translations.append(get_merge_parameters(picture1, picture2))
#     print(i)
#     i += 1
#
# i = START_INDEX + 1
# index = 0
# while i < END_INDEX + 1:
#     current_translation_x += translations[index][0][0]
#     current_translation_y += translations[index][0][1]
#     scale = translations[index][1]
#     angle = translations[index][2]
#     result = merge_with_parameters(result, Image.open('medium/' + get_str_index(i) + '.jpg'),
#                                    (current_translation_x, current_translation_y, scale, angle))
#     index += 1
#     i += 1
pyplot.imshow(img3)
pyplot.show()
