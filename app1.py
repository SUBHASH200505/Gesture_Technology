import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import threading
from flask import Flask, jsonify, render_template
import subprocess

# Initialize Flask app
app = Flask(__name__)

# Flask Routes
@app.route('/')
def index():
    return render_template('success3.html')

@app.route('/media_control')
def media_control():
    try:
        subprocess.Popen(['python', 'media_control.py'])
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/mouse_control')
def mouse_control():
    try:
        subprocess.Popen(['python', 'mouse_control.py'])
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/ppt_control')
def ppt_control():
    try:
        subprocess.Popen(['python', 'ppt_control.py'])
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/sound_control')
def sound_control():
    try:
        subprocess.Popen(['python', 'sound_control.py'])
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# New Game Control Route
@app.route('/game_control')
def game_control():
    try:
        subprocess.Popen(['python', 'game_control.py'])  # Call a game control script
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

# Start the Flask app in a separate thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, use_reloader=False)
