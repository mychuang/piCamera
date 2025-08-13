from enum import Enum

class StreamMode(Enum):
    NORMAL = 1
    MOUTH_NOSE_DETECTION = 2
    YOLO = 3  # 預留未來擴充
    
video_extensions = ['.mp4', '.mov', '.avi']

CONFIG = {
    "fps": 20.0,
    "width": 640,
    "height": 480,
    "max_files": 5,
    "interval_sec": 10,
    "missing_threshold": 10  # 連續多少幀缺失才警告
}
