from __future__ import print_function
import cv2
import numpy as np

from matplotlib import pyplot as plt

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


def merge_images(img1, img2, homograph):
    # Use homography
    height, width, channels = img2.shape
    im1Reg = cv2.warpPerspective(img1, homograph, (width + 200, height + 200))

    return concatImages(img2, im1Reg, width, height)
    # return im1Reg, h


def concatImages(img1, img2, width, height):
    img2[0:height, 0:width] = img1
    return img2


if __name__ == '__main__':
    translations = []

    i = 406
    print("Reading reference image : ", i)
    # imReg = cv2.imread("images/IMG0" + str(i) + ".jpg", cv2.IMREAD_COLOR)
    img1 = cv2.imread("111-2.png")
    img2 = cv2.imread("222-2.png")
    img3 = merge_images(img1, img2, find_homograph(img1, img2))
    plt.imshow(img3)
    plt.show()

    # while i < 407:
    #     imReg = cv2.imread("images/IMG0" + str(i) + ".jpg", cv2.IMREAD_COLOR)
    #     i += 1
    #     imFilename = "images/IMG0" + str(i) + ".jpg"
    #     print("Reading image to align : ", imFilename)
    #     im = cv2.imread(imFilename, cv2.IMREAD_COLOR)
    #     translations.append(alignImages(im, imReg))
    #
    # result = Image.open('images/IMG0' + str(406) + '.jpg')
    # height, width = result.size
    # current_translation_x = 0
    # current_translation_y = 0
    # i = 407
    # index = 0
    # while i < 408:
    #     current_translation_x += int(translations[index][0][2])
    #     current_translation_y += int(translations[index][1][2])
    #     result = merge_with_parameters(result, Image.open('images/IMG0' + str(i) + '.jpg'),
    #                                    (current_translation_x, current_translation_y))
    #     index += 1
    #     i += 1
    # plt.imshow(result)
    # plt.show()


