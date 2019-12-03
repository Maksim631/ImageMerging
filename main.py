from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters

START_INDEX = 10
END_INDEX = 20

def get_str_index(i):
    strI = str(i)
    if i < 10:
        strI = "0" + strI
    # if i < 100:
    #     strI = "0" + strI
    return strI


translations = []
current_translation_x = 0
current_translation_y = 0

i = START_INDEX

result = Image.open('Synthetic/img' + get_str_index(i) + '.JPG')

while i < END_INDEX:
    pictures1 = Image.open('Synthetic/img' + get_str_index(i) + '.JPG')
    pictures2 = Image.open('Synthetic/img' + get_str_index(i + 1) + '.JPG')
    translations.append(get_merge_parameters(pictures1, pictures2))
    print(i)
    i += 1

i = START_INDEX + 1
index = 0
while i < END_INDEX + 1:
    current_translation_x += translations[index][0][0]
    current_translation_y += translations[index][0][1]
    scale = translations[index][1]
    angle = translations[index][2]
    result = merge_with_parameters(result, Image.open('Synthetic/img' + get_str_index(i) + '.JPG'),
                                   (current_translation_x, current_translation_y, scale, angle))
    index += 1
    i += 1
pyplot.imshow(result)
pyplot.show()
