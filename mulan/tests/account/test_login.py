# -*- coding:utf-8 -*-
import unittest
import sys

from mulan.tests.base import TestBase

sys.path.append("../..")
__author__ = 'Simi'


class LoginTestCase(TestBase):

    def test_signin(self):
        #  不正确的 用户名/密码
        rv = self.signin('simi', 'imnotpassword')
        # print '不正确的 用户名/密码：', rv.data
        assert '用户名/密码不正确' in rv.data

        # 正确的用户名密码
        rv = self.signin('simi', 'simiwei')
        print '正确的：', rv.data
        # # assert 'true' in rv.data


if __name__ == '__main__':
    unittest.main()
