import os

from flask import Flask, request, send_from_directory
from gen_slack_theme import generate_slack_theme

app = Flask(__name__)

@app.route("/")
def hello():
    return "Try /default"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/default")
def get_default():
    return "#3F0E40,#350d36,#1164A3,#FFFFFF,#350D36,#FFFFFF,#2BAC76,#CD2553"

@app.route("/generate", methods=['POST'])
def generate():
    file = request.files['file']
    print(request.files)
    return generate_slack_theme(file)

