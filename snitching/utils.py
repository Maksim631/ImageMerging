import numpy as np
import cv2
import math
from scipy.signal import convolve2d

from snitching.feature import find_homograph
from snitching.fourier import get_merge_parameters


def noisy(image, sigma):
    gauss = np.random.normal(0, sigma, image.size)
    gauss = gauss.reshape(image.shape).astype('uint8')
    # Add the Gaussian noise to the image
    img_gauss = cv2.add(image, gauss)
    return img_gauss


# gauss = gauss.reshape((row, col, ch))
# noisy = image + gauss
def estimate_noise(I):
    H, W = I.shape
    M = [[1, -2, 1],
         [-2, 4, -2],
         [1, -2, 1]]

    sigma = np.sum(np.sum(np.absolute(convolve2d(I, M))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W - 2) * (H - 2))

    return sigma


def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def get_translation_from_homograph(homograph):
    return (-int(homograph[0][2]), -int(homograph[1][2]))


def complete_comparing(img1, img2):
    return test_translations(get_merge_parameters(img1, img2)[0],
                             get_translation_from_homograph(find_homograph(img1, img2)))


def test_translations(fourier_translation, feature_translation):
    feature = np.sqrt((99 - feature_translation[0]) ** 2 + (99 - feature_translation[1]) ** 2)
    fourier = np.sqrt((99 - fourier_translation[0]) ** 2 + (99 - fourier_translation[1]) ** 2)
    if feature >= fourier:
        return 'Fourier-Mellin'
    else:
        return 'Feature'