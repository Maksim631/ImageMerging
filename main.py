from matplotlib import pyplot
from PIL import Image
from fourier import get_merge_parameters, merge_with_parameters, merge

img1 = Image.open('sun/1_4.jpg')
img2 = Image.open('sun/2_4.jpg')
result = merge(img1, img2)
pyplot.imshow(result)
pyplot.show()
