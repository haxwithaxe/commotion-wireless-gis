#!/usr/bin/env python2

from shapely.geometry import *

class Geo(object):
	def __init__(self, lat=None, lon=None ,alt_m=0.0):
		self.lat1_m = 111015.45481323975
		self.lon1_m = None
		self.datum = 'wgs84'
		self.d_unit = 'm'
		self.E_radius = None

	@property
	def m1_lat(self):
		return 1/self.lat1_m

	def m1_lon(self, lon):
		return None

