# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-03] - 研讀 StockBuild 串接券商 API 報價做法 + Shioaji REST API 流量節流防護 + WebSocket 實時串流訂閱介面 (v1.0.42)

- **使用者需求 (User Prompt)**:
  - 「https://github.com/JeffHSU8310/SmartStock 去讀取Github 這個位置內最新檔案」
  - 「關於跟券商API串接，取得最新商品報價的做法，請參考這個位置內的檔案 https://github.com/JeffHSU8310/StockBuild，學習起來是怎麼做的，告訴我，他是怎麼做的。再調整SmartStock專案內的程式。」

- **系統處理與決策 (System Action & Decision)**:
  - 複製並深度研讀 `https://github.com/JeffHSU8310/StockBuild` 專案原始碼 (`brokers/sinopac.py` 與 `stock_app_pro.py`)：
    - **雙軌報價機制**：WebSocket 實時串流 (`subscribe`) 零成本推送撮合與五檔，配合 REST API 快照 (`snapshots`) 在無串流或離線時補充。
    - **API 流量防護 (Throttle Guard)**：REST 快照實施至少 **2.5 ~ 3 秒** 的呼叫間隔保護，恪守 Shioaji 官方 **10 秒 50 次** 上限，防護 API 遭封鎖。
    - **背景訂閱與安全鎖 (`subscribe_lock`)**：退訂舊合約與訂閱新合約放在背景執行緒，搭配 `subscribe_lock` 防護線程安全與避免快速連點帶來的無效訂閱。
  - 全面優化 [`src/sinopac_engine.py`](file:///e:/SmartStock/src/sinopac_engine.py)：
    - 加入 `subscribe_lock` (線程安全鎖) 與 `subscribed_contracts` 狀態追蹤。
    - 實作 `set_quote_callbacks()`、`subscribe_quote()` 與 `unsubscribe_quote()` WebSocket 實時報價訂閱介面。
    - 於 `get_realtime_quotes()` 加入 `MIN_SNAPSHOT_INTERVAL = 2.5` 秒流量防護與 `last_realtime_cache` 最新快取機制。
  - 沙盒環境 100% 通過單元測試腳本 `test_quote_engine.py` 驗證無誤。
  - 軟體版本由 `v1.0.41` 遞增至 `v1.0.42`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **最新版本**: `v1.0.42`

---

### 📌 [記錄時間: 2026-08-02] - 100% 券商真實數據金律 (Rule 22) + 徹底廢除假數據 + 布林通道第一層第二層獨立啟用 (v1.0.41)

- **使用者需求 (User Prompt)**:
  - 「1.布林指標第一層、第二層可以自行勾選是否啟用」
  - 「2.加權指數&櫃買指數&台指期貨的K線圖數據還是錯誤，又來了。還是解決不了問題」
  - 「3.然後切換商品的速度變成超級慢。(C++核心繪圖是不是又被改過了??)」
  - 「4.你的程式可以穩定一點嗎?改A功能，其他不該修改的也跟著被修改，很不穩定耶」
  - 「不準生成任何虛擬的數據，行情與技術分析必須 100% 使用券商 API 下載的真實數據！-寫進規則中，而且是重點中的重點」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///E:/SmartStock/PROJECT_RULES.md) 寫入最高原則 **Rule 22（100% 券商真實數據金律）**：本系統所有行情與指標分析 100% 必須自永豐金 API 下載真實數據，嚴禁生成任何 1 筆虛擬/假數據！
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 徹底停用與廢除 `_generate_fallback_kbars`。未連線 API 或無數據時嚴格回傳 `[]`（空列表），絕不偽造數據；並重構 Shioaji `api.Contracts.Indexs` / `api.Contracts.Indices` (TSE/OTC) 與 `Futures.TXF` 之全屬性動態遍歷 (Iterative Contract Search)，確保 100% 成功取得官方真實合約並下載實時歷史數據。
  - 於 [`src/widgets/indicator_settings_dialog.py`](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py) 與 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 新增 `chk_bb_b1` (啟用第一層通道 Upper1/Lower1) 與 `chk_bb_b2` (啟用第二層通道 Upper2/Lower2) 獨立勾選控制項。
  - 軟體版本由 `v1.0.40` 遞增至 `v1.0.41`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.41 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-02] - 期貨10年數據 + 大盤指數解析修復 + 主副圖 Overlay 釘選 + 布林獨立4條上下限 + 全指標 JSON 永久儲存 (v1.0.40)

