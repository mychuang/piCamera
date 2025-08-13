import mediapipe as mp
import cv2

# 初始化模組級別的變數
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

def init_face_mesh():
    # 初始化 Mediapipe 的 Face Mesh 模型
    return mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=False,  # 開啟精細模式（包含虹膜等細節）
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

def detect_face_landmarks(face_mesh, frame):
    # 將 BGR 畫面轉成 RGB 再處理
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(rgb_frame)

def draw_face_landmarks(frame, results):
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                # 如果你只想畫輪廓（不要 468 點全部），將 FACEMESH_TESSELATION 改成 FACEMESH_CONTOURS
                connections=mp_face_mesh.FACEMESH_CONTOURS, 
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

MOUTH_NOSE_LANDMARKS = [1, 13, 14, 98, 327]

def is_mouth_nose_visible(results, required_ratio=0.6):
    """
    判斷口鼻是否可見
    """
    if not results.multi_face_landmarks:
        return False

    face_landmarks = results.multi_face_landmarks[0]
    visible_count = sum(
        1 for idx in MOUTH_NOSE_LANDMARKS
        if 0 <= face_landmarks.landmark[idx].x <= 1 and 0 <= face_landmarks.landmark[idx].y <= 1
    )

    return (visible_count / len(MOUTH_NOSE_LANDMARKS)) >= required_ratio
