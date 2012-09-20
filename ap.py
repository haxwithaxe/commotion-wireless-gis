#!/usr/bin/env python2

import geo
from shapely.geometry import *

class AP(object):
	def __init__(self, lat, lon ,alt_m=0.0, radius_m=100):
		self.lat = lat
		self.lon = lon
		self.alt_m = alt_m
		self.poly = None
		self.radius = radius_m*geo.m1_lat
		self.cover_points = []

	def get_cover(self, radius_m=None):
		if not radius_m: radius = self.radius
		else: radius = radius_m*geo.m1_lat
		p = Point(self.lat,self.lon,self.alt_m)
		self.poly = p.buffer(radius)
		c = self.poly.exterior.coords
		self.cover_points = self._fix_coords(c)
	
	def _fix_coords(self, coords):
		for c in coords:
			c[2] = self.alt_m
			if c[0] > 180: c[0] = 180-c[0]
			elif c[0] < -180: c[0] = -180-c[0]
			if c[1] > 90: c[1] = 90-c[1]
			elif c[1] < -90: c[1] = -90-c[1]
		return coords
