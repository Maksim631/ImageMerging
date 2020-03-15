from __future__ import print_function
import cv2
import numpy as np

from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.restoration import estimate_sigma

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


def find_homograph(img1, img2):
    # Convert test_images to grayscale
    # img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    # img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    # imMatches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    return h

def noisy(image, sigma):
    gauss = np.random.normal(0, sigma, image.size)
    gauss = gauss.reshape(image.shape).astype('uint8')
    # Add the Gaussian noise to the image
    img_gauss = cv2.add(image, gauss)
    return img_gauss


def merge_images(img1, img2, homograph):
    # Use homography
    height, width = img2.shape
    im1Reg = cv2.warpPerspective(img1, homograph, (width + 100, height + 100))

    return concatImages(img2, im1Reg, width, height)
    # return im1Reg, h


def concatImages(img1, img2, width, height):
    img2[0:height, 0:width] = img1
    return img2


if __name__ == '__main__':
    # Read reference image
    # img1 = "1_4.jpg"
    # print("Reading reference image : ", refFilename)
    imReference = cv2.imread("2.jpg", cv2.IMREAD_GRAYSCALE)
    # img2 = cv2.imread("2_4.jpg", cv2.IMREAD_GRAYSCALE)
    width, height = imReference.shape

    img1 = imReference[:width - 100, : height - 100]
    img2 = imReference[99:width - 1, 99: height - 1]
    # img1 = cv2.cvtColor(np.array(noisy(img1, 0)), cv2.COLOR_RGB2GRAY)
    # img2 = cv2.cvtColor(np.array(noisy(img2, 0)), cv2.COLOR_RGB2GRAY)
    print("ssim: " + str(ssim(img1, img2)))
    # Read image to be aligned
    print(estimate_sigma(img1) + estimate_sigma(img2))

    print("Aligning test_images ...")
    # Registered image will be resotred in imReg.
    # The estimated homography will be stored in h.
    h = find_homograph(img2, img1)
    imReg = merge_images(img2, img1, h)
    cv2.imwrite("out.png", imReg)
    # print(h)
