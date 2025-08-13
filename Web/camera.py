import cv2
import platform

def detect_camera(max_index=5):
    """
    嘗試找到可用攝影機
    """
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        ret, _ = cap.read()
        if ret:
            print(f"使用攝影機 {i}")
            return cap
        cap.release()
    return None

def get_video_format(video_extensions):
    """
    根據作業系統回傳影片格式與 fourcc 編碼器
    """
    os_platform = platform.system()
    print(f"作業系統： {os_platform}")
    if os_platform == "Linux":
        return video_extensions[0], cv2.VideoWriter_fourcc(*'mp4v')
    elif os_platform == "Darwin":
        return video_extensions[1], cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    else:
        return video_extensions[2], cv2.VideoWriter_fourcc(*'XVID')