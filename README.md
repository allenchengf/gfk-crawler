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
### 複製.env
```bash
cp .env.example .env
```

### 安裝套件
```bash
poetry env use python
```
```bash
poetry install
```
## 使用
以Pyinstaller指令執行匯出exe後，即可搭配.env環境變數檔，執行下載動作
<a href="https://imgur.com/NLj1B0P"><img src="https://i.imgur.com/NLj1B0P.png" title="source: imgur.com" /></a>
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




