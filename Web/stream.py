# camera.py
import cv2
import numpy as np
import platform
from datetime import datetime
import time
import glob
import os
import threading
from utils import init_face_mesh, detect_face_landmarks, draw_face_landmarks

video_extensions = ['.mp4', '.mov', '.avi']

CONFIG = {
    "fps": 20.0,
    "width": 640,
    "height": 480,
    "max_files": 5,
    "interval_sec": 10
}

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
    print(f"作業系統： {os_platform}")
    if os_platform == "Linux":
        return video_extensions[0], cv2.VideoWriter_fourcc(*'mp4v')
    elif os_platform == "Darwin":
        return video_extensions[1], cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    else:
        return video_extensions[2], cv2.VideoWriter_fourcc(*'XVID')

def run_camera_loop():
    face_mesh = init_face_mesh()
    cap = detect_camera()
    if not cap:
        print("無法找到可用的攝影機。")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["height"])
    cap.set(cv2.CAP_PROP_FPS, CONFIG["fps"])

    formatName, fourcc = get_video_format()
    start_time = time.time()
    frames = []
    frame_count = 0

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        ret, frame = cap.read()

        if not ret:
            print("無法讀取影像幀，嘗試重新連接攝影機...")
            cap.release()
            cap = detect_camera()
            if not cap:
                print("重新連接攝影機失敗，停止串流。")
                break
            #cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["width"])
            #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["height"])
            #cap.set(cv2.CAP_PROP_FPS, CONFIG["fps"])
            continue

        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.putText(frame, f'Time: {dt_string}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        results = detect_face_landmarks(face_mesh, frame)
        draw_face_landmarks(frame, results)

        # 將當前 frame 編碼為 JPEG
        ret_jpeg, jpeg = cv2.imencode('.jpg', frame)
        if not ret_jpeg:
            print("無法將影像編碼為 JPEG, 跳過此幀。")
            continue 

        frames.append(frame.copy())
        frame_count += 1

        if len(frames) > CONFIG["fps"] * CONFIG["interval_sec"] * 1.5:
            print("⚠️ Frame buffer 過大，自動重置")
            frames = []
            frame_count = 0
            start_time = current_time
            continue

        if elapsed_time >= CONFIG["interval_sec"]:
            print("正在輸出影像")
            filename = f"{dt_string}_{CONFIG['interval_sec']}s{formatName}"
            out = cv2.VideoWriter(filename, fourcc, CONFIG["fps"], (CONFIG["width"], CONFIG["height"]))
            if out.isOpened():
                for f in frames:
                    out.write(f)
                out.release()
                print(f"✅ 影像已輸出：{filename}")
                print(f"🎞️ 共 {frame_count} 幀")
                delete_oldest_files(video_extensions)
            else:
                print(f"❌ 錯誤: 無法打開 {filename} 進行寫入。請檢查編碼器或檔案路徑。")
            start_time = current_time
            frames = []
            frame_count = 0

        # 使用 yield 返回 JPEG 格式的字節串
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    face_mesh.close()
    cap.release()

def run_in_background():
    thread = threading.Thread(target=run_camera_loop, daemon=True)
    thread.start()
