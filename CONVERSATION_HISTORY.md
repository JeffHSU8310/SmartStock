# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

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
