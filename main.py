from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters

translations = []
current_translation_x = 0
current_translation_y = 0

i = 406

result = Image.open('images/IMG0' + str(i) + '.jpg')

while i < 410:
    img1 = Image.open('images/IMG0' + str(i) + '.jpg')
    img2 = Image.open('images/IMG0' + str(i + 1) + '.jpg')
    translations.append(get_merge_parameters(img1, img2))
    print(i)
    i += 1

i = 407
index = 0
while i < 411:
    current_translation_x += translations[index][0]
    current_translation_y += translations[index][1]
    result = merge_with_parameters(result, Image.open('images/IMG0' + str(i) + '.jpg'),
                                   (current_translation_x, current_translation_y))
    index += 1
    i += 1
pyplot.imshow(result)
pyplot.show()
