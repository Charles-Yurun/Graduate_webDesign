# -*- coding: utf-8 -*-
from leancloud import Query

__author__ = 'Simi'
# __all__ = ('Account')


class Account:
    @staticmethod
    def get(id):
        try:
            return Query("_User").get(id)
        except:
            return None

    @staticmethod
    def get_by_username(username):
        try:
            return Query('_User').equal_to('username', username).first()
        except:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return Query('_User').equal_to('email', email).first()
        except:
            return None
