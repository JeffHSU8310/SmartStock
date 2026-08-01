# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 切換商品 K線資訊重置修復、8大週期 Resample、MA趨勢箭頭與一字K厚度發布 v1.0.8 (v1.0.8)

- **使用者需求 (User Prompt)**:
  - 依最新截圖 6 大紅框批註與切換商品反饋：
    1. 切換商品時，主圖 K 線資訊徹底重置清空，避免殘留上一檔商品的數據。
    2. 預設切換至 `[日]` 週期，且 `[日]` 按鈕呈現高亮藍底。
    3. 頂部資訊欄加入 MA5 / MA20 均線數值與趨勢箭頭 (`⬆️` / `⬇️` / `➡️`)。
    4. 修復自選股表格價格錯誤問題與五檔現價同步。
    5. 實現 8 大週期 K 棒時間與價格重採樣 (Resample Engine)。
    6. 修復 `open == close` 一字/十字 K 棒視覺厚度與上下影線。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 在 `set_data` 徹底清空歷史陣列、重建 `DateAxisItem`，並為 `open == close` 一字/十字 K 棒賦予標準視覺厚度。
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 實作 8 大全週期 K 棒動態重採樣演算法 (Resampling Engine)。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 實作 8 大週期按鈕高亮狀態切換、頂部 MA 趨勢箭頭即時顯示與定時器自選股價格刷新。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.8 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 追加第 18 條交易安全規範 & 發布 v1.0.7 (v1.0.7)

- **使用者需求 (User Prompt)**:
  - 要求將此規定寫入規則中：「交易安全：所有測試與測試下單一律嚴格限定於 Shioaji 模擬環境 (`simulation=True`) 或模擬帳戶，確保絕無實盤金錢下單風險！」
