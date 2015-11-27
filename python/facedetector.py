import cv2, sys

if __name__ == '__main__':
    if len(sys.argv) == 3:
        img = cv2.imread(sys.argv[1])
        haarcascade = sys.argv[2]
        faceCascade = cv2.CascadeClassifier(haarcascade)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = faceCascade.detectMultiScale(gray, 1.2, 8)
        print '{"faces": ['
        index = 0
        for (x, y, w, h) in faces:
            print '{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h)
            index += 1
            if index < len(faces):
                print ','
        print ']}'
    sys.stdout.flush()
