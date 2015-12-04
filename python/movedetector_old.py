import sys, detector, convert

if __name__ == '__main__':
    #if len(sys.argv) == 3:
    #(x, y, w, h) = detector.MoveDetection.find(sys.argv[1], sys.argv[2])
    #convert.Json.write('{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h))
    if len(sys.argv) == 2:
        json = sys.argv[1]
        (x, y, w, h) = detector.MoveDetection.find(json)
        convert.Json.write('{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h))
