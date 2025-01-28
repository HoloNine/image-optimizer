# filepath: /d:/apps/python/image-optimizer/app.py
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from utils.converter import convert_images_to_webp
from utils.clear_directory import clear_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads'
app.config['DOWNLOAD_FOLDER'] = '../downloads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 16 MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')
    quality = int(request.form.get('quality', 80))

    # clear_directory(app.config['UPLOAD_FOLDER'])
    # clear the downloads directory every time a new file is uploaded
    clear_directory(app.config['DOWNLOAD_FOLDER'])

    for file in files:
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    convert_images_to_webp(app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER'], quality=quality)
    return redirect(url_for('uploaded_files'))

@app.route('/uploads')
def uploaded_files():
    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template('uploads.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
