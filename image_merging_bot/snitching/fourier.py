import math

import cv2
import numpy as np
import scipy.ndimage.interpolation as ndii
from PIL import Image
from skimage.feature import register_translation


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


def translation(img1, img2):
    a = register_translation(img1, img2)
    return int(a[0][0]), int(a[0][1])


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


def highpass(shape):
    x = np.outer(
        np.cos(np.linspace(-math.pi / 2., math.pi / 2., shape[0])),
        np.cos(np.linspace(-math.pi / 2., math.pi / 2., shape[1])))
    return (1.0 - x) * (2.0 - x)


def rotation(im0, im1):
    f0 = np.fft.fftshift(abs(np.fft.fft2(im0)))
    f1 = np.fft.fftshift(abs(np.fft.fft2(im1)))

    h = highpass(f0.shape)
    f0 *= h
    f1 *= h
    del h

    f0, log_base = log_polar(f0)
    f1, log_base = log_polar(f1)

    f0 = np.fft.fft2(f0)
    f1 = np.fft.fft2(f1)
    r0 = abs(f0) * abs(f1)
    ir = abs(np.fft.ifft2((f0 * f1.conjugate()) / r0))
    i0, i1 = np.unravel_index(np.argmax(ir), ir.shape)
    angle = 180.0 * i0 / ir.shape[0]
    scale = log_base ** i1

    if scale > 1.8:
        ir = abs(np.fft.ifft2((f1 * f0.conjugate()) / r0))
        i0, i1 = np.unravel_index(np.argmax(ir), ir.shape)
        angle = -180.0 * i0 / ir.shape[0]
        scale = 1.0 / (log_base ** i1)
        if scale > 1.8:
            raise ValueError('Images are not compatible. Scale change > 1.8')

    if angle < -90.0:
        angle += 180.0
    elif angle > 90.0:
        angle -= 180.0
    return angle, scale


def simple_rotate(image, angle, scale):
    image = ndii.zoom(image, 1.0 / scale)
    image = ndii.rotate(image, angle)
    return image


def affine_rotate(image, angle, scale):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, scale)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def merge_with_parameters(img1, img2, translation_params):
    translation, scale, angle = translation_params
    x = translation[0]
    y = translation[1]
    img2 = simple_rotate(img2, angle, scale)
    img2 = Image.fromarray(img2)
    if x <= 0 < y:
        shape = (img2.size[0] + y, 2 * img2.size[1] + x)
        result_image = Image.new('RGB', shape)
        result_image.paste(img1, (0, int(abs(x))))
        result_image.paste(img2, (y, 0))
    if x >= 0 > y:
        shape = (2 * img1.size[0] + int(abs(y)), 2 * img1.size[1] + x)
        result_image = Image.new('RGB', shape)
        result_image.paste(img2, (0, x))
        result_image.paste(img1, (int(abs(y)), 0))
    if x < 0 and y < 0:
        shape = (img2.size[0] + x, img2.size[1] + int(abs(y)))
        result_image = Image.new('RGB', shape)
        result_image.paste(img2, (y, x))
        result_image.paste(img1, (0, 0))
    if x >= 0 and y > 0:
        shape = (img1.size[0] + x, img1.size[1] + y)
        result_image = Image.new('RGB', shape)
        result_image.paste(img2, (x, y))
        result_image.paste(img1, (0, 0))
    return result_image


def get_merge_parameters(cv_img1, cv_img2):
    cv_img1 = cv2.cvtColor(np.array(cv_img1), cv2.COLOR_RGB2GRAY)
    cv_img2 = cv2.cvtColor(np.array(cv_img2), cv2.COLOR_RGB2GRAY)

    blur_borders(cv_img1)
    blur_borders(cv_img2)
    # angle, scale = rotation(cv_img1, cv_img2)
    # img2_rotated = affine_rotate(cv_img2, angle, scale)
    return translation(cv_img1, cv_img2), 1, 0
