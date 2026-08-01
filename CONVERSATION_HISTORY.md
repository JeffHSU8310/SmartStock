# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 全真字典對接、8大週期切換、K棒懸停高亮與 DateAxis 發布 v1.0.6 (v1.0.6)

- **使用者需求 (User Prompt)**:
  - 依上傳圖片批註指導：
    1. 自選股「價格錯誤」修復。
    2. K 線圖頂部 8 大全週期按鈕：`[1分]` `[5分]` `[15分]` `[30分]` `[60分]` `[日]` `[週]` `[月]`。
    3. 滑鼠游標移到某根 K 線，就顯示該根股價資訊/漲跌點/漲跌幅/成交量。
    4. K 線與副圖底部 X 軸要顯示真實日期時間。
    5. 下單欄下拉選單 QSS 字體顏色改為黑色/高對比白字。
    6. 正確從永豐金證券網站對接 Shioaji 官方商品字典與報價。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 對接永豐金 Shioaji 官方 `api.Contracts.Stocks/Futures/Indices` 字典與 `api.snapshots()` 快照。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 實作 `DateAxisItem` 與游標懸停 K 棒 Listener (`hover_kbar_signal`)。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 實現 8 大全週期切換、頂部懸停高亮欄與 `QComboBox` 高對比黑底白字樣式。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.6 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 全真報價對接、K線切換修復、登入 Modal 與帳戶切換發布 v1.0.5 (v1.0.5)

- **使用者需求 (User Prompt)**:
  - 圖片 1：提示彈窗字體顏色改為高對比白字。
  - 圖片 2：右上角登入/登出動態切換按鈕，點擊彈出憑證登入 Modal。
