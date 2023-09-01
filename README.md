# GKF Data Crawler

## 功能

執行單一執行檔，下載gkf platform上saved Views中的資料檔案（xlsxs）

## 安裝

Python版本為：3.10.4

poetry版本為：1.6.1

### 取得專案
```bash
git clone git@github.com:allenchengf/gfk-crawler.git
```

### 安裝套件
```bash
poetry env use python
```
```bash
poetry install
```
## 使用
以Pyinstaller指令執行匯出exe後，之後即可以exe執行檔搭配.env環境變數檔，執行下載動作
![](/Users/allenchen/Downloads/螢幕擷取畫面 2023-09-01 133445.png)
### 匯出執行檔exe
```bash
pyinstaller -F ,\app.py
```

### .env 環境變數說明
```bash
EMAIL= 帳號
PASSWORD= 密碼
DOWNLOAD_PATH = 路徑 (需為完整路徑，如：C:\project\gkf-data-crawler-exe\download)
```




