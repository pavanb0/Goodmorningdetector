from flask import Flask, render_template, request, url_for
import os
from pathlib import Path
from PIL import Image
import pytesseract
import threading
import shutil


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/assets'
app.config['GOODMORNING'] = 'static/assets/goodmorningimg'

static_folder = Path('static/assets')

with open('goodmorning.txt', 'r') as f:
    lines = f.readlines()

words = [line.strip().lower() for line in lines]

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Files uploaded successfully!'
    return render_template('upload.html')


@app.route('/gallery')
def gallery():
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [url_for('static', filename=f'assets/{filename}') for filename in image_files]

    goodmorning_files = os.listdir(app.config['GOODMORNING'])
    goodmorning_urls = [url_for('static', filename=f'assets/goodmorningimg/{filename}') for filename in goodmorning_files]


    return render_template('gallery.html', image_urls=image_urls, goodmorning_urls=goodmorning_urls)

def have_common_letters(string1, string2):
    common_count = sum(1 for letter in string1 if letter in string2)
    return common_count >= 4

def paste_image(image_path, directory_name):
    
    image_filename = os.path.basename(image_path)    
    destination_path = os.path.join(directory_name, image_filename)    
    os.makedirs(directory_name, exist_ok=True)    
    shutil.copyfile(image_path, destination_path)


def goodmorning():
    imagepaths = [
    os.path.join(static_folder, name)
    for name in os.listdir(static_folder)
    if os.path.isfile(os.path.join(static_folder, name))
    ]
    texts =[]
    for image in imagepaths:
        extract = []
        text = pytesseract.image_to_string(Image.open(image)).lower()
        text = text.replace('\n', ' ')
        extract.append(text)
        has_common = any(have_common_letters(item, element) for item in extract for element in words)
        if has_common:
            texts.append(text)
            paste_image(image, 'static/assets/goodmorningimg')       
    return extract

# print(goodmorning())

if __name__ == '__main__':

    
    app.run(debug=True)
