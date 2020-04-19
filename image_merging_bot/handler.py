from io import BytesIO

from PIL import Image
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import requests
from rest_framework.response import Response

from image_merging_bot.common import ADVICE_URL
from image_merging_bot.database.models import Photo
from image_merging_bot.services.photo import get_user_photos_count, snitch_images
from image_merging_bot.services.sender import send_text, send_image, send_image_by_url
from image_merging_bot.services.way import set_fourier_way, set_feature_way, set_default_way, get_current_way


@api_view(['POST'])
@permission_classes((AllowAny,))
def handle(request):
    try:
        data = request.data
        print(data)
        chat_id = data["message"]["chat"]["id"]
        found = False
        if "photo" in data["message"]:
            handle_photo(data["message"]["photo"], chat_id)
            found = True
        text = str(data["message"]["text"])
        if "snitch" in text:
            send_text(chat_id, snitch_images(chat_id))
            found = True
        if "images" in text:
            send_text(chat_id, get_user_photos_count(chat_id))
            found = True
        if "fourier" in text:
            set_fourier_way(chat_id)
            send_text(chat_id, "Set snitching method to Fourier-Mellin transform")
            found = True
        if "feature" in text:
            set_feature_way(chat_id)
            send_text(chat_id, "Set snitching method to feature based")
            found = True
        if "default" in text:
            set_default_way(chat_id)
            send_text(chat_id, "Set snitching method to default")
            found = True
        if "advice" in text:
            send_image_by_url(chat_id, ADVICE_URL)
            found = True
        if "current" in text:
            send_text(chat_id, get_current_way(chat_id))
            found = True
        if not found:
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
    send_text(chat_id, response.encode("utf8"))
    print("SUCCESS 1")


# def snitch_images(chat_id):
#     send_text(chat_id, "SNITCH")
#
    # photos = Photo.objects.filter(group=group_id)
    # print(photos)
    # for photo in photos:
    #     image1 = Image.open(BytesIO(get_file(photo.photo_id)))
    #     image2 = Image.open(BytesIO(get_file(photo.photo_id)))
    #     parameters = get_merge_parameters(image1, image2)
    #     print(parameters)
    #     data = {"text": parameters, "chat_id": chat_id}
    #     requests.post(SEND_MESSAGE_URL, data)


def handle_photo(photos, chat_id):
    print("Received image with group_id = ", chat_id)
    photo_db = Photo()
    photo_db.user_id = chat_id
    photo_db.photo_id = photos[-1]["file_id"]
    photo_db.save()
    response = "Photo added"
    send_text(chat_id, response)
    # for photo in photos:

    #     # open('image_' + str(i) + ".jpg").write(file.content)
    #     # print(file.content)
    #     # print(GET_FILE_URL.replace("<file_path>", file_path))
    #     data = {"photo": file_id, "chat_id": chat_id}
    #     requests.post(SEND_PHOTO_URL, data)
    #     print("SUCCESS 2")
