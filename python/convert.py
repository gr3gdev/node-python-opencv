import sys, cv2, json

class Parser:
    @staticmethod
    def getImage(value):
        img = None
        for ki, vi in value.iteritems():
            if ki == 'path':
                img = cv2.imread(vi)
            if ki == 'base64':
                img = cv2.imdecode(vi)
        return img

    @staticmethod
    def loadMove(data):
        retour = dict()
        jdata = json.loads(data)
        for key, value in jdata.iteritems():
            if key == 'image1':
                retour['image1'] = Parser.getImage(value)
            if key == 'image2':
                retour['image2'] = Parser.getImage(value)
        return retour

    @staticmethod
    def loadFace(data):
        retour = dict()
        jdata = json.loads(data)
        for key, value in jdata.iteritems():
            if key == 'image':
                retour['image'] = Parser.getImage(value)
            if key == 'haarcascade':
                retour['haarcascade'] = Parser.getImage(value)
        return retour

    @staticmethod
    def write(data):
        print data
        sys.stdout.flush()

    @staticmethod
    def write_array(root, array):
        print '{"%s": [' % root
        index = 0
        for elt in array:
            index += 1
            print elt
            if index < len(array):
                print ','
        print ']}'
        sys.stdout.flush()
