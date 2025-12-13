# Google Maps Restaurant Search

這是一個使用 Google Maps API 搜尋附近餐廳的 Python 工具。

## 功能

*   **多種輸入模式**：支援地址、**Plus Codes** (如 `8QJ6+64 Taipei`) 或經緯度座標。
*   **擴充搜尋**：自動搜尋 `restaurant` 與 `food` 兩種類型，並自動翻頁抓取更多資料 (最多約 120 筆)。
*   **精簡匯出**：自動匯出 CSV 檔案，僅保留關鍵欄位 (`name`, `opening_hours`, `rating`, `types`, `vicinity`, `lat`, `lng`)。
*   **環境設定**：支援透過 `.env` 設定 API Key。

## 安裝

1. 安裝套件：
   ```bash
   pip install -r requirements.txt
   ```

2. 設定環境變數：
   複製 `EXAMPLE.env` 為 `.env`，並填入您的 Google Maps API Key。
   ```bash
   cp EXAMPLE.env .env
   # 編輯 .env 檔案
   ```

## 使用方法

執行主程式：
```bash
python main.py
```

### 操作流程

1. **選擇輸入模式**：
    *   輸入 `1`：使用地址或 Plus Code 搜尋 (例如: "台北車站" 或 "8QJ6+64 Taipei")
    *   輸入 `2`：使用座標搜尋 (例如: "25.0478,121.5170")
2. **輸入地點/座標**：依據選擇的模式輸入。
3. **輸入搜尋半徑**：輸入搜尋範圍 (公尺)，預設為 1000 公尺。
4. **查看結果**：程式將顯示搜尋到的餐廳資訊，並自動匯出 CSV 檔案至同目錄下。

## CSV 輸出

搜尋結果會自動匯出為 CSV 檔案，檔名格式為 `restaurants_YYYYMMDD_HHMMSS.csv`。
包含以下欄位：
- `name`: 店名
- `opening_hours`: 營業狀態 (顯示是否營業中)
- `rating`: 評分
- `types`: 類別標籤
- `vicinity`: 地址/鄰近地區
- `lat`: 緯度
- `lng`: 經度
