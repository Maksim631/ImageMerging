import io

import requests
from PIL import Image

from image_merging_bot.common import GET_FILE_PATH_URL, GET_FILE_URL
from image_merging_bot.database.photo import delete_user_photos as db_delete
from image_merging_bot.database.photo import save_photo, get_user_photos as db_get
from image_merging_bot.services.sender import send_image
from image_merging_bot.services.snitching.fourier import get_merge_parameters, merge_with_parameters


def delete_user_photos(user_id):
    db_delete(user_id)


def add_photo(user_id, photo_url):
    save_photo(user_id, photo_url)


def get_user_photos(user_id):
    return db_get(user_id)


def get_user_photos_count(user_id):
    return len(get_user_photos(user_id))


def get_file(file_id):
    file_path_response = requests.get(GET_FILE_PATH_URL.replace("<file_id>", file_id))
    print(file_path_response.json())
    file_path = file_path_response.json()["result"]["file_path"]
    print(GET_FILE_URL.replace("<file_path>", file_path))
    file = requests.get(GET_FILE_URL.replace("<file_path>", file_path), allow_redirects=True)
    # print(file.content)
    return Image.open(io.BytesIO(file.content))


def stitch_images(user_id):
    photos = get_user_photos(user_id)
    if len(photos) == 0:
        return "No photos to snitch"
    else:
        i = 0
        print(photos[0].photo_id)
        real_image_1 = get_file(photos[0].photo_id)
        real_image_2 = get_file(photos[1].photo_id)
        print("GOT IMAGES")
        print(get_merge_parameters(real_image_1, real_image_2))
        result_image = merge_with_parameters(real_image_1, real_image_2,
                                             get_merge_parameters(real_image_1, real_image_2))
        bio = io.BytesIO()
        bio.name = 'image.jpeg'
        result_image.save(bio, 'JPEG')
        bio.seek(0)
        send_image(user_id, bio)
        delete_user_photos(user_id)
    return "Result was sent"
