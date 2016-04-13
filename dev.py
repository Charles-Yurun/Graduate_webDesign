# -*- coding: utf-8 -*-
from mulan.app import create_app
from mulan.config import Dev

__author__ = 'simi'

app = create_app(config=Dev)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
