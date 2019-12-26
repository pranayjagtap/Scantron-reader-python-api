
import sys
sys.path.append('/home/jilia/.local/lib/python2.7/site-packages')
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def process(path):
    #Answers marked by student would be stored in result list
    result = []


    image = cv2.imread(path)
    #Adding resize to deal with issues faced when camera quality of Pixel was too high resulting in high resolution pictures
    image = cv2.resize(image,(525L,700L))
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged_image = cv2.Canny(grayscale_image, 75, 200)
    cnts = cv2.findContours(edged_image.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None
    #Get the test box
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                docCnt = approx
                break

    warped = four_point_transform(grayscale_image, docCnt.reshape(4, 2))

    #Otsu threshold
    thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            questionCnts.append(c)
    questionCnts = contours.sort_contours(questionCnts,
        method="top-to-bottom")[0]
  
    for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
        cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
        bubbled = None
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)


        result.append(bubbled[1])
    return result


if __name__ == '__main__':
    process("")