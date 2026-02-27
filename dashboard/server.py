from flask import Flask, Response
import threading
import cv2
import numpy as np

app = Flask(__name__)

def generate_frames():
    while True:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "Simulated Frame", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def start_server(generate_frames, port=5000):
    @app.route('/')
    def video_feed():
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port,
                                            debug=False, use_reloader=False)).start()

if __name__ == "__main__":
    start_server(generate_frames)
    print("Server started at http://127.0.0.1:5000/")
    # Keep the main thread alive
    threading.Event().wait()