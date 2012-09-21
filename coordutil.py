#!/usr/bin/env python2

def _fix_alt(coord, alt):
	c = list(coord)[:]
	if len(c) < 3:
		c.append(alt)
	else:
		c[2] = alt_m
	return c

def _wrap_at_end_of_grid(coord):
	c = list(coord)[:]
	if c[0] > 180: c[0] = 180-c[0]
	elif c[0] < -180: c[0] = -180-c[0]
	if c[1] > 90: c[1] = 90-c[1]
	elif c[1] < -90: c[1] = -90-c[1]
	return c

def fix(coords, alt_m):
	cs = list(coords)[:]
	amended_coords = []
	for c in cs:
		c = _fix_alt(c, alt_m)
		c = _wrap_at_end_of_grid(c)
		amended_coords.append(c)
	return amended_coords
