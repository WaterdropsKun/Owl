# Taken From https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited 
from flask import Flask, render_template, Response
from multiprocessing import Process

from camera_opencv import CameraOpenCV
from camera_opencv import inputQueue
from camera_opencv import outputQueue
from camera_opencv import Queue_frame


app = Flask(__name__)

@app.route('/')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(CameraOpenCV()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    # construct a child process *indepedent* from our main process of
    # execution
    print("[INFO] starting process...")
    p = Process(target=Queue_frame, args=(inputQueue, outputQueue))
    p.daemon = True
    p.start()

    app.run(host='0.0.0.0', threaded=True)



