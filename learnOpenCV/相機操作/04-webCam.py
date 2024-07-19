import cv2
import numpy as np

camera_found = False
for i in range(5):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret:
        camera_found = True
        print(f"使用攝影機 {i}")
        break
    cap.release()

print("當前攝影機的影像寬度: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("當前攝影機的影像高度: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 設置攝影機影像的寬度為 640
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# 設置攝影機影像的高度為 480
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print("設置後攝影機的影像寬度 " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("設置後攝影機的影像高度: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
"""
print("當前攝影機的幀率（每秒幀數） " + str(cap.get(cv2.CAP_PROP_FPS)))
print("影片編碼格式 " + str(cap.get(cv2.CAP_PROP_FOURCC)))
print("亮度 " + str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
print("對比度 " + str(cap.get(cv2.CAP_PROP_CONTRAST)))
print("飽和度 " + str(cap.get(cv2.CAP_PROP_SATURATION)))
print("色調 " + str(cap.get(cv2.CAP_PROP_HUE)))
print("增益 " + str(cap.get(cv2.CAP_PROP_GAIN)))
print("曝光 " + str(cap.get(cv2.CAP_PROP_EXPOSURE)))
print("是否轉換為 RGB " + str(cap.get(cv2.CAP_PROP_CONVERT_RGB)))
"""

# 進入無窮迴圈以不斷抓取影像
while True:
    # 從攝影機讀取一幀影像，ret: 是否成功讀取，frame: 讀取的影像
    ret, frame = cap.read()
    
    # 檢查是否成功讀取影像
    if frame is not None:
        # 獲取 FPS (每秒幀數)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 調整影像大小至 320x200，使用 INTER_AREA 進行插值
        frame=cv2.resize(frame, (320,200), interpolation=cv2.INTER_AREA)
        # 在影像的右上角打印 FPS
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # 顯示影像在名為 'frame' 的視窗中
        cv2.imshow('frame', frame)
    
    # 等待 1 毫秒以檢查是否有按鍵按下
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k== ord('s'):
        cv2.imwrite('test.jpg',frame)

# 釋放攝影機資源
cap.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()