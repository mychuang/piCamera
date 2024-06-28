import numpy as np
import cv2

img = cv2.imread('1.jpg')
cv2.imshow('image', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', hsv)

RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imshow('RGB', RGB)

k = cv2.waitKey(0)
if k == 27:  # wait for ESC key to exit
    print("ESC")
    cv2.destroyAllWindows()
elif k == ord('s'):  # wait for 's' key to save and exit
    print("s")
    cv2.imwrite('gray.png', gray)  # png, bmp, jpg
    cv2.destroyAllWindows()