#!/usr/bin/env python
# coding: utf-8
import os
import sys

from setuptools import setup, __version__ as setuptools_version
import mailgun

if sys.argv[-1] == 'publish':
	if setuptools_version >= '0.8':
		os.system('python setup.py sdist sdist_wheel upload')
	else:
		os.system('python setup.py sdist upload')
	sys.exit()


setup(
	name=mailgun.__title__,
	version=mailgun.__version__,
	packages=[
		'mailgun',
	],
	package_dir={
		'mailgun': 'mailgun'
	},
	scripts=[],
	install_requires=['requests'],
	package_data={
		'': [],
	},
	author=mailgun.__author__,
	author_email="aeron@aeron.cc",
	url="https://github.com/Aeron/PyMailgun",
	description="Simple Mailgun API wrapper.",
	license=mailgun.__license__,
	keywords="mailgun api wrapper",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		'Natural Language :: English',
		"License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
		"Topic :: Communications",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: Implementation :: CPython",
		"Programming Language :: Python :: Implementation :: PyPy",
	]
)
