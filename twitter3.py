import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_twitter_json():
    """
    This function uses Twitter API to get the information about the user
    and writes it in json file
    """
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1): return
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    with open("try_new.json", "w", encoding="utf-8") as json_file:
        json.dump(js, json_file, ensure_ascii=False)

    return "try_new.json"