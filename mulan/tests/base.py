# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase
from flask import url_for
# from mulan.models import db

__author__ = 'Simi'

__all__ = ['TestBase']


class TestBase(TestCase):
    def create_app(self):
        from mulan.app import create_app
        from mulan.config import Testing
        app = create_app(config=Testing)
        return app

    def setUp(self):
        print 'set up'
        # from mulan.app import create_app
        # from mulan.config import Testing
        # app = create_app(config=Testing)
        # self.client = app.test_client()

        # db.create_all()

    def tearDown(self):
        print 'tear down'
        # db.session.remove()
        # db.drop_all()

    def url_for(self, *args, **kwargs):
        with self.app.test_request_context():
            return url_for(*args, **kwargs)

    def signin(self, username, password):
        rv = self.client.post(self.url_for('account.signin'), data=dict(
                account=username,
                password=password
        ), follow_redirects=True)
        return rv

