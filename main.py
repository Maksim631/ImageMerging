import cv2
from fourier import get_merge_parameters, merge_with_parameters
from utils import get_translation_from_homograph, noisy, test_translations, psnr, estimate_noise, complete_comparing
from sklearn.metrics import mean_squared_error
from skimage.restoration import estimate_sigma
from skimage.morphology import disk
from scipy import signal
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.filters.rank import entropy


from feature import find_homograph, merge_images
import numpy as np

correct_pred = 0
features = 0
all_images = 0
sigmas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

image = cv2.imread('1.jpg')
width, height, ch = image.shape
img1 = image[:width - 100, : height - 100]
img2 = image[99:width - 1, 99: height - 1]
img1 = Image.fromarray(img1)
img2 = Image.fromarray(img2)
cv2.imwrite("out.jpg", np.array(merge_with_parameters(img1, img2, get_merge_parameters(img1, img2))))
print("end")

i = 6
while i < 7:
    image = cv2.imread('6.jpg')
    width, height, ch = image.shape
    for sigma in sigmas:
        print(sigma)
        all_images += 1
        # noisy_image = noisy(image, sigma)
        # cv2.imwrite(str(sigma) + '.png', noisy_image)
        # noisy_image = cv2.cvtColor(np.array(noisy_image), cv2.COLOR_RGB2GRAY)
        img1 = image[:width - 100, : height - 100]
        img2 = image[99:width - 1, 99: height - 1]
        img1 = cv2.cvtColor(np.array(noisy(img1, sigma)), cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(np.array(noisy(img2, sigma)), cv2.COLOR_RGB2GRAY)
        print("sigma: " + str(sigma))
        print("psnr: " + str(psnr(img1, img2)))
        print("mse: " + str(mean_squared_error(img1, img2)))
        print("ssim: " + str(ssim(img1, img2)))
        print("estimate_sigma:" + str(estimate_sigma(img1) + estimate_sigma(img2)))
        # print("entropy:" + str(entropy(img1, img2)))
        # cv2.imwrite(str(sigma) + '-1.png', img1)
        # cv2.imwrite(str(sigma) + '-2.png', img2)
        if estimate_sigma(img1) < 0.4 and estimate_sigma(img2) < 0.4:
            correct_pred += 1
        if complete_comparing(img1, img2) == 'Feature':
            features += 1
        # print('Noise for img1 ' + str(estimate_sigma(img1)))
        # print('Noise for img2 ' + str(estimate_sigma(img2)))
        # print('Winner for sigma=' + str(sigma))
        # print(test_translations(get_merge_parameters(img1, img2)[0],
        #                         get_translation_from_homograph(find_homograph(img1, img2))))
        # print('Feature-based')
        print(get_translation_from_homograph(find_homograph(img1, img2)))
        cv2.imwrite("out" + str(sigma) +'.jpg', merge_images(img1, img2, find_homograph(img1, img2)))
        # print('Fourier-Mellin:')
        # print(get_merge_parameters(img1, img2)[0])
    print(i)
    i += 1

print(all_images)
print(correct_pred)
print(features)

# image = cv2.imread('images/IMG0406.jpg')
# width, height, ch = image.shape
# sigmas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# for sigma in sigmas:
#     # noisy_image = noisy(image, sigma)
#     # cv2.imwrite(str(sigma) + '.png', noisy_image)
#     # noisy_image = cv2.cvtColor(np.array(noisy_image), cv2.COLOR_RGB2GRAY)
#     img1 = image[:width - 100, : height - 100]
#     img2 = image[99:width - 1, 99: height - 1]
#     img1 = cv2.cvtColor(np.array(noisy(img1, sigma)), cv2.COLOR_RGB2GRAY)
#     img2 = cv2.cvtColor(np.array(noisy(img2, sigma)), cv2.COLOR_RGB2GRAY)
#     cv2.imwrite(str(sigma) + '-1.png', img1)
#     cv2.imwrite(str(sigma) + '-2.png', img2)
#     print('Noise for img1 ' + str(estimate_sigma(img1)))
#     print('Noise for img2 ' + str(estimate_sigma(img2)))
#     print('Winner for sigma=' + str(sigma))
#     print(test_translations(get_merge_parameters(img1, img2)[0],
#           get_translation_from_homograph(find_homograph(img1, img2))))
#     print('Feature-based')
#     print(get_translation_from_homograph(find_homograph(img1, img2)))
#     print('Fourier-Mellin:')
#     print(get_merge_parameters(img1, img2)[0])
