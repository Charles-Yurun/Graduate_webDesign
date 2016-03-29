# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import models_committed
from flask import g

from ._base import *
from .account import *

__author__ = 'Simi'


def _clear_cache(sender, changes):
    for model, operation in changes:
        if isinstance(model, Account) and operation != 'update':
            cache.delete('status-account')


models_committed.connect(_clear_cache)
