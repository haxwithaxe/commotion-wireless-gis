#!/usr/bin/env python2

import copy
import random
import time
import xml.etree.ElementTree as etree
import wifiinfo

MESH = False
OSM_API_VERSION = '0.6'
GENERATOR = 'commotion-gis'
WIFI_AP_CHANNEL_Hz = str(wifiinfo.channel_Hz(11))
WIFIMODE = '802.11g'
SCDICT = {'quality': 'idealized', 'frequency-median-Hz':WIFI_AP_CHANNEL_Hz, 'protocol-osi-2':'802.11%s' % WIFIMODE}
if MESH: SDICT.update({'protocol-osi-3':'OLSR'})

def _random_uniq_id(id_len, used_ids):
	id_num = str(random.randint(0,(10**id_len)-1))
	if id_num in used_ids: id_num = _random_uniq_id(id_len, used_ids)
	return id_num

class OSM(object):
	def __init__(self, uid, user, email):
		self.uid = uid
		self.user = user
		self.email = email
		self.d_unit = 'm'
		self.doc = None
		self.timestamp_fmt = '%Y-%m-%dT%H:%M:%SZ'
		self.timestamp = self._get_timestamp()
		self.changeset = '0'
		self.id_len = 10
		self.feature_ids = []
		self.signal_coverage_dict = SCDICT
		self._xml_init()
	
	def _get_timestamp(self):
		return time.strftime(self.timestamp_fmt)

	def signal_coverage_tags(self):
		tags = []
		for k,v in self.signal_coverage_dict.items():
			tags.append({'k': 'signal-coverage-%s' % k, 'v':v})
		return tags

	def uniq_id(self):
		id_num = _random_uniq_id(self.id_len, self.feature_ids)
		self.feature_ids.append(id_num)
		return id_num

	def to_xml(self, filename, encoding='utf-8'):
		print(self.doc)
		for c in self.doc:
			print(c.tag, c.attrib)
		etree.ElementTree(self.doc).write(filename, encoding=encoding, xml_declaration=True, method='xml')

	def polygon(self, coords, **kwargs):
		point0 = None
		way = etree.SubElement(self.doc, 'way')
		way.attrib = {'id':self.uniq_id(),
				'user':self.user,
				'uid':self.uid,
				'visible':'true',
				'version':'0', #version,
				'changeset':self.changeset,
				'timestamp':self.timestamp
				}
		kwargs['tags'].append({'k':'area','v':'yes'})
		kwargs['tags'] += self.signal_coverage_tags()
		for tag in kwargs['tags']:
			self.tag(way, tag)
		for p in coords:
			args = copy.deepcopy(kwargs)
			args['tags'] = []
			point = self.point(p, **args)
			self.ref(way, point)
			if coords.index(p) == 0: point0 = point
		if len(point0):
			self.ref(way, point0)

	def point(self, coords, **kwargs):
		point = etree.SubElement(self.doc, 'node',
				{'id':self.uniq_id(),
				'lat':str(coords[0]),
				'lon':str(coords[1]),
				'user':self.user,
				'uid':str(self.uid),
				'visible':'true',
				'version':'0', #version,
				'changeset':self.changeset,
				'timestamp':self.timestamp
				}
			)
		args = copy.deepcopy(kwargs)
		args['tags'].append({'k':'altitude', 'v': str(coords[2])})
		for tag in args['tags']:
			self.tag(point, tag)
		return point

	def tag(self, parent, tag):
		etree.SubElement(parent, 'tag', tag)

	def ref(self, parent, point):
		id_num = point.get('id')
		etree.SubElement(parent,'nd', {'ref':id_num})

	def _xml_init(self):
		self.doc = etree.Element('osm')
		bounds = etree.SubElement(self.doc, 'bounds')
		bounds.attrib = {'minlat':'0', 'maxlat':'0', 'minlon':'0', 'maxlon':'0'}
		self.doc.attrib = {'version':OSM_API_VERSION, 'generator':GENERATOR}
