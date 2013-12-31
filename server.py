import os
import json
import copy
import time

from flask import (Flask, request, render_template)

from persistent_store import RedisStore
from coordinate_finder import (get_coordinates, add_pixel_to_latlng)


WEB_SERVER = "http://127.0.0.1:5000/"

app = Flask(__name__)
app.config['WEB_SERVER'] = WEB_SERVER
app.config['RESULT_FOLDER'] = "results"
app.config['CSV_UPLOAD_SERVER'] = WEB_SERVER + "upload/"
app.config['OUTPUT_FILE_NAME'] = "addresses.csv"
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['IMAGE_FOLDER'] = "images"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/kickstart', methods=['POST'])
def kickstart():
    if request.method == 'POST':
        # Extract necessary information from the request
        has_coordinates = request.form['has_coordinates']
        zoom_level = request.form['zoom_level']
        image_resolution = [600, 600]

        if has_coordinates == 'true':
            sw, ne = request.form['sw'], request.form['ne']
            sw = [float(each) for each in sw.split(',')]
            ne = [float(each) for each in ne.split(',')]

            # Assign information to respective variables. Make a copy of latitude
            # (lat) for the sake of the while loop ahead
            lat, lng = sw[0], sw[1]
            max_lat, max_lng = ne[0], ne[1]
            centers = []
            initial_lat = copy.copy(lat)

            # We find out the centers of all the static images to be obtained.
            while lng < max_lng:
                lat = initial_lat
                while lat < max_lat:
                    centers.append([lat, lng])
                    lat = add_pixel_to_latlng(float(lat), float(lng), 0,
                        -image_resolution[0], zoom_level)[0]
                lng = add_pixel_to_latlng(float(lat), float(lng),
                        image_resolution[1], 0, zoom_level)[1]

            print "No of tiles: ", len(centers)
            storage = RedisStore()
            storage.store_centers(centers)
        return download_and_extract_coordinates(zoom_level, image_resolution)


def download_and_extract_coordinates(zoom_level, image_resolution):
    storage = RedisStore()
    center = storage.get_center()
    coordinates = []

    while center:
        center = [float(each) for each in center.split(',')]
        input_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'map{}_{}.jpg'.format(center[0], center[1]))
        output_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'result{}_{}.jpg'.format(center[0], center[1]))
        time.sleep(2)
        coordinate = get_coordinates(float(center[0]), float(center[1]),
            zoom_level, image_resolution, input_file_path, output_file_path)
        coordinates += coordinate
        storage.store_coordinate(coordinate)
        center = storage.get_center()

    coordinate_count = len(coordinates)
    print "No of coordinates: ", coordinate_count
    return str(coordinate_count)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         if uploaded_file:
#             filename = secure_filename(uploaded_file.filename)
#             uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],
#                                             filename))
#             error_msg = ""
#             try:
#                 storage = PersistentStore()
#                 with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
#                     csv_data = f.read().split('\n')
#                     list_of_data = []
#                 for coordinate in csv_data:
#                     list_of_data.append(dict(coordinate = coordinate.split(','),
#                         address=None))
#                 response = storage.store(db_name="addresses",
#                     list_of_data=list_of_data)
#             except (OSError, IOError):
#                 error_msg = "Error occured while uploading the file. Try again"
#                 return render_template('upload_error.html', ERROR_MSG=error_msg)
#             return render_template('postupload.html') #, COORDINATES=json_data)
#     return render_template('upload.html', WEB_SERVER=app.config['CSV_UPLOAD_SERVER'])


@app.route('/data', methods=['POST'])
def accept_data():
    if request.method == 'POST':
        address = json.loads(request.data)
        coordinate = json.loads(request.data)['coordinate']

        with open('addresses.log', 'a') as f:
            f.write(request.data + '\n')
            f.flush()

        storage = RedisStore()
        storage.store_address(coordinate, address)
        return "Success"


@app.route('/coordinate', methods=['GET'])
def vend_coordinates():
    storage = RedisStore()
    result = storage.get_coordinate()
    time.sleep(3)
    print "Vending coordinate {} to client".format(result)
    if result is not None:
        return str(result)
    return "null" 


if __name__ == '__main__':
    app.debug = True
    app.run()
