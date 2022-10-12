# main.py

import os
from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import csv

UPLOAD_FOLDER = './proxy'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

@app.route('/')
def index():
    return render_template("index.html", equation="enter equation here")

@app.route('/', methods = ["POST"])
def action():
    # User enters equation
    if request.form['request_identifier'] == 'enter':
        equation = request.form.get("eq")
        result = eval_helper(equation)
        return render_template("index.html", equation=equation, result=result)
    # User uploads file
    elif request.form['request_identifier'] == 'upload':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file!!')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Illegal file type!!')
            return redirect(request.url)
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload.txt'))
            convert_upload_for_download()
            return render_template("index.html", equation="enter equation here",
                                   show_download=True)

@app.route('/download')
def download_file():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'download.csv')
    return send_file(path, as_attachment=True)

def convert_upload_for_download():
    uploadfile = os.path.join(app.config['UPLOAD_FOLDER'], 'upload.txt')
    downloadfile = os.path.join(app.config['UPLOAD_FOLDER'], 'download.csv')
    with open(uploadfile, 'r') as f:
        data = f.readlines()
    data = [[row, eval_helper(row)] for row in data]
    with open(downloadfile, 'w') as f:
        write = csv.writer(f) 
        write.writerow(['input string', 'result'])
        write.writerows(data)

def eval_helper(s: str) -> str:
    try:
        result = str(eval(s))
    except:
        result = 'N/A'
    return result

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run()
