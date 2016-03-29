# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request
from leancloud import Query, Object

from ..models import BaseQuery

__author__ = 'Simi'
__all__ = ['bp']
bp = Blueprint('work', __name__)

type_to_name = {3: '就业公告',
                4: '就业新闻',
                13: '每周来校招聘单位',
                15: '用人单位来校招聘信息发布',
                16: '用人单位网络招聘信息发布'
                }


@bp.route('/news_type=<news_type>')
def index(news_type):
    if news_type is None:
        news_type = 1
    else:
        news_type = int(news_type)
    page = int(request.args.get('page', 1))
    if not page:
        return abort(404)
    paginator = BaseQuery('Work', news_type, 'news_time').paginate(page, 20)
    return render_template('work/index.html', paginator=paginator,
                           endpoint='work.index', news_type=news_type,
                           news_title=type_to_name[news_type])


@bp.route('/news_id=<id>', methods=['GET'])
def content(id):
    if id is None:
        abort(404)
    news = Query(Object.extend('Work')).get(id)
    return render_template('work/content.html', news = news)