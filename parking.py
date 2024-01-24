
import cv2
import pickle
import cvzone
import numpy as np

url = 'http://192.168.0.110:8080/video'
cap = cv2.VideoCapture(url)

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

prevOccupied = [False] * len(posList)

width, height = 290, 180

def checkParkingSpace(imgPro):
    spaceCounter = 0
    occupiedSlots = []

    for i, pos in enumerate(posList):
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
            occupiedSlots.append(chr(ord("A") + i))

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

        cv2.putText(img, f'Car {chr(ord("A") + i)}', (x, y + height + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 128, 0), 2)

    emptySlots = [chr(ord("A") + i) for i in range(len(posList)) if chr(ord("A") + i) not in occupiedSlots]
    emptySlotsText = ', '.join(emptySlots)
    cv2.putText(img, f'Empty Slots: {emptySlotsText}', (0, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (70, 70),
                       scale=1, thickness=2, offset=15, colorR=(0, 200, 0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)
