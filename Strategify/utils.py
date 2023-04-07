from datetime import datetime
from datetime import timedelta
from .constants import *
import random
import string
import os
import base64

def subtarctdays(startdate,days):
    date_format = '%Y-%m-%d'
    dtObj = datetime.strptime(startdate, date_format)
    past_date = dtObj - timedelta(days=days)
    past_date_str = past_date.strftime(date_format)
    return past_date


def extractMaximum(ss):
    num, res = 0, 0
    for i in range(len(ss)):
        if ss[i] >= "0" and ss[i] <= "9":
            num = num * 10 + int(int(ss[i]) - 0)
        else:
            res = max(res, num)
            num = 0
          
    return max(res, num)

def convertTime(time):
    time = str(time).split(":")
    if (time[0] == "0" and time[1] == "00" and time[2] == "00"):
        return "0 sec ago"
    elif time[0] == "0" and time[1] == "00" and time[2] != "00":
        return str(time[2]) + " sec ago"
    elif time[0] == "0" and time[1] != "00":
        return str(time[1]) + " min ago"
    elif time[0] != "0":
        return str(time[0]) + " hours ago"
    else:
        print(ERROR)



def generateRandomURL():
    length = 10
    URL = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return URL


def generateRandomUID():
    UID = base64.b64encode(os.urandom(6)).decode('ascii')
    print("UID: ",UID)
    return UID


def todayDate():
    return datetime.today().strftime('%Y-%m-%d')


def todayTime():
    return datetime.now().strftime('%H:%M:%S')