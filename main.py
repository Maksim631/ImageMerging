from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters


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

i = 0

result = Image.open('lab_images/cyl_image' + get_str_index(i) + '.png')

while i < 24:
    lab_images1 = Image.open('lab_images/cyl_image' + get_str_index(i) + '.png')
    lab_images2 = Image.open('lab_images/cyl_image' + get_str_index(i + 1) + '.png')
    translations.append(get_merge_parameters(lab_images1, lab_images2))
    print(i)
    i += 1

i = 1
index = 0
while i < 25:
    current_translation_x += translations[index][0]
    current_translation_y += translations[index][1]
    result = merge_with_parameters(result, Image.open('lab_images/cyl_image' + get_str_index(i) + '.png'),
                                   (current_translation_x, current_translation_y))
    index += 1
    i += 1
pyplot.imshow(result)
pyplot.show()
