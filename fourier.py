import math

import cv2
import numpy as np
import scipy.ndimage.interpolation as ndii
from PIL import Image
from matplotlib import pyplot
# from skimage.feature import register_translation



def blur_single_border(x, y, w, h, image):
    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 5)
    sub_face = image[y:y + h, x:x + w]
    # apply a gaussian blur on this new recangle image
    sub_face = cv2.GaussianBlur(sub_face, (23, 23), 30)
    # merge this blurry rectangle to our final image
    image[y:y + sub_face.shape[0], x:x + sub_face.shape[1]] = sub_face


def blur_borders(input):
    sizeR = input.shape[0]
    sizeC = input.shape[1]
    blurSize = 50
    blur_single_border(0, 0, sizeR, blurSize, input)
    blur_single_border(0, 0, blurSize, sizeR, input)
    blur_single_border(0, sizeR - blurSize, sizeC, blurSize, input)
    blur_single_border(sizeC - blurSize, 0, blurSize, sizeR, input)


def fourier(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    return magnitude_spectrum


def phase_correlation(a, b):
    G_a = np.fft.fft2(a)
    G_b = np.fft.fft2(b)
    conj_b = np.ma.conjugate(G_b)
    R = G_a * conj_b
    R2 = G_a * G_b
    R /= np.absolute(R2)
    r = np.fft.ifft2(R).real
    return r


def translation(img1, img2):
    corr = phase_correlation(np.array(img1), np.array(img2))
    pyplot.imshow(corr, cmap='gray')
    pyplot.show()
    # corr[0, 0] = 0
    # blur_borders(corr)
    print(np.amax(corr))
    # result = np.where(corr == np.amax(corr), corr.shape[0], corr.shape[1])
    result = np.unravel_index(corr.argmax(), corr.shape)
    print((result[0], result[1]))
    return result[0], result[1]


def log_polar(image, angles=None, radii=None):
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
    log_base = 10.0 ** (math.log10(d) / radii)
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

    img1_log, log_base = log_polar(test1)
    img2_log, log_base = log_polar(test2)
    translation_point = translation(img1_log, img2_log)
    translation_point = (-translation_point[0], -translation_point[1])
    size = max(img1.shape[0], img2.shape[1])
    base = math.exp(math.log(img1.shape[0] / 2) / size)
    return (-180 * translation_point[1]) / size, pow(base, translation_point[0])


def rotate_image(image, angle, scale):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, scale)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def merge(img1, img2):
    translation_params, angle = get_merge_parameters(img1, img2)
    return merge_with_parameters(img1, img2, translation_params, angle)


def merge_with_parameters(img1, img2, translation_params):
    x, y = translation_params
    cv_img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
    # img2_rotated = rotate_image(cv_img2, angle, 1)
    shape = (img2.size[0] + y, img2.size[1] + x)
    result_image = Image.new('RGB', shape)
    result_image.paste(img1, (0, 0))
    result_image.paste(img2, (y, x))
    return result_image


def get_merge_parameters(img1, img2):
    cv_img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2GRAY)
    cv_img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
    blur_borders(cv_img1)
    blur_borders(cv_img2)
    # angle, scale = rotation(cv_img1, cv_img2)
    # img2_rotated = rotate_image(cv_img2, angle, 1)
    return translation(cv_img1, cv_img2)