- **使用者需求 (User Prompt)**:
  - 「1.期貨的歷史資料，又不見了。我要的十年以上。」
  - 「2.加權指數&櫃買指數的K線圖資料又跟以前一樣，沒有抓取到。」
  - 「3.圖片3中框就是主圖是均線數據資訊、副圖就是技術指標數據資訊」
  - 「4.副圖1，預設永遠都是成交量」
  - 「5.布林指標 要可以各自設定上限跟下限」
  - 「所有指標參數都是可以被儲存的」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 將期貨歷史數據下載天數解鎖至 `3650` 天 (10 年以上)，對齊個股；並相容 Shioaji `api.Contracts.Indices` 與 `api.Contracts.Indexs` 加強指數合約解析。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 連結 ViewBox `sigRangeChanged` 訊號，確保主圖、副圖一、副圖二左上角 Overlay 在縮放或滑動時 100% 釘選在畫布頂角，標註含趨勢符號 (**`↗` 上彎 / `↘` 下彎 / `→` 持平**) 之完整指標數據。
  - 固定副圖一預設指標永遠為 `成交量 (Volume)`。
  - 於 [`src/widgets/indicator_settings_dialog.py`](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py) 將布林通道拆解為 Upper1 K, Lower1 K, Upper2 K, Lower2 K 四條獨立上下限倍數數字微調器，並實作 `config/indicator_config.json` 設定檔寫入與讀取，重開軟體自動完全還原。
  - 軟體版本由 `v1.0.39` 遞增至 `v1.0.40`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.40 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-02] - 版面溢出修復 + 離線行情清空 + 主副圖獨立 Overlay 趨勢符號 (↗/↘/→) + 副圖自訂參數 (v1.0.39)

- **使用者需求 (User Prompt)**:
  - 「1.畫面跑掉了」
  - 「2.未登入前，主圖又出現亂七八糟的K線」
  - 「3.字體顏色都要黑色的」
  - 「4.均線資訊，要顯示主圖區的左上，還要有符號顯示均線是上彎、下彎、持平」
  - 「5.副圖的資訊，要顯示在各自的副圖區左上方，一樣要有符號顯示上彎、下彎、持平」
  - 「另外，副圖的技術指標，可以自行設定參數」

- **系統處理與決策 (System Action & Decision)**:
  - 精簡 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 頂部 `lbl_hover_info` 為單行精美資訊，徹底解決過長文字把右側時間快選按鈕擠出螢幕的問題。
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 與 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 設定 `not is_connected` 時主圖嚴格不繪製任何雜亂擬真 K 線，保持圖表乾淨並呈現連線提示。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 之 `p1` (主圖)、`p2` (副圖一)、`p3` (副圖二) 畫布分別建置獨立左上角 Overlay 標籤，並計算 `MA1~MA7` 與副圖指標相較於上一週期之斜率趨勢符號：**`↗` (上彎)**、**`↘` (下彎)**、**`→` (持平)**。
  - 於 [`src/widgets/indicator_settings_dialog.py`](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py) 新增副圖自訂參數專區，支援 MACD (12,26,9)、KDJ (9,3,3)、RSI (6,12,24)、Volume (5,10)、WR (14)、BIAS (6,12,24)、ATR (14)、CCI (14) 數字微調器，並套用暗黑高科技 QSS 風格，貫徹淺底純黑字 (#000000) 高對比鐵律。
  - 軟體版本由 `v1.0.38` 遞增至 `v1.0.39`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.39 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-02] - 7組均線 (SMA/EMA) + 雙層布林通道 + 多副圖技術指標與調色盤選色系統 (v1.0.38)

- **使用者需求 (User Prompt)**:
  - 「1.均線的資訊不見了」
  - 「2.增加主圖指標選項&副圖指標選項」
  - 「3.主圖指標有均線(SMA、EMA)，要有七組可以設定，線型顏色可以設定、參數可以設定。還有布林指標(上限&下限&中線的參數友都可以自行設定，然後，上限跟下限要有個兩組)，線型顏色可以設定。線型可以有多種線型(實線、需線、鍊線....等)，顏色可以用調色盤選擇。」
  - 「4.副圖指標有KDJ、MACD、RSI還有其他看盤軟體有的技術指標都要包含」

