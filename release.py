# -*- coding: utf-8 -*-
from mulan.app import create_app
from mulan.config import Release
from mulan.log import logger
__author__ = 'simi'

app = create_app(config=Release)

if __name__ == "__main__":
    logger.info('重启服务')
    app.run(host='0.0.0.0', port=5000, threaded=True)
