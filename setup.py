#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# https://github.com/kennethreitz/setup.py ✨ 🍰 ✨

NAME = 'scrapy-link-filter'
DESCRIPTION = 'Spider Middleware that allows a Scrapy Spider to filter requests.'
KEYWORDS = 'scrapy link filter'
URL = 'https://github.com/croqaz/scrapy-link-filter'
AUTHOR = 'Cristi Constantin'
EMAIL = 'cristi.constantin@live.com'

REQUIRES_PYTHON = '>=3.6.0'
REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, NAME.replace('-', '_'), '__version__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    version=about['__version__'],
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=KEYWORDS,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license='BSD',
    packages=find_packages(),
    platforms=['Any'],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Framework :: Scrapy',
    ],
)
