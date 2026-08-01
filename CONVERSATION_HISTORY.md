# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 台指期10年全歷史補齊 & 群組管理 & 週一日期 & Vertical QSplitter (v1.0.25)

- **使用者需求 (User Prompt)**:
  - 要求 1: 「週K時間不對，應該是7/27才對。」
  - 要求 2: 「系統廣播欄位高度預設減半，可用卷軸上下滾動，欄位可以上下調整；主副圖欄位也可以上下調整。」
  - 要求 3: 「台指期貨資料要有10年以上歷史數據，否則無法回測。」
  - 要求 4: 「自選股要增加群組功能，群組可以自定名稱，也可以修改/刪除。」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 提供台指期 (TX00) 10 年全歷史 (2500 筆) K 棒，並修正週 K 時間戳算法為週一日期 (如 2026-07-27)。
  - 於 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 實作多群組下拉選單與 ⚙️ 管理選單 (新增/重命名/刪除)。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 與 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 導入 Native `QSplitter(QtCore.Qt.Vertical)` 垂直分割器，訊息欄預設減半且可上下拖拉調整，主圖/成交量/MACD 三層圖表亦可上下拖拉調整。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.25 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 修復成交量矩形牆與斜線對角殘影 Bug & 發布 v1.0.24 (v1.0.24)

- **使用者需求 (User Prompt)**:
  - 反饋成交量繪製混亂，修復為自 0 起算並消滅畫布斜線殘影。
