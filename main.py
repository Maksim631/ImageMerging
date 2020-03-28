from matplotlib import pyplot
from PIL import Image
import cv2
from fourier import get_merge_parameters, merge_with_parameters, merge

img1 = cv2.imread("6_p.jpg")
img2 = cv2.imread("7_p.jpg")
# width, height, ch = img.shape
# img1r = img[:width - 100, : height - 100]
# img2r = img[99:width - 1, 99: height - 1]
img1 = Image.fromarray(img1)
img2 = Image.fromarray(img2)
# cv2.imwrite("1.jpg", img1r)
# cv2.imwrite("2.jpg", img2r)
result = merge(img1, img2)
pyplot.imshow(result)
pyplot.show()
