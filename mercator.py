import math


TILE_SIZE = 256

pixelOrigin_x = TILE_SIZE/2.0
pixelOrigin_y = TILE_SIZE/2.0

pixelsPerLngDegree = TILE_SIZE/360.0
pixelsPerLngRadian = TILE_SIZE/ (2*math.pi)

def latlng_to_world_coordinate(lat, lng):
	w1 = pixelOrigin_x + lng * pixelsPerLngDegree

	siny = math.sin(math.radians(lat))
	w2 = pixelOrigin_y + 0.5 * math.log((1 + siny)/(1 - siny)) * -pixelsPerLngRadian

	return [w1, w2]


def world_coordinate_to_pixel_coordinate(w1, w2, zoom_level):
	return [int(w1 * (2**zoom_level)), int(w2 * (2**zoom_level))]


def pixel_coordinate_to_world_coordinate(x, y, zoom_level):
	return [(x+0.0)/(2**zoom_level), (y+0.0)/(2**zoom_level)]


def world_coordinate_to_latlng(w1, w2):
	lng = (w1 - pixelOrigin_x) / pixelsPerLngDegree

	lat_radian = (w2 - pixelOrigin_y) / -pixelsPerLngRadian
	lat = math.degrees(2 * math.atan(math.exp(lat_radian)) - math.pi/2)

	return [lat, lng]
