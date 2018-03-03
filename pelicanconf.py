#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Sipmann'
SITENAME = 'Sipmann'
SITEURL = 'https://www.sipmann.com'

PATH = './content'
STATIC_PATHS = ['images']

TIMEZONE = 'America/Sao_Paulo'

THEME = 'theme'

DEFAULT_LANG = 'pt'
DEFAULT_IMAGE = 'images/sipmann.com.png'

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

#GOOGLE_ADS_CLIENT = "ca-pub-3097623931513783"
GOOGLE_ANALYTICS = 'UA-8072083-2'
TWITTER_USERNAME  = 'msipmann'
AVATAR = 'https://secure.gravatar.com/avatar/7f717d69fb6d3dbc5490d47369aca3e0';

# Blogroll
LINKS = (('PythonClub', 'http://pythonclub.com.br/'), ('Eduardo AW', 'https://eduardoaw.github.io/'))

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/MSipmann'),
		('Github', 'https://github.com/sipmann'),
		('Linkedin', 'http://br.linkedin.com/in/sipmann'))

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['plugins']

PLUGINS = [
	'related_posts',
	'sitemap',
	'gzip_cache'
]

ADDTHIS_PROFILE = 'ra-53d5af0d0caa9bff'

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.4,
        'pages': 0.4
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

DISQUS_SITENAME = 'sipmann'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
