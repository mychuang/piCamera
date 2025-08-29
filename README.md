# 樹梅派多工監控網站 

## 專案概述
本專案以 **樹莓派 (Raspberry Pi)** 為基礎，整合影像辨識與網頁展示功能，達成多工監控目標。  

功能模組：  
1. **嬰兒臉部辨識**：整合 [Mediapipe](https://github.com/google/mediapipe)  
2. **人物監測**：整合 [YOLO](https://github.com/ultralytics/yolov5) (待處理)  
3. **網路流量控管**：整合 [Pi-hole](https://pi-hole.net/) (待處理)  

---

## 系統架構與技術棧
專案將分為三大核心模組，並結合後端常駐服務：  

1. **前端**：`HTML`、`CSS`、`JavaScript`  
2. **後端**：`Flask`、`OpenCV`、`YOLO`、`Mediapipe`  
3. **常駐運行模組**：`Pi-hole`  

---

## 建構步驟

### 1. 建立虛擬環境並啟用 (Windows)
windows如下
```sh
python -m venv venv
venv\Scripts\activate
```
樹梅派如下
```sh
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
```

### 2. 安裝相關套件

```sh
pip install flask pytest

pip install "opencv-python<4.10" "numpy<2.0.0" mediapipe --force-reinstall
````

### 3. 樹梅派之vpn 

insall tailscale in raspberry 4
````sh
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
````