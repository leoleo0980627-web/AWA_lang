# ~/awa/utils/helpers.py
# 雜用函式

import datetime
import time
import random

def check_holidays():
    today = datetime.date.today()
    christmas = (today.month == 12 and today.day == 25)
    new_year = (today.month == 1 and today.day == 1)
    april_fools = (today.month == 4 and today.day == 1)
    return christmas, new_year, april_fools

def set_birthday(month, day):
    today = datetime.date.today()
    return (today.month == month and today.day == day)

def random_fortune():
    fortunes = [
        "U will write buggy code today",
        "A segmentation fault is in your future",
        "U will forget a semicolon",
        "U will spend 3 hours debugging a typo"
    ]
    return random.choice(fortunes)
