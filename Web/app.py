from flask import Flask, render_template, Response, url_for
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', videourl=url_for('video_feed'))

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    cap = cv2.VideoCapture(0)
    cap.set(3, 600)
    cap.set(4, 480)
    cap.set(5, 40)

    while True:
        ret, img = cap.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', img)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
