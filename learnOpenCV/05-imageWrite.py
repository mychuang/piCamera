import cv2
import numpy as np
import platform
from datetime import datetime

camera_found = False
for i in range(5):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret:
        camera_found = True
        print(f"使用攝影機 {i}")
        break
    cap.release()

if not camera_found:
    print("無法找到可用的攝影機。")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 獲取操作系統平台名稱
os = platform.system()
print(os)
if os == "Linux":
    filename = "test.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
elif os == "Darwin":
    filename = "test.mov"
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
else:
    filename = "test.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

ftp=20.0
width = 640
height = 480
out = cv2.VideoWriter(filename, fourcc, ftp, (width, height))

# 進入無窮迴圈以不斷抓取影像
while True:
    # 從攝影機讀取一幀影像，ret: 是否成功讀取，frame: 讀取的影像
    ret, frame = cap.read()
    
    # 檢查是否成功讀取影像
    if frame is not None:

        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.putText(frame, f'Time: {dt_string}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # 將影像寫入影片文件
        
        out.write(frame)
        cv2.imshow('frame', frame)
    
    # 等待 1 毫秒以檢查是否有按鍵按下
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k== ord('s'):
        cv2.imwrite('test.jpg',frame)


cap.release()
out.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()