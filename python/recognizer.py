import cv2, os, csv, sys, convert

import numpy as np

from os.path import isfile

if __name__ == '__main__':
    if len(sys.argv) == 4:
        file = open(sys.argv[1], 'rb')
        frame = cv2.imread(sys.argv[2])
        faceCascade = cv2.CascadeClassifier(sys.argv[3])
        images = []
        names = []
        labels = []
        rownum = 0
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if rownum == 0:
                header = row
            else:
                idx = row[0]
                name = row[1]
                path = row[2]
                if isfile(path) and path.endswith('.jpg'):
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img_to_save = cv2.resize(img, (100, 100))
                    images.append(img_to_save)
                    names.append(name)
                    labels.append(int(idx))
            rownum += 1
        file.close()
        #recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer = cv2.face.createEigenFaceRecognizer(10, 10.0)
        recognizer.train(images, np.array(labels))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = faceCascade.detectMultiScale(gray, 1.2, 8)
        finds = []
        for (x, y, w, h) in faces:
            img_to_check = cv2.resize(gray[y: y + h, x: x + w], (100, 100)) 
            nbr_predicted, conf = recognizer.predict(img_to_check)
            if nbr_predicted > 0:
                finds.append('{"name": "%s", "x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (names[nbr_predicted], x, y, w, h))
        convert.Json.write_array('faces', finds)
