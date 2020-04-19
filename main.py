import cv2
import numpy as np
from skimage.restoration import estimate_sigma

from feature import find_homograph
from fourier import get_merge_parameters
from utils import get_translation_from_homograph, noisy, test_translations, complete_comparing

correct_pred = 0
features = 0
all_images = 0
sigmas = np.linspace(0.1, 1.1, 11)
blurs = np.linspace(1, 7, 4)
print(blurs)
i = 1
while i < 12:
    image = cv2.imread(f"{i}.jpg")
    width, height, ch = image.shape
    for sigma in sigmas:

        img1 = image[:width - 100, : height - 100]
        img2 = image[99:width - 1, 99: height - 1]
        img1 = cv2.cvtColor(np.array(noisy(img1, sigma)), cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(np.array(noisy(img2, sigma)), cv2.COLOR_RGB2GRAY)
        for sigma_blur in blurs:
            sigma_blur = int(sigma_blur)
            # print(sigma_blur)
            img1 = cv2.GaussianBlur(img1, (sigma_blur, sigma_blur), cv2.BORDER_DEFAULT)
            img2 = cv2.GaussianBlur(img2, (sigma_blur, sigma_blur), cv2.BORDER_DEFAULT)

            try:
                comparing_result = complete_comparing(img1, img2)
                if comparing_result == "same":
                    correct_pred += 1
                elif (estimate_sigma(img1) + estimate_sigma(img2) < 0.8
                    and comparing_result == 'Feature') or \
                        (estimate_sigma(img1) + estimate_sigma(img2) >= 0.8
                         and comparing_result == 'Fourier-Mellin'):
                    correct_pred += 1

                print(test_translations(get_merge_parameters(img1, img2)[0],
                                        get_translation_from_homograph(find_homograph(img1, img2))))
                print('Feature-based')
                print(get_translation_from_homograph(find_homograph(img1, img2)))
                # cv2.imwrite("out" + str(sigma) +'.jpg', merge_images(img1, img2, find_homograph(img1, img2)))
                print('Fourier-Mellin:')
                print(get_merge_parameters(img1, img2)[0])
                all_images += 1
            except Exception:
                print("Skip")
    print(i)
    i += 1

print(f"all_images-{all_images}")
print(f"correct_pred-{correct_pred}")
print(f"features-{features}")

