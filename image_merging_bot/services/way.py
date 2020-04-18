from image_merging_bot.database.way import *
from image_merging_bot.database.models import Ways


def set_default_way(user_id):
    change_user_way(user_id, Ways["DEFAULT"])


def set_fourier_way(user_id):
    change_user_way(user_id, Ways["FOURIER"])


def set_feature_way(user_id):
    change_user_way(user_id, Ways["FEATURE"])


def get_current_way(user_id):
    return get_current_user_way(user_id).way
