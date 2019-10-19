from matplotlib import pyplot
from PIL import Image
from fourier import merge

result = Image.open('images/IMG0406.jpg')

i = 7
while i < 119:
    result = merge(result, Image.open('images/IMG040' + str(i) + '.jpg'))
    i += 1
# img2Colour = Image.open('test_images/IMG0407.jpg')
pyplot.imshow(result)
pyplot.show()
