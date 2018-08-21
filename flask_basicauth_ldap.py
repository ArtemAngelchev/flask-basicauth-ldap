# -*- coding: utf-8 -*-
import os
from functools import wraps

from flask import g, jsonify, request
from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPBindError, LDAPPasswordIsMandatoryError

__version__ = '0.0.0a1.dev2'


class LDAPBasicAuth:
    def __init__(self, app=None, host=None, port=None, domain=None):
        if app is not None:
            self.init_app(app, host=host, port=port, domain=domain)
        else:
            self.app = None

    def init_app(self, app, host=None, port=None, domain=None):
        self.app = app
        self.host = host
        self.port = port
        self.domain = domain
        self._unauthorizedfunc = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if value is None:
            value = self._get_config('LDAP_HOST')
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if value is None:
            value = self._get_config('LDAP_PORT')
            value = int(value) if value else value
        self._port = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value is None:
            value = self._get_config('LDAP_DOMAIN')
        self._domain = value

    def _get_config(self, config):
        return self.app.config.get(config) or os.getenv(config)

    def authenticate(self):
        auth = request.authorization
        if auth and auth.type == 'basic':
            login, password = auth.username, auth.password
            try:
                server = Server(self.host, port=self.port)
                user = f'{login}@{self.domain}'
                conn = Connection(
                    server, auto_bind=True, user=user, password=password
                )
            except (LDAPPasswordIsMandatoryError, LDAPBindError):
                return False
            else:
                g.login = conn.extend.standard.who_am_i()
                return True
        return False

    def unauthorizedhandler(self, route):
        self._unauthorizedfunc = route

    def challenge(self):
        if self._unauthorizedfunc:
            return self._unauthorizedfunc()
        return (
            jsonify(
                {
                    'status': 'error',
                    'message': 'Invalid username/password specified'
                }
            ), 401
        )

    def required(self, route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            if self.authenticate():
                return route(*args, **kwargs)
            return self.challenge()
        return wrapper
