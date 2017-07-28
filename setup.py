#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages
import shop_currencies

with open('README.rst') as fd:
    README = fd.read()

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
#    'Programming Language :: Python :: 2.7',
#    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    author="Richard Case",
    author_email="rich@racitup.com",
    name="djangoshop-currencies",
    packages=find_packages(exclude=['docs']),
    version=shop_currencies.__version__,
    description="Django-SHOP integration with django-currencies",
    long_description=README,
    url='https://github.com/racitup/djangoshop-currencies',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    keywords= ['Django', 'Django-SHOP'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.10.0,<1.11',
        'django-currencies>=0.4.0',
        'django-shop>=0.10.2,<0.11',
    ],
)
