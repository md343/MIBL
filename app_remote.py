import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template, Response, jsonify, render_template_string
from waitress import serve
from pathlib import Path
import socket
from src.retrieval import RetRemote
import cv2

app = Flask(__name__)
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/img_retrieval', methods=['POST'])
def img_retrieval():

    retriever.localise()

    return render_template("index.html")

def loop():
    try:
        while True:
            ret, frame = retriever.camera.read()

            if retriever.isAgilityCar:
                width = frame.shape[1]
                frame = frame[:,:width//2]

            frame = retriever.join_map(frame)

            ret, jpeg = cv2.imencode('.jpg', frame)
            if jpeg is not None:
                yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            else:
                print("frame is none")
    except KeyboardInterrupt:
        print("User interrupted!")

    finally:
        retriever.terminate()

@app.route('/video_feed')
def video_feed():
    return Response(loop(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print("Initialising Retrieval")
    retriever = RetRemote()
    print("Initiating Server")
    print("Server Host: "+IPAddr+":5000")
    try:
        serve(app, host=IPAddr, port=5000, threads=2)
    except KeyboardInterrupt:
        print('Stopping server...')


#<!img src="{{url_for('static', filename='maps/' + '.jpg')}}" alt="MAP_TEST">
