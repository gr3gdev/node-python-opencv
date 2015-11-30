import cv2, imutils, base64, socket
import numpy as np

TCP_IP = '127.0.0.1'
TCP_PORT = 4004

video = cv2.VideoCapture(0)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
while True:
    if video.isOpened():
        success, frame = video.read()
    else:
        frame = np.zeros((500, 500), dtype=np.uint8)
        cv2.putText(frame, 'Camera(s) OFF', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    frame = imutils.resize(frame, width = 500)
    #cv2.imwrite('out.png', frame)
    # Encodage de l'image
    ret, image = cv2.imencode('.jpg', frame)
    # Conversion en Base64
    b64 = base64.encodestring(image)
    conn.sendall('WEBCAMimgPY%s' % b64)
conn.close()
