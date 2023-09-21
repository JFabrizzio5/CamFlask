from flask import Flask, render_template, Response, request
import cv2
import threading
import uuid

app = Flask(__name__)

# Diccionario para llevar un seguimiento de las cámaras por usuario
user_cameras = {}

# Función para generar fotogramas de la cámara de un usuario específico
def generate_frames(user_id):
    while True:
        if user_id in user_cameras:
            cap = user_cameras[user_id]
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    break
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Genera un ID único para el usuario actual
    user_id = str(uuid.uuid4())
    return render_template('index.html', user_id=user_id)

@app.route('/video_feed/<user_id>')
def video_feed(user_id):
    return Response(generate_frames(user_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    user_id = request.form.get('user_id')
    if user_id:
        cap = cv2.VideoCapture(0)  # Inicializa la cámara para el usuario
        user_cameras[user_id] = cap
    return render_template('index.html', user_id=user_id)

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    user_id = request.form.get('user_id')
    if user_id in user_cameras:
        cap = user_cameras[user_id]
        cap.release()  # Libera la cámara
        del user_cameras[user_id]  # Elimina la cámara del diccionario
    return render_template('index.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
