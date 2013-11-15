import os
import json
from flask import Flask, request, render_template, url_for, redirect
from werkzeug import secure_filename

WEB_SERVER = "http://127.0.0.1:5000/"

app = Flask(__name__)
app.config['WEB_SERVER'] = WEB_SERVER
app.config['RESULT_FOLDER'] = "results"
app.config['CSV_UPLOAD_SERVER'] = WEB_SERVER + "upload/"
app.config['OUTPUT_FILE_NAME'] = "addresses.csv"
app.config['UPLOAD_FOLDER'] = "uploads"


def process_data(address_data):
    final = {}
    keys = ["street_number", "route", "neighborhood", "sublocality",
    "administrative_area_level_2", "administrative_area_level_1", "country",
    "postal_code"]
    with open('log.log', 'a') as f:
        f.write(str(address_data)  + '\n')

    for component in address_data:
        try:
            final[component['types'][0]] = component['long_name']
        except IndexError:
            print component['types']

    result = ''
    for key in keys:
        try:
            result += final[key]+','
        except KeyError:
            result += ','
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('upload'))


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
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                    csv_data = f.read().split('\n')
                    json_data = {'data': []}
                for coordinate in csv_data:
                    json_data['data'].append(coordinate.split(','))
                try:
                    json_data = json.dumps(json_data)
                except:
                    error_msg = "Check if the file is of CSV type"
                    return render_template('upload_error.html', ERROR_MSG=error_msg)
            except (OSError, IOError):
                error_msg = "Error occured while uploading the file. Try again"
                return render_template('upload_error.html', ERROR_MSG=error_msg)
            return render_template('postupload.html', COORDINATES=json_data)
    return render_template('upload.html', WEB_SERVER=app.config['CSV_UPLOAD_SERVER'])


@app.route('/data', methods=['POST'])
def accept_data():
    if request.method == 'POST':
        with open(os.path.join(app.config['RESULT_FOLDER'],
            app.config['OUTPUT_FILE_NAME']), 'a') as f:
            data = json.loads(request.data)
            to_save = process_data(data['address_components'])
            f.write(to_save + '\n')
            f.flush()
        return "hey"

if __name__ == '__main__':
    app.debug = True
    app.run()
