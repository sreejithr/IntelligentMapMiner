import os
import json

from flask import (Flask, request, render_template, url_for, redirect)
from werkzeug import secure_filename

from persistent_store import PersistentStore
from coordinate_finder import get_coordinates


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
        input_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'map{}.jpg'.format(latlng.split(',')[0]))
        output_file_path =\
            os.path.join('/Users/sreejith/MQuotient/maps/google_miner/images',
                'result{}.jpg'.format(latlng.split(',')[0]))
        image_resolution = [600, 600]

        print get_coordinates(float(lat), float(lng), zoom_level,
            image_resolution, input_file_path, output_file_path)

    return "Success"


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
            error_msg = ""
            try:
                storage = PersistentStore()
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                    csv_data = f.read().split('\n')
                    list_of_data = []
                for coordinate in csv_data:
                    list_of_data.append(dict(coordinate = coordinate.split(','),
                        address=None))
                response = storage.store(db_name="addresses",
                    list_of_data=list_of_data)
            except (OSError, IOError):
                error_msg = "Error occured while uploading the file. Try again"
                return render_template('upload_error.html', ERROR_MSG=error_msg)
            return render_template('postupload.html') #, COORDINATES=json_data)
    return render_template('upload.html', WEB_SERVER=app.config['CSV_UPLOAD_SERVER'])


@app.route('/data', methods=['POST'])
def accept_data():
    if request.method == 'POST':
        with open(os.path.join(app.config['RESULT_FOLDER'],
            app.config['OUTPUT_FILE_NAME']), 'a') as f:
            data = json.loads(request.data)
            to_save = save_to_file(data['address_components'])
            f.write(to_save + '\n')
            f.flush()
        return "hey"





if __name__ == '__main__':
    app.debug = True
    app.run()
