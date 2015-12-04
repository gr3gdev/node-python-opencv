import socket, sys, detector

class DetectFace(object):
    def __init__(self):
        self.image = None
        self.haar = None

if __name__ == '__main__':
    if len(sys.argv) == 2:
        mode = None
        TCP_IP = '127.0.0.1'
        TCP_PORT = int(sys.argv[1])
        BUFFER_SIZE = 16
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()
        while 1:
            data = conn.recv(BUFFER_SIZE)
            try:
                if data == 'STOP':
                    break
                if data == 'INIT':
                    mode = DetectFace()
                    conn.send('INITIALIZED')
                elif data == 'EXECUTE':
                    faces = detector.FaceDetection.find(mode.image, mode.haar)
                    finds = '{"faces": ['
                    index = 0
                    for (x, y, w, h) in faces:
                        index += 1
                        finds += '{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h)
                        if index < len(faces):
                            finds += ','
                    finds += ']}'
                    conn.send('%s' % finds)
                elif data is not None:
                    if data.startswith('BUF1'):
                        BUFFER_SIZE = int(data[5:])
                        conn.send('BUFFER1 RECEIVED');
                    if data.startswith('BUF2'):
                        BUFFER_SIZE = int(data[5:])
                        conn.send('BUFFER2 RECEIVED');
                    if data.startswith('IMG1'):
                        mode.image = data[5:]
                        conn.send('IMAGE1 RECEIVED');
                    if data.startswith('PTH1'):
                        mode.haar = data[5:]
                        conn.send('PATH1 RECEIVED');
            except:
                conn.send('- ERROR %s : %s' % (sys.exc_info()[0], sys.exc_info()[1]))
        conn.close()
