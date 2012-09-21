#!/usr/bin/env python2

import coordutil
from geo import Geo
from shapely.geometry import *

geo = Geo()

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
		self.cover_points = coordutil.fix(c, self.alt_m)
