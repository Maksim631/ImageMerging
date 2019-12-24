import cv2
from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters
import numpy

START_INDEX = 5
END_INDEX = 6

WINDOW_WIDTH = int((1290 - 140) / 10)
WINDOW_HEIGHT = int((960) / 10)

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


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

shape = (1290 - 140, 960)
squares = numpy.zeros(shape)


def get_value(translation_params):
    translation, scale, angle = translation_params
    return int(abs(translation[0]) + abs(translation[1]) + abs(scale) * 10 + abs(angle)) **2


while i < END_INDEX:
    picture1 = cv2.imread('box/' + get_str_index(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
    picture2 = cv2.imread('box/' + get_str_index(i + 1) + '.jpg', cv2.IMREAD_GRAYSCALE)
    translations.append(get_merge_parameters(picture1, picture2))
    print(translations[0])
    print(i)
    i += 1

for i in range(9):
    for j in range(9):
        picture1 = cv2.imread('box/5.jpg', cv2.IMREAD_GRAYSCALE)
        picture2 = cv2.imread('box/6.jpg', cv2.IMREAD_GRAYSCALE)
        picture1 = picture1[i * WINDOW_WIDTH: (i + 1) * WINDOW_WIDTH,
                   151+ j * WINDOW_HEIGHT:  151+ (j + 1) * WINDOW_HEIGHT]
        picture2 = picture2[i * WINDOW_WIDTH:(i + 1) * WINDOW_WIDTH, j * WINDOW_HEIGHT: (j + 1) * WINDOW_HEIGHT]
        cv2.imwrite("./res/First" + str(i) + "j=" + str(j) + ".jpg", picture1)
        cv2.imwrite("./res/Second" + str(i) + "j=" + str(j) + ".jpg", picture2)
        squares[i * WINDOW_WIDTH: (i + 1) * WINDOW_WIDTH, j * WINDOW_HEIGHT: (j + 1) * WINDOW_HEIGHT] = get_value(
            get_merge_parameters(picture1, picture2))
        print("i: " + str(i) + " j: " + str(j))
        print(get_merge_parameters(picture1, picture2))

pyplot.imshow(squares, cmap='hot', interpolation='nearest')
pyplot.colorbar()
pyplot.show()

# Used to merge images
#
# i = START_INDEX + 1
# index = 0
# while i < END_INDEX + 1:
#     current_translation_x += translations[index][0][0]
#     current_translation_y += translations[index][0][1]
#     scale = translations[index][1]
#     angle = translations[index][2]
#     result = merge_with_parameters(result, Image.open('box/' + get_str_index(i) + '.jpg'),
#                                    (current_translation_x, current_translation_y, scale, angle))
#     index += 1
#     i += 1
# pyplot.imshow(result)
# pyplot.show()
