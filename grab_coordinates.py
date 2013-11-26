import mercator
from opencv.build.map_extract import OpenCVMapAnalyzer

IMAGE_RESOLUTION = [600, 600]


def map_analyzer_pixel_to_map_pixel(center_pixel_x, center_pixel_y, pixel_coordinate):
	"""
	Converts pixel coordinates to latlng coordinates
	"""
	return [center_pixel_x + (pixel_coordinate[0] - IMAGE_RESOLUTION[0]/2),
		center_pixel_y + (pixel_coordinate[1] - IMAGE_RESOLUTION[0]/2)]


def get_coordinates(center_lat, center_lng, zoom_level, input_file_path,
	output_file_path):
	"""
	Extracts coordinates from map image using the OpenCV module
	"""
	map_analyzer = OpenCVMapAnalyzer()
	pixels =  map_analyzer.extract_points(input_file_path, output_file_path)

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
		new_x, new_y = map_analyzer_pixel_to_map_pixel(x, y, pixel_coordinate)
		w1, w2 = mercator.pixel_coordinate_to_world_coordinate(new_x, new_y,
			zoom_level)
		coordinates.append(mercator.world_coordinate_to_latlng(w1, w2))

	print coordinates

get_coordinates(-15.80165472282688, -47.91369087477404, 15, "/Users/sreejith/Desktop/cape.tiff",
	"/Users/sreejith/Desktop/circles.jpg")