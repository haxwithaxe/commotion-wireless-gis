#!/usr/bin/env python2

import geo
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
			groups += [[ap]]
			for target in self.ap_list:
				if target != ap and ap.poly.intersects(target):
					groups[index] += target
			index += 1
		ugroups = []
		print(groups)
		for g in groups:
			for p in groups:
				if _lsort(g) == _lsort(p) and p not in ugroups:
					ugroups += p
		print(ugroups)
		self.ap_groups = ugroups

	def get_cover(self, union=False):
		if union:
			for g in self.ap_groups:
				polygons = []
				for ap in g:
					polygons += ap.poly
				self.polys += cascaded_union(ploygons)
		else:
			for ap in self.ap_list:
				self.polys += ap.poly
		for poly in self.polys:
			print(poly)
			self.coords += [poly.exterior.coords]

	
