import cv2
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--video", help="Chemin de votre video. Ne pas specifier si non")
args = parser.parse_args()

# print(args.video)

print("Appretez-vous à devenir invisible....")

cap = cv2.VideoCapture(args.video if args.video else 0)

time.sleep(4)

background = 0

for i in range(60):
    ret, background = cap.read()
print(background.shape)

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(image, image, mask=mask2)

    rendu_final = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.namedWindow("Invisible", cv2.WINDOW_NORMAL)

    cv2.imshow('Invisible', rendu_final)

    k = cv2.waitKey(10)

    if k == 27:
        break


