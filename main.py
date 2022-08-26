from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']

birthday_z = os.environ['ZBIRTHDAY']
birthday_l = os.environ['LBIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id_l = os.environ["USER_ID_L"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday_l():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_l, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday_z():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_z, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  # words = requests.get("https://api.shadiao.pro/chp")
  words = requests.get("https://devapi.qweather.com/v7/indices/1d?location=121.48,31.40&key=cdf6c29c017144a49986d73463f868ca&type=8")
  if words.status_code != 200:
    return get_words()
  # return words.json()['data']['text']
  return words.json()['daily'][0]['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low, high = get_weather()
data = {"diqu":{"value":city},"tianqi":{"value":wea},"low":{"value":low},"high":{"value":high},"lianai":{"value":get_count()},"lshengri":{"value":get_birthday_l()},"zshengri":{"value":get_birthday_z()},"jinju":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res = wm.send_template(user_id_l, template_id, data)
print(res)
