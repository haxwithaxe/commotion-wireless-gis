#!/usr/bin/env python2

import geo
import coordutil
from shapely.ops import cascaded_union

def _lsort(unsorted_list):
	ul = unsorted_list[:]
	ul.sort()
	return ul

class Network(object):
	def __init__(self, ap_list=[]):
		self.ap_list = ap_list
		self.polys = []
		self.coords = []
		self.ap_groups = []

	def get_intersecting(self):
		groups = []
		index = 0
		for ap in self.ap_list:
			groups.append([ap])
			for target in self.ap_list:
				if target != ap and ap.poly.intersects(target.poly):
					groups[index].append(target)
			index += 1
		ugroups = []
		for g in groups:
			for p in groups:
				if _lsort(g) == _lsort(p) and p not in ugroups:
					ugroups.append(p)
		self.ap_groups = ugroups

	def get_cover(self, union=True):
		if union:
			for g in self.ap_groups:
				polygons = []
				alt_m_sum = 0
				for ap in g:
					alt_m_sum += ap.alt_m
					polygons.append(ap.poly)
				poly = cascaded_union(polygons)
				avg_alt_m = float(alt_m_sum)/(len(g) or 1)
				self.polys.append({'aps':g, 'alt_m':avg_alt_m, 'shape':poly})
		else:
			for ap in self.ap_list:
				self.polys.append({'aps':ap, 'alt_m':ap.alt_m,'shape':ap.poly})
		for poly in self.polys:
			pcoords = poly['shape'].exterior.coords
			print(pcoords[0])
			pcoords = coordutil.fix(pcoords, poly['alt_m'])
			print(pcoords[0])
			self.coords.append(pcoords)

	
