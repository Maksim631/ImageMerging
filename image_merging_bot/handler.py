import json

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import os
import requests
from rest_framework.response import Response

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
GET_FILE_PATH_URL = BASE_URL + "/getFile?file_id=<file_id>"
GET_FILE_URL = BASE_URL + "/<file_path>"
SEND_MESSAGE_URL = BASE_URL + "/sendMessage"


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


def handle_photo(photos, chat_id):
    print("Received image")
    for photo in photos:
        file_path = requests.get(GET_FILE_PATH_URL.replace("<file_id>", photo["file_id"]))
        print(file_path)
        file = requests.get(GET_FILE_URL.replace("<file_path>", file_path.json()["file_path"]))
        data = {"text": "image", "chat_id": chat_id, photo: file}
        requests.post(SEND_MESSAGE_URL, data)
        print("SUCCESS 2")
