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

def get_week_day(date):
  week_day_dict = {
      0: '星期一',
      1: '星期二',
      2: '星期三',
      3: '星期四',
      4: '星期五',
      5: '星期六',
      6: '星期天',
  }
  day_color_dict = {
    0: '#999999',
    1: '#999999',
    2: '#999999',
    3: '#999999',
    4: '#ffc0cb',
    5: '#ffc0cb',
    6: '#ffc0cb',
  }
  day = date.weekday()
  return week_day_dict[day], day_color_dict[day]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather['humidity']

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
wea, low, high, humidity = get_weather()
dayOfWeek, dayColor = get_week_day(today)
data = {"riqi":{"value":dayOfWeek,"color":dayColor},"diqu":{"value":city},"tianqi":{"value":wea},"shidu":{"value":humidity},"low":{"value":low},"high":{"value":high},"lianai":{"value":get_count()},"lshengri":{"value":get_birthday_l()},"zshengri":{"value":get_birthday_z()},"jinju":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res = wm.send_template(user_id_l, template_id, data)
print(res)
