# -*- coding: utf-8 -*-

import sys
sys.path.append('../mensapagescraper')

import mensapagescraper

import json

main =  mensapagescraper.getMensaInfo()[u'2017-09-13']

print(main[u'veg_menu'])

#print(mensapagescraper.getMensaInfo()[u'2017-09-13'][u'veg_menu'])
#print(mensapagescraper.getMensaInfo()[u'2017-09-13'][u'mensa_vit'])