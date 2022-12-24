import time

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [
    [97, 138, 168, 255, 212, 255]  # blue
]

myColorValue = [
    [150, 150, 0]  # BGR
]

myPoints = []  # [x, y]


def empty(_):
    pass


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def drawCanvas(myPoint):
    # d = np.array(myPoint)
    # cv2.drawContours(imgContour, [d], 0, (255, 255, 255), 2)
    for point in myPoint:
        cv2.circle(imgContour, (point[0], point[1]), 14, myColorValue[0], cv2.FILLED)


def findColor(img_):
    kernel = np.ones((5, 5), np.uint8)
    imgHSV = cv2.cvtColor(img_, cv2.COLOR_BGR2HSV)
    newPoints = []

    lower = np.array(myColors[0][0:3])
    upper = np.array(myColors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgDilation = cv2.dilate(mask, kernel, iterations=1)  # add thickness
    imgErosion = cv2.erode(imgDilation, kernel, iterations=1)  # remove thickness

    x, y = getContours(imgErosion)
    # cv2.circle(imgContour, (x, y), 15, myColorValue[0], cv2.FILLED)
    if x != 0 and y != 0:
        newPoints.append([x, y])
    # cv2.imshow("mask", mask)
    # stackVideo = stackImages(0.7, ([img_, mask]))
    # cv2.imshow("stackVideo", stackVideo)
    return newPoints


def getContours(img_):
    contours, hierarchy = cv2.findContours(img_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, width, height = 0, 0, 0, 0
    for _, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        print(f'area: {area}')
        if area > 1:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, width, height = cv2.boundingRect(approx)
    return x + width // 2, y + height // 2


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgContour = img.copy()

    newPoints = findColor(img)  # getting list
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawCanvas(myPoints)

    cv2.imshow("result", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
