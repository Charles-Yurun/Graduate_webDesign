# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, jsonify, request, redirect, url_for, g, \
    flash, current_app

__author__ = 'Simi'
__all__ = ['bp']

# 提供各种服务
bp = Blueprint('services', __name__)


@bp.route('/')
def index():
    """

    """
    pass
