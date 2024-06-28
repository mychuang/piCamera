import cv2
import numpy as np

print("python version: ", cv2.__version__)

img = cv2.imread('1.jpg')
print(img.shape)
cv2.imshow('image', img)

"""
color change
"""
img2 = img.copy() 
img2[0:100 ,0:100] = [0, 0, 255]  # RGB，但此處使用 BGR 撰寫
img2[10:200, 10:200] = [0,255,0]
cv2.imshow('img2', img2)

"""
gray image
"""
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

k = cv2.waitKey(0)
"""
close window
"""
if k == 27:  # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'):  # wait for 's' key to save and exit
    cv2.imwrite('gray.png', gray)  # png, bmp, jpg
    cv2.destroyAllWindows()