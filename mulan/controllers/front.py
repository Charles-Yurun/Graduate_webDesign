# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, json
from leancloud import Object, Query

__author__ = 'Simi'
__all__ = ['bp']
bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # return render_template('front/index.html')
    college_news = Query(Object.extend('College')).descending(key='news_time'). \
        limit(10).select('news_title', 'news_time').find()
    work_news = Query(Object.extend('Work')).descending(key='news_time'). \
        limit(10).select('news_title', 'news_time').find()
    return render_template('front/index.html', college_news=college_news,
                           work_news=work_news)


@bp.route('/_get_today_college_news')
def get_today_college_news():
    college_news = Query(Object.extend('College')).descending(key='news_time'). \
        select('news_title', 'news_type', 'news_time').find()
    print type(college_news)
    return json.dumps()
