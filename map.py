

import data
import net
import ap
import osm


class Map(object):
	def __init__(self, ap_data, title, osm_uid, osm_user, osm_email, coverage_color=('08','03','00','08'), extent=(0.0, 0.0, 0.0, 0.0)):
		self.data = ap_data
		self.title = title
		self.output_filename = 'output-%s.osm' % self.title
		self.color = coverage_color
		self.ap_list = []
		self.osm = osm.OSM(osm_uid, osm_user, osm_email)
		self.net = None
	def get_network(self):
		for item in self.data:
			if 'latitude' in item:
				lat = float(item['latitude'])
			else:
				continue
			if 'longitude' in item:
				lon = float(item['longitude'])
			else:
				continue
			if 'altitude' in item:
				alt = float(item['altitude'])
			else:
				alt = 10.0
			if 'radius' in item:
				rad = int(item['radius'],10)
			else:
				rad = 100
			self.ap_list.append(ap.AP(lat, lon, alt, rad))
			self.ap_list[-1].get_cover()
		self.net = net.Network(self.ap_list)

	def to_xml(self):
		self.net.get_intersecting()
		self.net.get_cover()
		for g in self.net.coords:
			self.osm.polygon(g, tags=[])
		self.osm.to_xml(self.output_filename)

if __name__ == '__main__':
	ap_data = data.read('example.csv')
	map_obj = Map(ap_data, 'example', '0', 'user', 'user@example.com')
	map_obj.get_network()
	map_obj.to_xml()
