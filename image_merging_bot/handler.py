from io import BytesIO

from PIL import Image
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import os
import requests
from rest_framework.response import Response

from image_merging_bot.models.models import Photo
from snitching.fourier import get_merge_parameters

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
GET_FILE_PATH_URL = BASE_URL + "/getFile?file_id=<file_id>"
GET_FILE_URL = "https://api.telegram.org/file/bot{}".format(TOKEN) + "/<file_path>"
SEND_MESSAGE_URL = BASE_URL + "/sendMessage"
SEND_PHOTO_URL = BASE_URL + "/sendPhoto"

images = {}


@api_view(['POST'])
@permission_classes((AllowAny,))
def handle(request):
    try:
        data = request.data
        print(data)
        chat_id = data["message"]["chat"]["id"]
        if "photo" in data["message"]:
            print("2")
            handle_photo(data["message"]["photo"], chat_id, data["message"]["photo"]["media_group_id"])
        else:
            text = str(data["message"]["text"])
            if "snitch" in text:
                snitch_images(chat_id, text.split(" ")[1])
            if "images" in text:
                data = {"text": str(Photo.objects.all()), "chat_id": chat_id}
                requests.post(SEND_MESSAGE_URL, data)
            else:
                default_handler(chat_id, data["message"])

    except Exception as e:
        print(e)


    return Response(status=status.HTTP_200_OK)


def default_handler(chat_id, message):
    text = message["text"]
    first_name = message["chat"]["first_name"]
    response = "Please /start, {}".format(first_name)
    if "start" in text:
        response = "Hello {}".format(first_name)
    print(response)
    print(chat_id)
    data = {"text": response.encode("utf8"), "chat_id": chat_id}
    a = requests.post(SEND_MESSAGE_URL, data)
    print(a)
    print("SUCCESS 1")


def get_file(photo):
    file_id = photo["file_id"]
    file_path_response = requests.get(GET_FILE_PATH_URL.replace("<file_id>", file_id))
    print(file_path_response.json())
    file_path = file_path_response.json()["result"]["file_path"]
    print(GET_FILE_URL.replace("<file_path>", file_path))
    file = requests.get(GET_FILE_URL.replace("<file_path>", file_path), allow_redirects=True)
    # print(file.content)
    return file.content


def snitch_images(chat_id, group_id):
    photos = Photo.objects.filter(group=group_id)
    print(photos)
    for photo in photos:
        image1 = Image.open(BytesIO(get_file(photo.photo_id)))
        image2 = Image.open(BytesIO(get_file(photo.photo_id)))
        parameters = get_merge_parameters(image1, image2)
        print(parameters)
        data = {"text": parameters, "chat_id": chat_id}
        requests.post(SEND_MESSAGE_URL, data)


def handle_photo(photos, chat_id, media_group_id):
    print("Received image with group_id = ", media_group_id)
    print(images)
    photo_db = Photo()
    photo_db.group = media_group_id
    photo_db.photo_id = photos[-1]["file_id"]
    photo_db.save()
    response = "Photo added to group " + media_group_id
    data = {"text": response, "chat_id": chat_id}
    requests.post(SEND_MESSAGE_URL, data)
    # for photo in photos:

    #     # open('image_' + str(i) + ".jpg").write(file.content)
    #     # print(file.content)
    #     # print(GET_FILE_URL.replace("<file_path>", file_path))
    #     data = {"photo": file_id, "chat_id": chat_id}
    #     requests.post(SEND_PHOTO_URL, data)
    #     print("SUCCESS 2")
