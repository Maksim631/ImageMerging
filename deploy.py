import re
import requests
import os


def find(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
    return url


f = open("deploy.out", "r")
serverless = f.read()
aws_url = find(serverless)[0] + '/dev/bot'
print(aws_url)

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}/setWebhook".format(TOKEN)
DATA = {
    'url': aws_url
}

print(requests.post(BASE_URL, DATA))

# curl --request POST --url https://api.telegram.org/bot901222655:AAHXyriyQfZOc_-mEhroRNTpwbwtWo9Zqqg/setWebhook --header 'content-type: application/json' --data '{"url": "https://kdncs60my4.execute-api.us-east-1.amazonaws.com/dev/bot"}'
