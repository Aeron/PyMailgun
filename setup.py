# coding: utf-8
from setuptools import setup
import mailgun

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
