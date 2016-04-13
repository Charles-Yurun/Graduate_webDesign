# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, json, request
from leancloud import Object, Query

__author__ = 'Simi'
__all__ = ['bp']
bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    college_news = Query(Object.extend('College')).descending(key='news_time'). \
        limit(10).select('news_title', 'news_time').find()

    work_news = Query(Object.extend('Work')).descending(key='news_time'). \
        limit(10).select('news_title', 'news_time').find()

    notice_news = Query(Object.extend('College')).equal_to(key='news_type', value=10).\
        descending(key='news_time').limit(10).select('news_title', 'news_time').find()

    recruit_news = Query(Object.extend('Work')).equal_to(key='news_type', value=16).\
        descending(key='news_time').limit(10).select('news_title', 'news_time').find()

    return render_template('front/index.html', college_news=college_news, work_news=work_news,
                           notice_news=notice_news, recruit_news=recruit_news)
