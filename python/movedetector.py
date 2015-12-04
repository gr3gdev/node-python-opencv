import socket, sys, detector

class DetectMove(object):
    def __init__(self):
        self.image1 = None
        self.image2 = None

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
                    mode = DetectMove()
                    conn.send('INITIALIZED')
                elif data == 'EXECUTE':
                    (x, y, w, h) = detector.MoveDetection.find(mode.image1, mode.image2)
                    conn.send('{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h))
                elif data is not None:
                    if data.startswith('BUF1'):
                        BUFFER_SIZE = int(data[5:])
                        conn.send('BUFFER1 RECEIVED');
                    if data.startswith('BUF2'):
                        BUFFER_SIZE = int(data[5:])
                        conn.send('BUFFER2 RECEIVED');
                    if data.startswith('IMG1'):
                        mode.image1 = data[5:]
                        conn.send('IMAGE1 RECEIVED');
                    if data.startswith('IMG2'):
                        mode.image2 = data[5:]
                        conn.send('IMAGE2 RECEIVED');
            except:
                conn.send('{"ERROR": "%s : %s"}' % (sys.exc_info()[0], sys.exc_info()[1]))
        conn.close()
