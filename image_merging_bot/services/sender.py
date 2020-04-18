import requests

from image_merging_bot.common import BASE_URL

SEND_MESSAGE_URL = BASE_URL + "/sendMessage"
SEND_PHOTO_URL = BASE_URL + "/sendPhoto"


def send_text(chat_id, text):
    data = {"text": text, "chat_id": chat_id}
    requests.post(SEND_MESSAGE_URL, data)


def send_image_by_url(chat_id, image_path):
    print("Sending Photo")
    data = {"chat_id": chat_id, "photo": image_path}
    requests.post(SEND_PHOTO_URL, data=data)


def send_image(chat_id, image):
    print("Sending Photo")
    files = {'photo': image}
    requests.post(SEND_PHOTO_URL + f"?chat_id={chat_id}", files=files)
