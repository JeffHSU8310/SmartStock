# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.42] - 2026-08-03

### 🎯 研讀 StockBuild 串接券商 API 金律 + Shioaji 行情 REST API 流量節流防護 + WebSocket 實時串流訂閱介面 (v1.0.42)
- **研讀與借鏡 StockBuild 專案 (https://github.com/JeffHSU8310/StockBuild)**：
  - 深入研讀與學習 `StockBuild` 在與永豐金 Shioaji API 串接獲取最新商品報價時的雙軌架構（WebSocket 實時串流推送 + REST API 批次快照流量防護），並全面調整 SmartStock 行情引擎。
- **REST API 快照流量防護器 (Throttle Guard) ([src/sinopac_engine.py](file:///e:/SmartStock/src/sinopac_engine.py))**：
  - 新增 `MIN_SNAPSHOT_INTERVAL = 2.5` 秒最小快照間隔防護與 `last_realtime_cache` 快取機制，防護 `get_realtime_quotes` 過度頻繁請求，恪守 Shioaji 官方 10 秒 50 次 (snapshots/ticks/kbars) 存取限制金律。
- **WebSocket 實時報價訂閱與退訂介面 ([src/sinopac_engine.py](file:///e:/SmartStock/src/sinopac_engine.py))**：
  - 新增 `subscribe_lock` (線程安全鎖) 與 `subscribed_contracts` 集合。
  - 實作 `set_quote_callbacks()`、`subscribe_quote()` 及 `unsubscribe_quote()`，支援實時 Tick 與 BidAsk (五檔) 串流報價訂閱。
- **沙盒自動化驗證**：
  - 於沙盒中 100% 通過單元測試腳本 `test_quote_engine.py`，驗證初始化鎖、流量保護與 Rule 22 券商真實數據金律無誤。
- **版本規範**：
  - 版號升級至 v1.0.42，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.41] - 2026-08-02

### 🎯 100% 券商真實數據金律 (Rule 22) + 徹底廢除假數據 + 布林通道第一層第二層獨立啟用 (v1.0.41)
- **寫入 Rule 22 重點規則 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 增設最高原則 **Rule 22（100% 券商真實數據金律）**：本系統所有行情與指標分析 100% 必須自永豐金 API 下載真實數據，嚴禁生成任何 1 筆虛擬/假數據！
- **徹底廢除擬真/合成數據 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 徹底停用與廢除 `_generate_fallback_kbars`！若 API 未連線或無交易數據時，嚴格回傳 `[]`（空列表），主圖保持乾淨並提示警示文字。
- **加權指數/櫃買指數/台指期全真實數據合約搜尋重構 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 實作 Shioaji `api.Contracts.Indexs` / `api.Contracts.Indices` (TSE/OTC) 與 `Futures.TXF` 之全屬性動態遍歷 (Iterative Contract Search)，確保 100% 成功取得官方真實合約並下載實時歷史數據。
- **布林通道第一層與第二層獨立啟用 CheckBox ([src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py), [src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 新增 `chk_bb_b1` (啟用第一層通道 Upper1/Lower1) 與 `chk_bb_b2` (啟用第二層通道 Upper2/Lower2) 獨立勾選控制項。
- **版本規範**：
  - 版號升級至 v1.0.41，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.40] - 2026-08-02

### 🎯 期貨10年數據 + 大盤指數解析修復 + 主副圖 Overlay 釘選 + 布林獨立4條上下限 + 全指標 JSON 永久儲存 (v1.0.40)
- **期貨數據天數解鎖 10 年以上 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 徹底移除期貨僅下載 60 天的限制，全數擴充解鎖至 **3,650 天 (10 年以上)**，對齊股票歷史長度需求。
- **加權指數與櫃買指數 API 雙版本相容解析 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 相容 Shioaji `api.Contracts.Indices` 與 `api.Contracts.Indexs` 結構，精準抓取 `TSE001` / `IX0001` 與 `OTC101` / `IX0043` 歷史數據。
- **主圖與副圖左上角 Overlay 100% 畫布釘選 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 連結 ViewBox `sigRangeChanged` 訊號，確保縮放、滾動或拖曳時，主圖左上角 (均線數據)、副圖一左上角、副圖二左上角數據與趨勢符號 (**`↗` 上彎 / `↘` 下彎 / `→` 持平**) 100% 釘選於畫布頂角。
- **副圖一預設永遠為成交量 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py), [src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py))**：
  - 固定副圖一預設指標永遠為 `成交量 (Volume)`。
- **布林通道 4 條獨立上下限倍數設定 ([src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py), [src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 將布林通道倍數拆解為 Upper1 K (第一層上限)、Lower1 K (第一層下限)、Upper2 K (第二層上限)、Lower2 K (第二層下限) 4 組獨立數字微調器。
- **全指標與顏色設定永久 JSON 自動儲存 ([src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py))**：
  - 實作 `config/indicator_config.json` 讀寫機制，用戶點擊儲存後自動持久化寫入，重開軟體自動完全還原。
- **版本規範**：
  - 版號升級至 v1.0.40，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.39] - 2026-08-02

### 🎯 版面溢出修復 + 離線行情清空 + 主副圖獨立 Overlay 趨勢符號 (↗/↘/→) + 副圖自訂參數 (v1.0.39)
- **版面橫向推擠溢出修復 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 精簡頂部 `lbl_hover_info` 為單行精美資訊，徹底解決過長文字把右側「1分/5分/日/週/月」按鈕擠出螢幕的問題。
- **未登入 API 時清空假 K 線 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py), [src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 未連線 API 時 (`not is_connected`) 嚴格保持主圖乾淨，不繪製任何雜亂擬真 K 線，並呈現「💡 尚未連線 API」連線提示。
- **主圖與副圖獨立左上角 Overlay 資訊列 + 趨勢斜率符號 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 主圖、副圖一、副圖二左上角分別建置專屬 Overlay 資訊標籤。
  - 即時計算並標註 `MA1~MA7` 均線與副圖指標相較於上一週期之斜率趨勢符號：**`↗` (上彎)**、**`↘` (下彎)**、**`→` (持平)**。
- **副圖技術指標自訂參數 ([src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py))**：
  - 於指標設定視窗新增副圖自訂參數專區，支援 MACD (12,26,9)、KDJ (9,3,3)、RSI (6,12,24)、Volume (5,10)、WR (14)、BIAS (6,12,24)、ATR (14)、CCI (14) 數字微調器。
  - 暗黑高科技對話視窗風格，貫徹淺色背景純黑色 (#000000) 高對比鐵律。
- **版本規範**：
  - 版號升級至 v1.0.39，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.38] - 2026-08-02

### 🎯 7 組均線 (SMA/EMA) + 布林通道雙層上下限 + 多副圖技術指標與調色盤選色系統 (v1.0.38)
- **資訊列均線顯示修復 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 修復 K 線懸停資訊列，依據各均線設定之專屬色彩（如金黃、白、青藍、粉紫等）即時動態輸出 `MA5` / `MA10` / `MA20` / `MA60` 等均線數值。
- **全新技術指標詳細設定視窗 ([src/widgets/indicator_settings_dialog.py](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py))**：
  - 新增 `IndicatorSettingsDialog` 設定對話視窗與 `ColorButton` 顏色調色盤選色器。
  - **主圖指標**: 支援 7 組移動平均線（可自訂 SMA / EMA、週期 1~1000、顏色、實線/虛線/點線/點劃線線型）以及布林通道 (Bollinger Bands - 中線與雙層 Upper1/Lower1/Upper2/Lower2 上下限)。
  - **副圖指標**: 支援 `成交量 (Volume)`、`MACD`、`KDJ`、`RSI`、`KD`、`WR (威廉指標)`、`BIAS (乖離率)`、`ATR (真實區間)`、`DMI (趨向指標)`、`CCI (順勢指標)` 之雙副圖自由切換。
- **全動態指標計算與繪圖引擎 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 全面升級 `NativeCandlestickChart` 指標引擎，支援 7 組均線與布林通道實時繪製，並完整輸出游標吸附處之所有指標數值。
- **版本規範**：
  - 版號升級至 v1.0.38，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.37] - 2026-08-02

### 🎯 頂部大盤三大指數 (加權指數 / 櫃買指數 / 台指期貨) 點擊切換主圖 K 線圖功能 (v1.0.37)
- **大盤 Banner 點擊互動 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 新增 `ClickableIndexBanner` 類別，為頂部「加權指數 (`IX0001`)」、「櫃買指數 (`IX0043`)」、「台指期貨 (`TX00`)」加入手勢指標與點擊事件。
  - 點擊三大指數 Banner 任何一區，即可立即切換主圖 K 線圖、均線、成交量與 MACD 指標至對應指數。
- **全動態 Fallback K 線渲染 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 擴充 `_generate_fallback_kbars` 支援 `IX0001` (43,119.75 點)、`IX0043` (347.85 點) 與 `TX00` (42,650.00 點) 之 K 線模擬，確保不論 API 連線或離線皆能順暢顯示高擬真 K 線圖。
- **版本規範**：
  - 版號升級至 v1.0.37，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.36] - 2026-08-02

### 🎯 跨 AI 模型 (Claude / GPT / Gemini 等) 無條件自動讀取與恪遵專案規則規範 (v1.0.36)
- **新增專案重點規則 Rule 21 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 不論切換或使用哪一個 AI 模型（包含 Claude、GPT、Gemini 等所有模型），開啟對話與執行任務時都必須自動讀取 `PROJECT_RULES.md` 專案重點規則，並無條件嚴格遵守專案所有 22 項規則。
- **版本規範**：
  - 版號升級至 v1.0.36，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.35] - 2026-08-02

### 🎯 下單帳戶預設虛擬帳號 + 左側面板欄寬自動伸縮 (v1.0.35)
- **下單帳戶預設為虛擬帳號 ([src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 啟動時下單帳戶 ComboBox 預設選擇「🟡 智慧模擬/虛擬交易帳戶 (Paper Trading)」，避免誤操作實盤帳戶。
- **左側面板欄寬全自動伸縮 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py), [src/widgets/five_bids_widget.py](file:///E:/SmartStock/src/widgets/five_bids_widget.py), [src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 自選股表格 4 欄 (代碼/名稱/成交價/漲跌幅) 全部改為 `QHeaderView.Stretch` 隨面板拉寬自動等比伸縮。
  - 五檔委買委賣表格 4 欄亦改為逐欄 `Stretch`，確保各欄隨面板寬度自動調整。
  - 下單工具欄 GridLayout 增加 `setColumnStretch`，輸入欄位隨面板寬度自適應。
- **版本規範**：
  - 版號升級至 v1.0.35，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.34] - 2026-08-01

### 🎯 全面導入 TAIFEX 官方期貨開盤參考價 (Reference Price) 漲跌計算引擎 (v1.0.34)
- **期貨開盤參考價 (Reference Price / Settlement Price) 引擎 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 感謝用戶專業指出！將原先誤用的 `收盤 - 開盤` 徹底廢除，更正為台灣期貨交易所 (TAIFEX) 官方標準：
    - **漲跌點數** = `最新成交價 - 開盤參考價 (Reference Price)`
    - **漲跌幅 (%)** = `(漲跌點數 / 開盤參考價) * 100%`
  - 台指期貨近月 (`TXFR1`)：前日結算參考價 `43,727.00` 點，當前價 `42,650.00` 點 ➔ 精確計算出 **`-1,077.00 點 (-2.46%)`**！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.33` 升級至 `v1.0.34`。

---

## [v1.0.33] - 2026-08-01

### 🎯 獨立防護 Snapshots 串流 & 登入後 100% 刷洗為 [全真實盤] (v1.0.33)
- 重構獨立防護 Snapshots 串流，連線後 100% 刷洗為 `[全真實盤]`，期貨鎖定 `TXFR1`。
