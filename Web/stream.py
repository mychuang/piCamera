# camera.py
import cv2
import numpy as np
import platform
from datetime import datetime
import time
import glob
import os
import threading
from PIL import Image
from io import BytesIO

CONFIG = {
    "fps": 20.0,
    "width": 640,
    "height": 480,
    "interval_sec": 10,
    "max_files": 5,
    "show_preview": False
}

video_extensions = ['.mp4', '.mov', '.avi']

latest_frame = None  

def get_latest_frame_bytes(resize_factor=0.5, quality=30):
    global latest_frame
    if latest_frame is None:
        return None

    # 轉成 PIL 處理
    img = cv2.cvtColor(latest_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    # 縮小圖片
    w, h = img.size
    img.thumbnail((int(w * resize_factor), int(h * resize_factor)))

    # 存為 JPEG Bytes
    bytes_io = BytesIO()
    img.save(bytes_io, 'jpeg', quality=quality)
    return bytes_io.getvalue()

def delete_oldest_files(extensions):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join("./", f'*{ext}')))
    files = [f for f in files if os.path.basename(f)[:8].isdigit()]
    if len(files) > CONFIG["max_files"]:
        files.sort(key=os.path.getmtime)
        os.remove(files[0])

def detect_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        ret, _ = cap.read()
        if ret:
            print(f"使用攝影機 {i}")
            return cap
        cap.release()
    return None

def get_video_format():
    os_platform = platform.system()
    if os_platform == "Linux":
        return video_extensions[0], cv2.VideoWriter_fourcc(*'mp4v')
    elif os_platform == "Darwin":
        return video_extensions[1], cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    else:
        return video_extensions[2], cv2.VideoWriter_fourcc(*'XVID')

def run_camera_loop():
    cap = detect_camera()
    if not cap:
        print("無法找到可用的攝影機。")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["height"])

    formatName, fourcc = get_video_format()
    start_time = time.time()
    frames = []
    frame_count = 0

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        ret, frame = cap.read()
        if not ret:
            continue

        global latest_frame
        latest_frame = frame.copy()  # ← 即時更新

        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.putText(frame, f'Time: {dt_string}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if CONFIG["show_preview"]:
            cv2.imshow('frame', frame)

        frames.append(frame.copy())
        frame_count += 1

        if len(frames) > CONFIG["fps"] * CONFIG["interval_sec"] * 1.5:
            print("⚠️ Frame buffer 過大，自動重置")
            frames = []
            frame_count = 0
            start_time = current_time
            continue

        if elapsed_time >= CONFIG["interval_sec"]:
            filename = f"{dt_string}_{CONFIG['interval_sec']}s{formatName}"
            out = cv2.VideoWriter(filename, fourcc, CONFIG["fps"], (CONFIG["width"], CONFIG["height"]))
            if out.isOpened():
                for f in frames:
                    out.write(f)
                out.release()
                print(f"✅ 影像已輸出：{filename}")
                print(f"🎞️ 共 {frame_count} 幀")
                delete_oldest_files(video_extensions)
            start_time = current_time
            frames = []
            frame_count = 0

        if CONFIG["show_preview"] and cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def run_in_background():
    thread = threading.Thread(target=run_camera_loop, daemon=True)
    thread.start()
