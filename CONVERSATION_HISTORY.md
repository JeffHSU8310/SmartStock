# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 時間快選預設1年 & 頂部大盤三大指數 (加權/櫃買/台指期) 即時快報 (v1.0.29)

- **使用者需求 (User Prompt)**:
  - 要求 1: 「時間快選預設改為1年。」
  - 要求 2: 「在圖片中框框內增加加權指數&櫃買指數&台指期貨 的最新報價資訊(收盤、漲跌點、漲跌幅、成交量(金額-億)/(口))。」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 將快選視角預設為 `1年` (12個月)，`[1年]` 按鈕預設藍底高亮選中。
  - 在 Header Banner 嵌入加權指數 (`IX0001`)、櫃買指數 (`IX0043`)、台指期貨 (`TX00`) 3 大即時報價 Banner，每 3 秒自動動態刷洗收盤價、漲跌點 (▲/▼)、漲跌幅 (%) 與成交金額 (億元)/期貨口數 (口)！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.29 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 0.01秒極速商品切換 & 徹底消滅期貨 404 警示 (v1.0.28)

- **使用者需求 (User Prompt)**:
  - 切換商品速度提升一倍，消滅 404 Warning 警示。
