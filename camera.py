import cv2
import numpy as np
import platform
from datetime import datetime
import time
import glob
import os

# 支援的影片副檔名
video_extensions = ['.mp4', '.mov', '.avi']

def delete_oldest_files(extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join("./", f'*{ext}')))

    if len(files) > 5:
        files.sort(key=os.path.getmtime)
        print("刪除檔案： " + files[0])
        os.remove(files[0])

"""
確認攝影機狀態
"""
camera_found = False
cap = None
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

"""
設置影像匯出格式
"""
os_platform = platform.system()
print(f"作業系統： {os_platform}")
if os_platform == "Linux":
    formatName = video_extensions[0]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
elif os_platform == "Darwin":
    formatName = video_extensions[1]
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
else:
    formatName = video_extensions[2]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

fps = 20.0
width = 640
height = 480

"""
開啟攝影機運作與匯出
"""
interval = 10
start_time = time.time()
frames = []
frame_count = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    ret, frame = cap.read()
    if ret:
        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")

        cv2.putText(frame, f'Time: {dt_string}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        frames.append(frame.copy())  # 將幀添加到列表中
        frame_count += 1

        if elapsed_time >= interval:
            print("正在輸出影像")
            filename = dt_string + formatName
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            # 寫入過去10秒的所有幀
            for frame in frames:
                out.write(frame)

            out.release()  # 確保每個文件都能正常寫入和關閉
            print(f"影像已輸出： {filename}")
            print(f"共 {frame_count} 幀")

            # 呼叫函數來管理檔案
            delete_oldest_files(video_extensions)

            # 重置計時器和幀列表
            start_time = current_time
            frames = []
            frame_count = 0

    k = cv2.waitKey(1)
    if k == 27:  # ESC鍵
        break

cap.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()

