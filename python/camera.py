import cv2, base64, imutils
import numpy as np

class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.frame = None
        self.actif = False

    def __del__(self):
        self.video.release()

    def read(self):
        # Lecture image de la webcam
        if self.video.isOpened():
            self.actif = True
            success, frame = self.video.read()
        else:
            frame = np.zeros((500, 500), dtype=np.uint8)
            cv2.putText(frame, 'Camera(s) OFF', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        self.frame = imutils.resize(frame, width = 500)

    def get_frame(self):
        # Image de la webcam
        return self.frame, self.actif

    def get_frame_base64(self):
        # Encodage de l'image
        ret, image = cv2.imencode('.jpg', self.frame)
        # Conversion en Base64
        b64 = base64.encodestring(image)
        return 'data:image/png;base64,%s' % b64
