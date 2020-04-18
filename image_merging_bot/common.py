import os

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
GET_FILE_PATH_URL = BASE_URL + "/getFile?file_id=<file_id>"
GET_FILE_URL = "https://api.telegram.org/file/bot{}".format(TOKEN) + "/<file_path>"

ADVICE_URL = "https://imgur.com/5MdN52R"