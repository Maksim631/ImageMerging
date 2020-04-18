from image_merging_bot.database.models import Photo


def get_user_photos(user_id):
    return Photo.objects.filter(user_id=user_id)


def save_photo(user_id, photo_url):
    photo_db = Photo()
    photo_db.chat_id = user_id
    photo_db.photo_id = photo_url
    photo_db.save()


def delete_user_photos(user_id):
    Photo.objects.filter(user_id=user_id).delete()
