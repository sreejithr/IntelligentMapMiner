
import os
import json
from flask import Flask, request, render_template
from werkzeug import secure_filename

app = Flask(__name__)
app.config['WEB_SERVER'] = "http://127.0.0.1:5000/"
app.config['RESULT_FOLDER'] = "results"
app.config['OUTPUT_FILE_NAME'] = "addresses.csv"
app.config['UPLOAD_FOLDER'] = "../uploads"


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
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('postupload.html')
    return render_template('upload.html', WEB_SERVER=app.config['WEB_SERVER'])

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
