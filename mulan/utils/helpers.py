# -*- coding: utf-8 -*-
import datetime

__author__ = 'Simi'


def force_int(value, default=1):
    try:
        return int(value)
    except:
        return default


def is_email(value):
    import re
    return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) != None


def timesince(value):
    now = datetime.datetime.utcnow()
    delta = now - value
    if delta.days > 365:
        return '{} years ago'.format(delta.days / 365)
    if delta.days > 30:
        return '{} months ago'.format(delta.days / 30)
    if delta.days > 0:
        return '{} days ago'.format(delta.days)
    if delta.seconds > 3600:
        return '{} hours ago'.format(delta.seconds / 3600)
    if delta.seconds > 60:
        return '{} minutes ago'.format(delta.seconds / 60)
    return 'just now'


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
