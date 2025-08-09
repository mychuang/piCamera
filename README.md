# piCamera

本專案預期搭建樹莓派網路視訊串流系統，分四階段進行

一、python opencv 開啟相機影像

二、python flask 網站後台建置

三、前端搭建與影像串流顯示

四、DNS與路由設置

## Web

- 前後端影像串流雛形

## 環境配置

- 樹莓派4, OS release 2024-3-15

- python version: 3.11.9

- opencv version: 4.10.0

## raspberry
- 建立虛擬環境
python3 -m venv venv

- 啟用虛擬環境
source venv/bin/activate  # Linux/macOS

- 安裝套件
pip install "opencv-python<4.10" "numpy<2.0.0" mediapipe --force-reinstall

- deactivate

## 學習策略 : learnOpenCV

- 相機操作

- 圖像繪製