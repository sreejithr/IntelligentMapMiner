import os
import json

from flask import (Flask, request, render_template)
from werkzeug import secure_filename

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
    return render_template("index.html") #redirect(url_for('kickstart'))


@app.route('/kickstart', methods=['POST'])
def kickstart():
    if request.method == 'POST':
        latlng = request.form['latlng']
        lat, lng = latlng.split(',')
        zoom_level = request.form['zoom_level']
        image_resolution = [600, 600]

        # sw = []
        # ne = []

        # lat, lng = sw[0], sw[1]
        # max_lat, max_lng = ne[0], ne[1]
        # coordinates = []

        # while lng < max_lng:
        #     while lat < max_lat:
        #         coordinates.append([lat, lng])
        #         lat += add_pixel_to_latlng(float(lat), 0.0, image_resolution[0],
        #                 image_resolution[1], zoom_level)[0]
        #     lng += add_pixel_to_latlng(0.0, float(lng), image_resolution[0],
        #             image_resolution[1], zoom_level)[1]

        input_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'map{}.jpg'.format(latlng.split(',')[0]))
        output_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'result{}.jpg'.format(latlng.split(',')[0]))

        storage = RedisStore()
        storage.store_coordinate(get_coordinates(float(lat), float(lng),
            zoom_level, image_resolution, input_file_path, output_file_path))

    return "Success"


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
        print request.data
        #storage = RedisStore()
        #storage.store_address()
        # with open(os.path.join(app.config['RESULT_FOLDER'],
        #     app.config['OUTPUT_FILE_NAME']), 'a') as f:
        #     data = json.loads(request.data)
        #     to_save = save_to_file(data['address_components'])
        #     f.write(to_save + '\n')
        #     f.flush()
        # return "hey"
    return "hey"

@app.route('/coordinate', methods=['GET'])
def vend_coordinates():
    storage = RedisStore()
    result = storage.get_coordinate()
    print result
    import time
    time.sleep(2)
    if result is not None:
        return str(result)
    return "null" 


if __name__ == '__main__':
    app.debug = True
    app.run()
