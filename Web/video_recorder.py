import os
import glob
import cv2

def delete_oldest_files(directory, extensions, max_files):
    """
    刪除最舊的影片檔案，維持檔案數量上限
    """
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f'*{ext}')))
    files = [f for f in files if os.path.basename(f)[:8].isdigit()]
    if len(files) > max_files:
        files.sort(key=os.path.getmtime)
        os.remove(files[0])

def save_video(frames, filename, fourcc, fps, size):
    """
    將 frames 存成影片
    """
    out = cv2.VideoWriter(filename, fourcc, fps, size)
    for f in frames:
        out.write(f)
    out.release()
    print(f"✅ 影像已輸出：{filename}")
