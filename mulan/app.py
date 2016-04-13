# -*- coding: utf-8 -*-
import os
import time
import datetime
import hashlib
import logging
from flask import g, render_template, make_response, jsonify
from ._flask import Flask
__author__ = 'simi'


def config_str_to_obj(cfg):
    if isinstance(cfg, basestring):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def create_app(config=None):
    app = Flask(
            __name__,
            template_folder='templates',
    )
    # app.config.from_pyfile('_settings.py')

    if 'MULAN_SETTINGS' in os.environ:
        app.config.from_envvar('MULAN_SETTINGS')

    # if isinstance(config, dict):
    #     app.config.update(config)
    # elif config:
    #     app.config.from_pyfile(os.path.abspath(config))
    config = config_str_to_obj(config)
    app.config.from_object(config)
    app.config.from_envvar("APP_CONFIG", silent=True)  # avaiable in the server

    app.static_folder = app.config.get('STATIC_FOLDER')
    app.config.update({'SITE_TIME': datetime.datetime.utcnow()})

    register_hooks(app)
    register_jinja(app)
    # register_database(app)

    register_routes(app)
    register_error_handlers(app)
    register_assets(app)
    register_leancloud(app)

    return app


def register_hooks(app):
    """Hooks for request."""
    from .utils.user import get_current_user

    @app.before_request
    def load_current_user():
        g.user = get_current_user()
        if g.user:
            g._before_request_time = time.time()

    @app.after_request
    def rendering_time(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response


def register_jinja(app):
    from . import filters

    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    def static_url(filename):
        if app.testing:
            return filename

        if filename in app._static_hash:
            return app._static_hash[filename]
        with open(os.path.join(app.static_folder, filename), 'r') as f:
            content = f.read()
            hsh = hashlib.md5(content).hexdigest()

        prefix = app.config.get('SITE_STATIC_PREFIX', '/static/')
        value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
        app._static_hash[filename] = value
        return value

    @app.context_processor
    def register_context():
        return dict(
            static_url=static_url,
            db=dict(
            )
        )

    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    app.jinja_env.filters['markdown'] = filters.markdown
    app.jinja_env.filters['timesince'] = filters.timesince
    app.jinja_env.filters['xmldatetime'] = filters.xmldatetime
    app.jinja_env.filters['_datetime'] = filters._datetime
    app.jinja_env.filters['date'] = filters.date
    app.jinja_env.filters['youtube'] = filters.youtube

    app.jinja_env.filters['college_type'] = filters.college_type
    app.jinja_env.filters['work_type'] = filters.work_type

def register_database(app):
    """Database related configuration."""
    #: prepare for database
    db.init_app(app)
    db.app = app
    #: prepare for cache
    # cache.init_app(app)


def register_routes(app):
    from .controllers import front, services, account, admin, college, work

    app.register_blueprint(college.bp, url_prefix='/college')
    app.register_blueprint(work.bp, url_prefix='/work')
    app.register_blueprint(front.bp, url_prefix='')

    return app


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        """
        The server understood the request, but is refusing to fulfill it.
        Authorization will not help and the request SHOULD NOT be repeated.
        If the request method was not HEAD and the server wishes to make public
        why the request has not been fulfilled, it SHOULD describe the reason for
        the refusal in the entity. If the server does not wish to make this
        information available to the client, the status code 404 (Not Found)
        can be used instead.
        """
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        """
        The server has not found anything matching the Request-URI. No indication
        is given of whether the condition is temporary or permanent. The 410 (Gone)
        status code SHOULD be used if the server knows, through some internally
        configurable mechanism, that an old resource is permanently unavailable
        and has no forwarding address. This status code is commonly used when the
        server does not wish to reveal exactly why the request has been refused,
        or when no other response is applicable.
        """
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        """
        The method specified in the Request-Line is not allowed for the resource
        identified by the Request-URI. The response MUST include an Allow header
        containing a list of valid methods for the requested resource.
        """
        return make_response(jsonify(error=str(error)), 405)

    @app.errorhandler(500)
    def server_error_page(error):
        import log
        log.exception(str(error))
        return make_response(jsonify(error=str(error)), 500)

    @app.errorhandler(501)
    def server_error_page(error):
        return render_template("501.html"), 501

        @app.errorhandler(Exception)
        def handle_exception(e):
            import log
            log.exception(e.message)

            return jsonify(ok=False, message=e.message)


def register_assets(app):
    from flask.ext.assets import Environment, Bundle

    assets = Environment(app)
    js_common = Bundle(
            'js/jquery-1.10.2.min.js',
            'js/bootstrap.min.js',
            'js/ripples.min.js',
            'js/material.min.js',
            filters='jsmin',
            output='app.js')

    assets.register('js_common', js_common)

    css = Bundle(
            'css/bootstrap.min.css',
            'css/ripples.min.css',
            'css/material-wfont.min.css',
            # 'css/common.css',
            filters='cssmin',
            output='app.css'
    )

    assets.register('css_common', css)

    assets.init_app(app)


def register_leancloud(app):
    import leancloud

    leancloud.init(app.config['APP_ID'], master_key=app.config['MASTER_KEY'])
