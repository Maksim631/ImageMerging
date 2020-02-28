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

requests.post(BASE_URL, DATA)

# curl --request POST --url
# https://api.telegram.org/bot459903168:APHruyw7ZFj5qOJmJGeYEmfFJxil-z5uLS8/setWebhook
# --header 'content-type: application/json' --data
# '{"url": "https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url"}'
