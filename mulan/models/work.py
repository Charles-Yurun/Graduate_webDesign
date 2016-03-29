from leancloud import Object, Query
from flask import _request_ctx_stack, abort, has_request_context, request

__all__ = ['Work']


class Work(Object):

    @property
    def news_time(self):
        return self.get('news_time')

    @news_time.setter
    def news_time(self, value):
        return self.set('news_time', value)

    @property
    def news_url(self):
        return self.get('news_url')

    @news_url.setter
    def news_url(self, value):
        return self.set('news_url', value)

    @property
    def news_title(self):
        return self.get('news_title')

    @news_title.setter
    def news_title(self, value):
        return self.set('news_title', value)

    @property
    def news_content(self):
        return self.get('news_content')

    @news_content.setter
    def news_content(self, value):
        return self.set('news_content', value)

    @property
    def news_type(self):
        return self.get('news_type')

    @news_type.setter
    def news_type(self, value):
        return self.set('news_type', value)

    @property
    def news_attachment(self):
        return self.get('news_attachment')

    @news_attachment.setter
    def news_attachment(self, value):
        return self.set('news_attachment', value)

    @property
    def news_other(self):
        return self.get('news_other')

    @news_other.setter
    def news_other(self, value):
        return self.set('news_other', value)

    @staticmethod
    def get(id):
        try:
            return Query('College').get(id)
        except:
            return None
