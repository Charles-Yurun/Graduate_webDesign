# -*- coding: utf-8 -*-
from math import ceil

from flask import has_request_context, request, abort
from leancloud import Query, Object

__author__ = 'zhuyurun'
__all__ = [
   'BaseQuery', 'Pagination'
]


class BaseQuery:
    def __init__(self, query_class, news_type, descend_key):
        self.query_class = query_class
        self.descend_key = descend_key
        self.news_type = news_type

    def paginate(self, page=None, per_page=None, error_out=True):
        if has_request_context():
            if page is None:
                try:
                    page = int(request.args.get('page', 1))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    page = 1

            if per_page is None:
                try:
                    per_page = int(request.args.get('per_page', 20))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    per_page = 1

        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if error_out and page < 1:
            abort(404)

        items = Query(Object.extend(self.query_class)).equal_to('news_type', self.news_type).\
            descending(key=self.descend_key).skip((page - 1) * per_page).limit(per_page).\
            select('news_title','news_time').find()

        if not items and page != 1 and error_out:
            abort(404)

        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = Query(Object.extend(self.query_class)).equal_to('news_type', self.news_type).count()

        return Pagination(page, per_page, total, items)


class Pagination(Object):

    def __init__(self, page, per_page, total, items, **attrs):
        super(Pagination, self).__init__(**attrs)
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=5):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
                    (self.page - left_current - 1 < num < self.page + right_current) or \
                    num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

