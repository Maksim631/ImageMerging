import cv2
import numpy as np
from scipy.fftpack import fft2
from matplotlib import pyplot as plt
import math
import polarTransform as pt

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

    matOfOnes = np.ones(magimg.shape, dtype=magimg.dtype)
    cv2.add(matOfOnes, magimg, magimg)  # switch to logarithmic scale
    cv2.log(magimg, magimg)

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


def logPolarTransform(img):
    return pt.convertToPolarImage(img)


def rotation(img1, img2):
    test1 = fourier(img1)
    test2 = fourier(img2)

    img1Log = logPolarTransform(test1)
    img2Log = logPolarTransform(test2)

    # //Mat img1_log{ fourier(img1_logKEK) }
    # //Mat img2_log{ fourier(img2_logKEK) }
    cv2.imshow("1", img1Log[0])
    cv2.imshow("2", img2Log[0])
    cv2.waitKey()
    translationPoint = translation(img1Log[0], img2Log[0])
    # int size{ max(img1.rows, img2.cols) }
    # double base{ exp(log(img1.rows / 2) / size) }
    #
    # Point2d result{ Point2d(-M_PI * translationPoint.x / size, pow(base, translationPoint.y)) }
    return translationPoint


img1 = cv2.imread(cv2.samples.findFile("horse2332.png"), cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(cv2.samples.findFile("horse_rotated2332.png"), cv2.IMREAD_GRAYSCALE)

print(rotation(img1, img2))

# plt.subplot(121), plt.imshow(img)
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(fourier(img), cmap='gray')
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()
