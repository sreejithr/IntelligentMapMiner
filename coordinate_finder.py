import requests

import mercator
from map_extract_tool.map_extract import OpenCVMapAnalyzer


class GETException(Exception):
	def __init__(self, message):
		self.message = message
		super.__init__(self)

def map_analyzer_pixel_to_map_pixel(center_pixel_x, center_pixel_y,
	pixel_coordinate, image_resolution):
	"""
	Converts pixel coordinates to latlng coordinates
	"""
	return [center_pixel_x + (pixel_coordinate[0] - image_resolution[0]/2),
		center_pixel_y + (pixel_coordinate[1] - image_resolution[0]/2)]


def get_coordinates(center_lat, center_lng, zoom_level, image_resolution,
	input_file_path, output_file_path):
	"""
	Extracts coordinates from map image using the OpenCV module
	"""
	import ipdb; ipdb.set_trace()
	get_static_map_image([center_lat, center_lng], zoom_level, image_resolution,
		input_file_path)

	map_analyzer = OpenCVMapAnalyzer()
	pixels =  map_analyzer.extract_points(str(input_file_path),
		str(output_file_path))

	# We pair pixels by twos and make a list of pixel coordinates
	pixels_rev = pixels[::-1]
	pixel_coordinates = []
	while len(pixels)!=0:
		try:
			pixel_coordinates.append([pixels_rev.pop(), pixels_rev.pop()])
		except IndexError:
			break

	w1, w2 = mercator.latlng_to_world_coordinate(center_lat, center_lng)
	x, y = mercator.world_coordinate_to_pixel_coordinate(w1, w2, zoom_level)

	coordinates = []
	for pixel_coordinate in pixel_coordinates:
		new_x, new_y = map_analyzer_pixel_to_map_pixel(x, y, pixel_coordinate,
			image_resolution)
		w1, w2 = mercator.pixel_coordinate_to_world_coordinate(new_x, new_y,
			zoom_level)
		coordinates.append(mercator.world_coordinate_to_latlng(w1, w2))

	return coordinates


def get_static_map_image(latlng, zoom_level, image_resolution, input_filename):
	latlng = [str(each) for each in latlng]
	image_resolution = [str(each) for each in image_resolution]
	url = 'http://maps.googleapis.com/maps/api/staticmap?center={}&zoom={}&size={}&sensor=false'.format(
		','.join(latlng), zoom_level, 'x'.join(image_resolution))

	try:
		response = requests.get(url)
	except requests.exceptions.ConnectionError:
		raise GETException("Problem connecting with Static Image API")
	except requests.exceptions.HTTPError:
		raise GETException("Received invalid HTTP response from Static Image API")

	with open(input_filename, 'w') as f:
		f.write(response.content)
		f.flush()
