import cv2
import numpy as np

# 建立一個黑色圖像，大小為512x512像素，且有3個色彩通道 (RGB)
img = np.zeros((512, 512, 3), np.uint8) 

"""
Draw Line
"""
# 在圖像上畫一條藍色的對角線，
# 從左上角 (0, 0) 到右下角 (511, 511)，線條的粗細為5像素
cv2.line(img, pt1=(0, 0), pt2=(511, 511), color=(255, 0, 0), thickness=5)

"""
Draw Circle
"""
cv2.circle(img, center=(447, 63), radius=63, color=(0, 0, 255), thickness=-1)  # center, radius, color, thickness=None
cv2.circle(img, center=(0, 30), radius=10, color=(255,0,0), thickness=2)

"""
Draw Rectangle
"""
# (384, 0): 矩形的左上角頂點座標 (x, y)
# (510, 128): 矩形的右下角頂點座標 (x, y)
# (0, 255, 0): 矩形框的顏色，這裡是綠色 (B, G, R)
# 3: 矩形框的線條粗細，這裡是 3 像素
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)

"""
不規則多邊形
"""
# 定義一組點的坐標，這些點將用來繪製多邊形
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
print(pts.shape)

# 重塑 pts 以符合繪製多邊形的需求
pts = pts.reshape((-1, 1, 2))
print(pts.shape)

# 在圖像上畫一個由 pts 定義的多邊形，
# 最後一個參數 True 表示多邊形是閉合的，顏色為黃色，厚度為1像素
cv2.polylines(img, [pts], True, (0,255,255))

"""
橢圓形
"""
# 第一個参数是中心點的位置座標。 第二個参数是長短軸長度。第三個參數是椭圆沿逆時針方向旋轉的角度。
# 第四跟第五個參數是順時針方向起始的角度和结束角度, 如果是 0 很 360 就是整個椭圆
cv2.ellipse(img, center=(256, 256),
            axes=(100, 50), angle=0,
            startAngle=0, endAngle=180,
            color=(180,180,180),
            thickness=-1)

cv2.ellipse(img, center=(100, 256),
            axes=(100, 50), angle=0,
            startAngle=90, endAngle=360,
            color=(180,180,180),
            thickness=1)

"""
箭頭
"""
cv2.arrowedLine(img,pt1=(21, 13), pt2=(151, 401), color=(100, 0, 100), thickness=5)

"""
文字
"""
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, text='OpenCV', org=(10, 150), fontFace=font,
            fontScale=1, color=(0, 0, 255), thickness=1)

"""
開啟窗口
"""
# 建立一個命名為 'example' 的窗口，0 表示可以調整窗口大小
winname = 'example'
cv2.namedWindow(winname, 0)

# 在命名為 'example' 的窗口中顯示圖像
cv2.imshow(winname, img)

# 等待使用者按下任意鍵
cv2.waitKey(0)

# 關閉所有 OpenCV 窗口
cv2.destroyAllWindows()

