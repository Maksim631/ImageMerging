import json
from io import BytesIO

from PIL import Image
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import os
import requests
from rest_framework.response import Response

from snitching.fourier import get_merge_parameters

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
GET_FILE_PATH_URL = BASE_URL + "/getFile?file_id=<file_id>"
GET_FILE_URL = "https://api.telegram.org/file/bot{}".format(TOKEN) + "/<file_path>"
SEND_MESSAGE_URL = BASE_URL + "/sendMessage"
SEND_PHOTO_URL = BASE_URL + "/sendPhoto"


@api_view(['POST'])
@permission_classes((AllowAny,))
def handle(request):
    print("start")
    print(str(request))
    print(TOKEN)
    try:
        data = request.data
        print(data)
        chat_id = data["message"]["chat"]["id"]
        if data["message"]["photo"] is not None:
            handle_photo(data["message"]["photo"], chat_id)
        else:
            message = str(data["message"]["text"])

            first_name = data["message"]["chat"]["first_name"]

            response = "Please /start, {}".format(first_name)

            if "start" in message:
                response = "Hello {}".format(first_name)

            data = {"text": response.encode("utf8"), "chat_id": chat_id}

            requests.post(SEND_MESSAGE_URL, data)
            print("SUCCESS 1")
    except Exception as e:
        print(e)

    return Response(status=status.HTTP_200_OK)


def get_biggest_photos(photos):
    current_size = 0
    result = []
    current_photo = photos[0]
    for photo in photos:
        if photo["file_size"] > current_size:
            current_size = photo["file_size"]
        else:
            result.append(current_photo)
            current_size = 0
        current_photo = photo
    result.append(photos[-1])
    return result


def get_file(photo):
    file_id = photo["file_id"]
    file_path_response = requests.get(GET_FILE_PATH_URL.replace("<file_id>", file_id))
    print(file_path_response.json())
    file_path = file_path_response.json()["result"]["file_path"]
    file = requests.get(GET_FILE_URL.replace("<file_path>", file_path), allow_redirects=True)
    # print(file.content)
    return file.content


def handle_photo(photos, chat_id):
    print("Received image")
    i = 0
    photos = get_biggest_photos(photos)
    print(photos)
    image1 = Image.open(BytesIO(get_file(photos[0])))
    image2 = Image.open(BytesIO(get_file(photos[1])))
    parameters = get_merge_parameters(image1, image2)
    print(parameters)

    data = {"text": parameters, "chat_id": chat_id}
    requests.post(SEND_MESSAGE_URL, data)
    # for photo in photos:

    #     # open('image_' + str(i) + ".jpg").write(file.content)
    #     # print(file.content)
    #     # print(GET_FILE_URL.replace("<file_path>", file_path))
    #     data = {"photo": file_id, "chat_id": chat_id}
    #     requests.post(SEND_PHOTO_URL, data)
    #     print("SUCCESS 2")
