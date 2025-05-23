import cv2
import numpy as np
import platform
from datetime import datetime
import time
import glob
import os

# 參數設定區（建議日後抽成 config）
CONFIG = {
    "fps": 20.0,
    "width": 640,
    "height": 480,
    "interval_sec": 10,
    "max_files": 5,
    "show_preview": True  # 若日後嵌入 Flask，可改為 False
}

# 支援的影片副檔名
video_extensions = ['.mp4', '.mov', '.avi']

# 刪除過舊影片，保持最大檔案數
def delete_oldest_files(extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join("./", f'*{ext}')))

    # 過濾合法格式的檔案（例如檔名以數字開頭）
    files = [f for f in files if os.path.basename(f)[:8].isdigit()]
    
    if len(files) > CONFIG["max_files"]:
        files.sort(key=os.path.getmtime)
        print("刪除檔案： " + files[0])
        os.remove(files[0])

# 嘗試偵測攝影機
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

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["height"])

# 根據作業系統選擇影片格式
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

# 初始化錄影參數
start_time = time.time()
frames = []
frame_count = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    ret, frame = cap.read()
    if ret:
        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")

        # 加上時間戳記
        cv2.putText(frame, f'Time: {dt_string}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # 顯示畫面（可選）
        if CONFIG["show_preview"]:
            cv2.imshow('frame', frame)

        frames.append(frame.copy())
        frame_count += 1

        # 安全機制：防止 buffer 無限擴張
        if len(frames) > CONFIG["fps"] * CONFIG["interval_sec"] * 1.5:
            print("⚠️ Frame buffer 過大，自動重置")
            frames = []
            frame_count = 0
            start_time = current_time
            continue

        # 每 interval 秒儲存一次影片
        if elapsed_time >= CONFIG["interval_sec"]:
            print("正在輸出影像")
            filename = f"{dt_string}_{CONFIG['interval_sec']}s{formatName}"
            out = cv2.VideoWriter(filename, fourcc, CONFIG["fps"], (CONFIG["width"], CONFIG["height"]))

            if not out.isOpened():
                print(f"❌ 無法開啟 VideoWriter，跳過輸出：{filename}")
            else:
                for f in frames:
                    out.write(f)
                out.release()
                print(f"✅ 影像已輸出：{filename}")
                print(f"🎞️ 共 {frame_count} 幀")

                # 檔案管理
                delete_oldest_files(video_extensions)

            # 重置 buffer 與計時
            start_time = current_time
            frames = []
            frame_count = 0

    # 按 ESC 結束
    if cv2.waitKey(1) == 27:
        break

# 收尾
cap.release()
cv2.destroyAllWindows()
