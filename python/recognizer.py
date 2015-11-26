import cv2, os, detector, csv
import numpy as np

from os.path import isfile, join

class FaceRecognizer(object):

    def __init__(self, csvFile):
        self.faceDetector = detector.FaceDetector()
        images = []
        self.names = []
        labels = []
        rownum = 0
        file = open(csvFile, 'rb')
        reader = csv.reader(file, delimiter=';')
        print 'Load database file'
        for row in reader:
            if rownum == 0:
                header = row
            else:
                print '> %s: %s, %s: %s (%s=%s)' % (header[0], row[0], header[1], row[1], header[2], row[2])
                idx = row[0]
                name = row[1]
                path = row[2]
                if isfile(path) and path.endswith('.jpg'):
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img_to_save = cv2.resize(img, (100, 100))
                    images.append(img_to_save)
                    self.names.append(name)
                    labels.append(int(idx))
            rownum += 1
        file.close()
        #self.recognizer = cv2.face.createLBPHFaceRecognizer()
        self.recognizer = cv2.face.createEigenFaceRecognizer(10, 10.0)
        self.recognizer.train(images, np.array(labels))
        self.borderWidth = 1
        self.borderColor = (255, 0, 0)

    def find(self, img, draw = False):
        faces, gray = self.faceDetector.find(img, False)
        for (x, y, w, h) in faces:
            img_to_check = cv2.resize(gray[y: y + h, x: x + w], (100, 100)) 
            nbr_predicted, conf = self.recognizer.predict(img_to_check)
            if nbr_predicted > 0:
                print '%s is recognized (%s)' % (self.names[nbr_predicted], conf)
                if draw == True:
                    cv2.putText(img, self.names[nbr_predicted], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, self.borderColor, 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), self.borderColor, self.borderWidth)
