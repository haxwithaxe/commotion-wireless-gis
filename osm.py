#!/usr/bin/env python2

import random
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
		self.doc = etree.Element('osm')
		self.timestamp_fmt = '%Y-%m-%dT%H:%M:%SZ'
		self.changeset = '0'
		self.id_len = 10
		self.elems = []
		self.feature_ids = []
		self.signal_coverage_dict = SCDICT

	def signal_coverage_tags(self):
		tags = []
		for k,v in self.signal_coverage_dict.items():
			tags += {'k': 'signal-coverage-%s' % k, 'v':v}
		return tags

	@property
	def uniq_iq(self):
		id_num = _rand_uniq_id(self.id_len, self.feature_ids)
		self.feature_ids += id_num
		return id_num

	def to_xml(self, filename):
		osm_attrib, bounds = self.xml_head()
		self.doc.attrib = osm_attrib
		self.doc.append(bounds)
		for e in self.elems:
			self.doc.append(e)
			print(e)
		etree.ElementTree(self.doc).write(filename, encoding='utf-8', xml_declaration=True, method='xml')

	def polygon(self, coords, **kwargs):
		poly = []
		point0 = None
		way = etree.Element('way',
				{'id':self.uniq_id,
				'user':self.user,
				'uid':self.uid,
				'visible':True,
				'version':'0', #version,
				'changeset':self.changeset,
				'timestamp':self.timestamp
				}
			)
		kwargs['tags'] += {'k':'area','v':'yes'}
		kwargs['tags'] += self.signal_coverage_tags()
		for tag in kwargs['tags']:
			way.append(self.tag(tag))
		for p in coords:
			args = copy.deepcopy(kwargs)
			args['tags'] = []
			point = self.point(p, kwargs)
			way.append(self.ref(point))
			poly += point
			if coords.index(p) == 0: point0 = point
		if point0: way.append(self.ref(point0))
		poly += way
		self.elems += poly
		return poly

	def point(self, coords, **kwargs):
		point = etree.Element('node',
				{'id':self.uniq_id,
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
		args['tags'] += {'k':'altitude', 'v': str(coords[2])}
		for tag in args['tags']:
			point.append(self.tag(tag))
		if 'add' in kwargs and kwargs['add']: self.elems += point
		return point

	def tag(self, tag={'k':'','v':''}):
		return etree.Element('tag', tag)

	def ref(self, point):
		id_num = point.get('id')
		ref = etree.Element('nd', {'ref':id_num})
		return ref

	def xml_head(self):
		bounds = etree.Element('bounds')
		bounds.attrib = {'minlat':'0', 'maxlat':'0', 'minlon':'0', 'maxlon':'0'}
		osm_attrib = {'version':OSM_API_VERSION, 'generator':GENERATOR}
		return osm_attrib, bounds
