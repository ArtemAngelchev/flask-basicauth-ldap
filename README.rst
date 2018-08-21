Flask-BasicAuth-LDAP
====================

Flask-BasicAuth-LDAP is a Flask extension that provides an easy way to protect
certain views of an application with `LDAP`_ and HTTP `basic access authentication`_

.. _LDAP: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol
.. _basic access authentication: https://en.wikipedia.org/wiki/Basic_access_authentication

Install
-------

::

    pip install flask-basicauth-ldap

Quickstart
----------

::

    from flask import Flask, jsonify
    from flask_basicauth_ldap import LDAPBasicAuth

    app = Flask(__name__)
    auth = LDAPBasicAuth(app)

    app.config['LDAP_HOST'] = 'ldap://test_host'
    app.config['LDAP_PORT'] = 'test_port'
    app.config['LDAP_DOMAIN'] = 'test_domain'


    @app.route('/secret', methods=['GET'])
    @auth.required
    def secret_view():
       return jsonify({'status': 'secret'})

If you want to change a response on the unauthorized access, just use
`unauthorizedhandler` to register function that should return `Response` object

::

   @auth.unauthorizedhandler
   def custom_unathorized_view():
      return jsonify({'message': 'Athorize first'}), 401