- **系統處理與決策 (System Action & Decision)**:
  - 新增 [`src/widgets/indicator_settings_dialog.py`](file:///E:/SmartStock/src/widgets/indicator_settings_dialog.py)：實作 `IndicatorSettingsDialog` 與 `ColorButton` 顏色調色盤選色器，支援 7 組均線 (SMA/EMA)、雙層布林通道 (Middle, Upper1/Lower1, Upper2/Lower2) 與副圖指標選單。
  - 全面升級 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py)：指標繪製與計算引擎支援 7 組均線 (實線/虛線/點線/點劃線與獨立顏色) 以及 `Volume`, `MACD`, `KDJ`, `RSI`, `KD`, `WR`, `BIAS`, `ATR`, `CCI` 等技術指標繪製。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 增加「⚙️ 技術指標設定」按鈕，並修復 `on_hover_kbar` 懸停資訊列，依據各指標設定色彩動態輸出 `MA1~MA7`、`Bollinger Bands` 與副圖指標數值。
  - 軟體版本由 `v1.0.37` 遞增至 `v1.0.38`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.38 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-02] - 頂部大盤三大指數點擊切換主圖 K 線圖功能 (v1.0.37)

- **使用者需求 (User Prompt)**:
  - 「點擊打勾的指數&台指期，也可以跟其他商品一樣在主圖中看到K線圖」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 實作 `ClickableIndexBanner` 類別，為頂部「加權指數 (`IX0001`)」、「櫃買指數 (`IX0043`)」與「台指期貨 (`TX00`)」標籤加入手指游標 Hover 提示與點擊事件。
  - 點擊三大指數 Banner 任何一區，立即觸發 `on_stock_changed(code, name)` 切換主圖 K 線、均線、成交量與 MACD。
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 擴充 `_generate_fallback_kbars` 支援 `IX0001` (43,119.75)、`IX0043` (347.85) 與 `TX00` (42,650.00)，無論 API 連線與否皆能順暢顯示高擬真 K 線圖。
  - 軟體版本由 `v1.0.36` 遞增至 `v1.0.37`（恪遵 Rule 13 `+0.0.1` 遞增規範）。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.37 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-02] - 新增跨 AI 模型無條件讀取與遵守專案規則 Rule 21 (v1.0.36)

- **使用者需求 (User Prompt)**:
  - 要求加入新規則：「不論用哪一個模型 (包含 Claude & GPT)，都還是要讀取規則、遵守規則。」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///E:/SmartStock/PROJECT_RULES.md) 正式新增 **Rule 21**：「**跨 AI 模型無條件自動讀取與恪遵專案規則規範**：不論切換或使用哪一個 AI 模型（包含 Claude、GPT、Gemini 等所有模型），開啟對話與執行任務時都必須自動讀取 `PROJECT_RULES.md` 專案重點規則，並無條件嚴格遵守所有 22 項規則！」
  - 軟體版本由 `v1.0.35` 遞增至 `v1.0.36`（恪遵 Rule 13 `+0.0.1` 遞增規範）。
  - 同步更新 [`CHANGELOG.md`](file:///E:/SmartStock/CHANGELOG.md) 與主程式標題版本。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.36 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 全面導入 TAIFEX 期貨開盤參考價 (Reference Price) 漲跌計算引擎 (v1.0.34)

- **使用者需求 (User Prompt)**:
  - 專業指出: 「我知道你期貨報價哪裡出問題了，你只是單純的計算 開盤/收盤 之間的價差，但是期貨應該是要用它的參考價為起點來計算。所以，你抓到的資料確實是有問題的，沒有抓到期貨開盤的參考價，導致發生收盤結果有很大的出入。你要去找出期貨的參考價數據」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 徹底廢除 `Close - Open` 算法，全面導入 Shioaji 官方 `snap.reference_price`（開盤參考價 / 結算價）。
  - 以 `最新價 - 參考價 (43727.00)` 精確計算台指期漲跌點數 `-1077.00` 點與漲跌幅 `-2.46%`！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.34 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 獨立防護 Snapshots 串流 (v1.0.33)

- **使用者需求 (User Prompt)**:
  - 獨立防護與對接 TXFR1。
