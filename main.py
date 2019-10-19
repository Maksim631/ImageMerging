from matplotlib import pyplot
from PIL import Image
from fourier import merge

result = Image.open('images/IMG0406.jpg')

i = 7
while i < 119:
    result = merge(result, Image.open('images/IMG040' + str(i) + '.jpg'))
    pyplot.imshow(result)
    pyplot.show()
    i += 1
pyplot.imshow(result)
pyplot.show()
