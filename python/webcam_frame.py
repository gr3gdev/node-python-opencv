import sys, cv2, imutils, base64, threading
import numpy as np

class webcamThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def run(self):
        frame(self.video)

def frame(video):
    while True:
        if video.isOpened():
            success, frame = video.read()
        else:
            frame = np.zeros((500, 500), dtype=np.uint8)
            cv2.putText(frame, 'Camera(s) OFF', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        frame = imutils.resize(frame, width = 500)
        # Encodage de l'image
        ret, image = cv2.imencode('.jpg', frame)
        # Conversion en Base64
        b64 = base64.encodestring(image)
        print 'data:image/png;base64,%s' % b64

if __name__ == '__main__':
    thread = webcamThread(1, 'Webcam')
    thread.start()
    sys.stdout.flush()
