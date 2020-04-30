import os
from flask import Flask, request, send_from_directory
from gen_slack_theme import generate_slack_theme
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)
CORS(app, resources={
     r"*": {"origins": ["https://slackable-themes.com, https://slackablethemes.com"]}})


@app.route("/")
def hello():
    return "Try /default"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route("/default")
def get_default():
    return "#3F0E40,#350d36,#1164A3,#FFFFFF,#350D36,#FFFFFF,#2BAC76,#CD2553"


@app.route("/create-theme", methods=['POST'])
@cross_origin()
def create_theme():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        theme = generate_slack_theme(file)
        return theme
    return "Shit happened"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
