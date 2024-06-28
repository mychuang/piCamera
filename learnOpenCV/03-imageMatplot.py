import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('1.jpg')
#cv2.imshow('gray', img) #默認使用 BGR 

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #轉RGB

# 定義 x 軸和 y 軸上的數據點
x = [100, 200, 300]
y = [100, 200, 100]
plt.plot(x, y)

plt.xticks([])
plt.yticks([]) 
plt.imshow(img_rgb)
plt.show()