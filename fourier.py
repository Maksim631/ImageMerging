import cv2
import numpy as np
import math
import scipy.ndimage.interpolation as ndii
from PIL import Image
from matplotlib import pyplot
from scipy.fftpack import ifftn, fftn


def blurSingleBorder(x, y, w, h, image):
    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 5)
    sub_face = image[y:y + h, x:x + w]
    # apply a gaussian blur on this new recangle image
    sub_face = cv2.GaussianBlur(sub_face, (23, 23), 30)
    # merge this blurry rectangle to our final image
    image[y:y + sub_face.shape[0], x:x + sub_face.shape[1]] = sub_face


def blurBorders(input):
    sizeR = input.shape[0]
    sizeC = input.shape[1]
    blurSize = 50
    blurSingleBorder(0, 0, sizeR, blurSize, input)
    blurSingleBorder(0, 0, blurSize, sizeR, input)
    blurSingleBorder(0, sizeR - blurSize, sizeC, blurSize, input)
    blurSingleBorder(sizeC - blurSize, 0, blurSize, sizeR, input)


def fourier(img):
    rows, cols = img.shape
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    return magnitude_spectrum


def phase_correlation(a, b):
    G_a = np.fft.fft2(a)
    G_b = np.fft.fft2(b)
    conj_b = np.ma.conjugate(G_b)
    R = G_a * conj_b
    R /= np.absolute(R)
    r = np.fft.ifft2(R).real
    return r


def translation(img1, img2):
    corr = phase_correlation(np.array(img1), np.array(img2))
    pyplot.imshow(corr, cmap='gray')
    pyplot.show()
    corr[0,0] = 0
    result = np.where(corr == np.amax(corr))
    return result[0], result [1]
    # point = cv2.phaseCorrelate(np.float32(img1), np.float32(img2))
    # result = [round(point[0][0]), round(point[0][1])]
    # return result


def logpolar(image, angles=None, radii=None):
    """Return log-polar transformed image and log base."""
    shape = image.shape
    center = shape[0] / 2, shape[1] / 2
    if angles is None:
        angles = shape[0]
    if radii is None:
        radii = shape[1]
    theta = np.empty((angles, radii), dtype='float64')
    theta.T[:] = np.linspace(0, np.pi, angles, endpoint=False) * -1.0
    # d = radii
    d = np.hypot(shape[0] - center[0], shape[1] - center[1])
    log_base = 10.0 ** (math.log10(d) / (radii))
    radius = np.empty_like(theta)
    radius[:] = np.power(log_base,
                         np.arange(radii, dtype='float64')) - 1.0
    x = radius * np.sin(theta) + center[0]
    y = radius * np.cos(theta) + center[1]
    output = np.empty_like(x)
    ndii.map_coordinates(image, [x, y], output=output)
    return output, log_base


def rotation(img1, img2):
    test1 = fourier(img1)
    test2 = fourier(img2)

    img1Log, logBase = logpolar(test1)
    img2Log, logBase = logpolar(test2)



    cv2.imwrite('1.png', img1Log)
    cv2.imwrite('3_2.png', test1)
    cv2.imwrite('4_2.png', test2)
    cv2.imwrite('2.png', img2Log)
    cv2.destroyAllWindows()


    translationPoint = translation(img1Log, img2Log)
    translationPoint = [-translationPoint[0], -translationPoint[1]]
    size = max(img1.shape[0], img2.shape[1])
    base = math.exp(math.log(img1.shape[0] / 2) / size)

    return (-180 * translationPoint[1]) / size, pow(base, translationPoint[0])

img1Colour = Image.open('images/IMG0406.jpg')
img2Colour = Image.open('images/IMG0407.jpg')
img1Grey = cv2.imread(cv2.samples.findFile("images/IMG0406.jpg"), cv2.IMREAD_GRAYSCALE)
img2Grey = cv2.imread(cv2.samples.findFile("images/IMG0407.jpg"), cv2.IMREAD_GRAYSCALE)

blurBorders(img1Grey)
blurBorders(img2Grey)

x, y = translation(img1Grey, img2Grey)
print(rotation(img1Grey, img2Grey))
image = Image.new('RGB', (1500, 1500))
image.paste(img1Colour, (0, 0))
image.paste(img2Colour, (y, x))
# img2Colour.paste(img1Colour, (x, y))
pyplot.imshow(image)
pyplot.show()
