# coding: utf-8
from setuptools import setup

setup(
	name="pymailgun",
	version="0.1.49",
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
	author=u"Eugene “Aeron” Glybin",
	author_email="aeron@aeron.cc",
	url="https://github.com/Aeron/PyMailgun",
	description="Simple Mailgun API wrapper. Only Messages, Mailing Lists (with bulk create) and Campaigns available at this moment.",
	license="LGPLv3",
	keywords="mailgun api wrapper",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
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
