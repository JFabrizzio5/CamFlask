from flask import Flask, render_template, Response
import cv2
import numpy as np
import mss

app = Flask(__name__)

# Función para capturar el escritorio y generar los frames
def generate_frames():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        while True:
            frame = np.array(sct.grab(monitor))
            ret, buffer = cv2.imencode('.jpg', frame)

            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
