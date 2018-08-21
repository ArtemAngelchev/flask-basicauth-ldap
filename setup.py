# -*- coding: utf-8 -*-
from setuptools import setup


version = __import__('flask_basicauth_ldap').__version__


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='Flask-BasicAuth-LDAP',
    long_description=read('README.rst'),
    long_description_content_type="text/markdown",
    version=version,
    description=(
        'Flask extension that provides an easy way to protect certain views '
        'of an application with LDAP and HTTP basic access authentication.'
    ),
    author='Angelchev Artem',
    author_email='artangelchev@gmail.com',
    url='https://github.com/ArtemAngelchev/flask-basicauth-ldap',
    keywords=[
        'ldap', 'flask', 'api', 'rest', 'auth', 'basicauth',
    ],
    install_requires=['Flask>=0.10', 'ldap3'],
    license='MIT',
    py_modules=['flask_basicauth_ldap'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
