# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request
from leancloud import Query, Object

from ..models import BaseQuery

__author__ = 'Simi'
__all__ = ['bp']
bp = Blueprint('college', __name__)

type_to_name = {1: '桂电要闻',
                2: '校园快讯',
                4: '校内通知',
                6: '学术会议',
                8: '学院动态',
                9: '媒体桂电',
                10: '公 告'}


@bp.route("/", methods=['GET'])
def index():
    page = int(request.args.get('page', 1))
    if not page:
        return abort(404)
    paginator = BaseQuery(query_class='College', descend_key='news_time').paginate(page, 20)
    return render_template('college/index.html', paginator=paginator,
                           endpoint='college.index')


@bp.route(u'/type=<news_type>', methods=['GET'])
def index_type(news_type):
    if news_type is None:
        news_type = 1
    else:
        news_type = int(news_type)
    page = int(request.args.get('page', 1))
    if not page:
        return abort(404)
    paginator = BaseQuery('College', news_type, 'news_time').paginate(page, 20)
    return render_template('college/index_type.html', paginator=paginator,
                           endpoint='college.index_type', news_type=news_type,
                           news_title=type_to_name[news_type])


@bp.route('/<id>', methods=['GET'])
def content(id):
    if id is None:
        abort(404)
    news = Query(Object.extend('College')).get(id)
    print news.created_at
    return render_template('college/content.html', news=news)
