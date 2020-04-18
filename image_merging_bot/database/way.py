from image_merging_bot.database.models import Way, Ways


def change_user_way(user_id, way):
    current_way = get_current_user_way(user_id)
    print(way)
    current_way.way = way
    current_way.save()


def get_current_user_way(user_id):
    current_way = Way.objects.filter(user_id=user_id)
    if current_way:
        return current_way.first()
    else:
        current_way = Way()
        current_way.user_id = user_id
        current_way.way = Ways["DEFAULT"]
        print(Ways["DEFAULT"])
        current_way.save()
    return current_way
