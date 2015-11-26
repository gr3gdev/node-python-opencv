import sys, cv2, imutils, base64
import numpy as np

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
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
    sys.stdout.flush()
