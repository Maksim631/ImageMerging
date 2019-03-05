import cv2
import numpy as np
from scipy.fftpack import fft2
from matplotlib import pyplot as plt
import math
import polarTransform as pt
from log_transform import main
import scipy.ndimage.interpolation as ndii


def fourier(img):
    rows, cols = img.shape
    m = cv2.getOptimalDFTSize(rows)
    n = cv2.getOptimalDFTSize(cols)
    padded = cv2.copyMakeBorder(img, 0, m - rows, 0, n - cols, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    planes = [np.float32(padded), np.zeros(padded.shape, np.float32)]
    compleximg = cv2.merge(planes)  # Add to the expanded another plane with zeros

    cv2.dft(compleximg, compleximg)  # this way the result may fit in the source matrix

    cv2.split(compleximg, planes)  # planes[0] = Re(DFT(img), planes[1] = imgm(DFT(img))
    cv2.magnitude(planes[0], planes[1], planes[0])  # planes[0] = magnitude
    magimg = planes[0]

    # matOfOnes = np.ones(magimg.shape, dtype=magimg.dtype)
    # cv2.add(matOfOnes, magimg, magimg)  # switch to logarithmic scale
    # cv2.log(magimg, magimg)

    magimg_rows, magimg_cols = magimg.shape
    # crop the spectrum, if it has an odd number of rows or columns
    magimg = magimg[0:(magimg_rows & -2), 0:(magimg_cols & -2)]
    cx = int(magimg_rows / 2)
    cy = int(magimg_cols / 2)
    q0 = magimg[0:cx, 0:cy]  # Top-Left - Create a ROimg per quadrant
    q1 = magimg[cx:cx + cx, 0:cy]  # Top-Right
    q2 = magimg[0:cx, cy:cy + cy]  # Bottom-Left
    q3 = magimg[cx:cx + cx, cy:cy + cy]  # Bottom-Right
    tmp = np.copy(q0)  # swap quadrants (Top-Left with Bottom-Right)
    magimg[0:cx, 0:cy] = q3
    magimg[cx:cx + cx, cy:cy + cy] = tmp
    tmp = np.copy(q1)  # swap quadrant (Top-Right with Bottom-Left)
    magimg[cx:cx + cx, 0:cy] = q2
    magimg[0:cx, cy:cy + cy] = tmp

    cv2.normalize(magimg, magimg, 0, 1, cv2.NORM_MINMAX)  # Transform the matrix with float values into a
    return magimg


def translation(img1, img2):
    point = cv2.phaseCorrelate(np.float64(img1), np.float64(img2))
    result = [round(point[0][0]), round(point[0][1])]
    return result


# def logPolarTransform(img, i):
#     return logpolar(img)[0]
    # cv2.imwrite(i + ".png", img*255)  # ("3", img1Log[0])
    # main(i)
    # val = i + ".png"
    # return cv2.imread(cv2.samples.findFile(val), cv2.IMREAD_GRAYSCALE)

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

    # //Mat img1_log{ fourier(img1_logKEK) }
    # //Mat img2_log{ fourier(img2_logKEK) }
    # cv2.imshow("1", img1Log)
    # cv2.imshow("2", img2Log)

    # cv2.imwrite('1.png', img1Log)  # ("3", img1Log[0])
    # cv2.imwrite('2.png', img2Log)  # ("4", img2Log[0])
    # cv2.destroyAllWindows()

    # cv2.waitKey()
    # np.array(float_img * 255, dtype=np.uint8)

    # print(trans)
    translationPoint = translation(img1Log, img2Log)
    translationPoint = [-translationPoint[0], -translationPoint[1]]
    size = max(img1.shape[0], img2.shape[1])
    base = math.exp(math.log(img1.shape[0] / 2) / size)

    return (-180 * translationPoint[1]) / size, pow(base, translationPoint[0])


img1 = cv2.imread(cv2.samples.findFile("images/horse.png"), cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(cv2.samples.findFile("images/horse_rot_scale.png"), cv2.IMREAD_GRAYSCALE)

# cv2.imshow("123", logPolarTransform(fourier(img1))[0])
print(rotation(img1, img2))

# plt.subplot(121), plt.imshow(img)
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(fourier(img), cmap='gray')
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()
