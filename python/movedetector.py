import cv2, sys

if __name__ == '__main__':
    if len(sys.argv) == 3:
        firstFrame = cv2.imread(sys.argv[1])
        img = cv2.imread(sys.argv[2])
        firstGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
        firstGray = cv2.equalizeHist(firstGray)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        #gray = cv2.GaussianBlur(gray, (21, 21), 0)
        frameDelta = cv2.absdiff(firstGray, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        #cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contourMax = None
        areaMax = None
        for c in cnts:
            contour = cv2.contourArea(c)
            if contour < 500:
                continue
            if contourMax is None or contour > contourMax:
                contourMax = contour
                areaMax = c
        if not areaMax is None:
            (x, y, w, h) = cv2.boundingRect(areaMax)
            print '{"x": "%s", "y": "%s", "w": "%s", "h": "%s"}' % (x, y, w, h)
    sys.stdout.flush()
