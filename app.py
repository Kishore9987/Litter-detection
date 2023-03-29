from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from PIL import Image
from PIL import ImageColor
import re
import os
import urllib.request
from werkzeug.utils import secure_filename
import shutil

UPLOAD_FOLDER = 'static/'

app = Flask(__name__)
app.secret_key = 'background'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', '.mp4', '.mkv', '.avi'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload-image', methods =['GET', 'POST'])
def upimage():
    if request.method=='POST':
        f = request.files['file']
        file_path = UPLOAD_FOLDER+'images/'+f.filename
        f.save(file_path) 
        # Define the path to the image that you want to detect
        image_path = file_path
        # Build the command string with the dynamic image path
        command = 'python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.25 --source "{}"'.format(image_path)
        # Run the command using os.system
        os.system(command)
        demo_dir = "runs/detect"  # Path to the demo folder
        dirs = [os.path.join(demo_dir, d) for d in os.listdir(demo_dir) if os.path.isdir(os.path.join(demo_dir, d))]
        latest_dir = max(dirs, key=os.path.getmtime)
        latest_dir_name = os.path.basename(latest_dir)
        detected_image_path = demo_dir+'/'+latest_dir_name+'/'+f.filename

        exp_dir = "runs/detect/"+latest_dir_name  # Path to the exp folder
        static_dir = "static/images"  # Path to the static/images folder
        old_name = f.filename  # Name of the image file in the exp folder
        new_name = f.filename+'.jpg'  # New name for the image file
        # Construct paths to the old and new image files
        old_path = os.path.join(exp_dir, old_name)
        new_path = os.path.join(static_dir, new_name)
        # Move the image file to the new location and rename it
        shutil.move(old_path, new_path)
        # Delete the exp folder (if it's empty)
        os.rmdir(exp_dir)
        print('Absolute path ',detected_image_path)
        session['image_path'] = 'static/images/'+new_name
    return render_template('upload-image.html')

@app.route('/upload-video', methods =['GET', 'POST'])
def upvideo():
    if request.method=='POST':
        f = request.files['vid']
        file_path = UPLOAD_FOLDER+'videos/'+f.filename
        f.save(file_path) 
        # Define the path to the video that you want to detect
        image_path = file_path
        # Build the command string with the dynamic video path
        command = 'python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.25 --source "{}"'.format(image_path)
        # Run the command using os.system
        os.system(command)
        demo_dir = "runs/detect"  # Path to the demo folder
        dirs = [os.path.join(demo_dir, d) for d in os.listdir(demo_dir) if os.path.isdir(os.path.join(demo_dir, d))]
        latest_dir = max(dirs, key=os.path.getmtime)
        latest_dir_name = os.path.basename(latest_dir)
        detected_image_path = demo_dir+'/'+latest_dir_name+'/'+f.filename

        exp_dir = "runs/detect/"+latest_dir_name  # Path to the exp folder
        static_dir = "static/videos"  # Path to the static/video folder
        old_name = f.filename  # Name of the video file in the exp folder
        new_name = f.filename+'.mp4'  # New name for the video file
        # Construct paths to the old and new video files
        old_path = os.path.join(exp_dir, old_name)
        new_path = os.path.join(static_dir, new_name)
        # Move the video file to the new location and rename it
        shutil.move(old_path, new_path)
        # Delete the exp folder (if it's empty)
        os.rmdir(exp_dir)
        print('Absolute path ',detected_image_path)
        session['video_path'] = 'static/videos/'+new_name
    return render_template('upload-video.html')

@app.route('/use-webcam')
def webc():
    command = 'python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.25 --source 0'
    os.system(command)
    return redirect(url_for('index'))