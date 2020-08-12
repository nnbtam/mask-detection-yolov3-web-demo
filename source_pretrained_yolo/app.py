import base64
import os

import cv2
from flask import Flask, render_template, request, url_for, redirect


from yolov3.detect import infer_image, load_model

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
app.config.update(
    ENV='development',
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
)

 # LOAD YOLO MODEL ONCE
yolo, classes, colors, output_layers = load_model()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # request the user to upload a file
    image = request.files["file"]
    
        # Create directory to store uploaded image
    upload_dir = "/".join([app.config['UPLOAD_FOLDER'], 'uploads'])
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)

    # Save uploaded image to local storage
    filename = image.filename
    upload_dir = "/".join([upload_dir, filename])
    image.save(upload_dir)

    output_filename, file_extension = os.path.splitext(filename)
    output_filename = output_filename + '_detected' + file_extension

    output_dir = "/".join([app.config['UPLOAD_FOLDER'], 'detected'])
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Save processed image to local storage
    output_dir = "/".join([output_dir, output_filename])


    # Object detection API
    infer_image(upload_dir, output_dir, yolo, classes, colors, output_layers)

    return render_template("upload.html", upload_img=filename, output_img=output_filename)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)