import cv2
import time
from datetime import datetime
from config import CONFIG, video_extensions, StreamMode
from eye_detection import init_face_mesh, detect_face_landmarks, draw_face_landmarks, is_mouth_nose_visible, MOUTH_NOSE_LANDMARKS
from camera import detect_camera, get_video_format
from video_recorder import delete_oldest_files, save_video
import threading

def draw_mouth_nose_points(frame, results):
    """
    在畫面上標記口鼻關鍵點
    """
    if results.multi_face_landmarks:
        h, w, _ = frame.shape
        for idx in MOUTH_NOSE_LANDMARKS:
            lm = results.multi_face_landmarks[0].landmark[idx]
            px, py = int(lm.x * w), int(lm.y * h)
            color = (0, 0, 255) if 0 <= lm.x <= 1 and 0 <= lm.y <= 1 else (128, 128, 128)
            cv2.circle(frame, (px, py), 4, color, -1)
    return frame

def run_camera_loop(mode: StreamMode):
    face_mesh = None
    if mode == StreamMode.MOUTH_NOSE_DETECTION:
        face_mesh = init_face_mesh()

    cap = detect_camera()
    if not cap:
        print("無法找到可用的攝影機。")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG["width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG["height"])
    cap.set(cv2.CAP_PROP_FPS, CONFIG["fps"])

    formatName, fourcc = get_video_format(video_extensions)
    start_time = time.time()
    frames = []
    missing_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取影像幀")
            break

        dt_string = datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.putText(frame, f'Time: {dt_string}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # --- 模式判斷 ---
        if mode == StreamMode.MOUTH_NOSE_DETECTION:
            results = detect_face_landmarks(face_mesh, frame)
            draw_face_landmarks(frame, results)
            draw_mouth_nose_points(frame, results)

            if is_mouth_nose_visible(results):
                missing_counter = 0
                status_text, status_color = "Mouth/Nose Visible", (0, 255, 0)
            else:
                missing_counter += 1
                if missing_counter >= CONFIG["missing_threshold"]:
                    status_text, status_color = "⚠️ Missing!", (0, 0, 255)
                else:
                    status_text, status_color = "Checking...", (0, 255, 255)

            cv2.putText(frame, status_text, (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

        elif mode == StreamMode.NORMAL:
            pass  # 單純錄影，不做偵測

        elif mode == StreamMode.YOLO:
            # 預留 YOLO 偵測邏輯
            pass

        # --- 錄影 ---
        frames.append(frame.copy())

        if time.time() - start_time >= CONFIG["interval_sec"]:
            filename = f"{dt_string}_{CONFIG['interval_sec']}s{formatName}"
            save_video(frames, filename, fourcc, CONFIG["fps"], (CONFIG["width"], CONFIG["height"]))
            delete_oldest_files("./", video_extensions, CONFIG["max_files"])
            frames = []
            start_time = time.time()

        # --- 串流輸出 ---
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

    if face_mesh:
        face_mesh.close()
    cap.release()

def run_in_background(mode: StreamMode):
    thread = threading.Thread(target=run_camera_loop(mode), daemon=True)
    thread.start()
