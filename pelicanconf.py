#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Sipmann'
AUTHOR_IMAGE = 'https://s.gravatar.com/avatar/7f717d69fb6d3dbc5490d47369aca3e0?s=180'
SITENAME = 'Sipmann'
SITEURL = 'https://www.sipmann.com'

PATH = './content'
STATIC_PATHS = ['images']

TIMEZONE = 'America/Sao_Paulo'

THEME = 'theme'

DEFAULT_LANG = 'en'
DEFAULT_IMAGE = 'images/sipmann.com.png'

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

#GOOGLE_ADS_CLIENT = "ca-pub-3097623931513783"
GOOGLE_ANALYTICS = 'UA-8072083-2'
TWITTER_USERNAME  = 'msipmann'
AVATAR = 'https://secure.gravatar.com/avatar/7f717d69fb6d3dbc5490d47369aca3e0';

# Blogroll
LINKS = (('Eduardo AW', 'https://eduardoaw.github.io/') , 
	('Grepora', 'https://www.grepora.com'),
	('PythonClub', 'http://pythonclub.com.br/'))

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/MSipmann'),
		('Github', 'https://github.com/sipmann'),
		('Linkedin', 'http://br.linkedin.com/in/sipmann'))

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['plugins']

PLUGINS = [
	'related_posts',
	'sitemap',
	'gzip_cache',
	'series'
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

COIL_TOKEN='$coil.xrptipbot.com/uH6DA7YAQ7y0_IvXt4p0VQ'


#js -- monokai
#xml -- 3024
#sql -- hopscotch
