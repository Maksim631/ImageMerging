import json

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import os
import requests
from rest_framework.response import Response

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


@api_view(['POST'])
@permission_classes((AllowAny,))
def handle(request):
    print("start")
    print(str(request))
    print(TOKEN)
    try:
        data = json.loads(request.data)
        print(data)
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = "Please /start, {}".format(first_name)

        if "start" in message:
            response = "Hello {}".format(first_name)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)
        print("SUCCESS")
    except Exception as e:
        print(e)

    return Response(status=status.HTTP_200_OK)