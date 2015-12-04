import sys, detector, convert

if __name__ == '__main__':
    if len(sys.argv) == 3:
        faces = detector.FaceDetection.find(sys.argv[1], sys.argv[2])
        finds = []
        for (x, y, w, h) in faces:
            finds.append('{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h))
        convert.Json.write_array('faces', finds)
