# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 未登入前主圖保持乾淨空白，登入後載入全真數據 & 發布 v1.0.18 (v1.0.18)

- **使用者需求 (User Prompt)**:
  - 反饋：「尚未登入的主線圖是這個鬼樣子。還沒有登入前，主圖就空白，登入後，選擇商品，主圖就顯示出正確的K線圖。有沒有問題?」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 設定未登入時 `get_kbars` 直接回傳 `[]`。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 設定未登入時呈現深色乾淨空白畫布與引導提示；登入成功後向伺服器請求全真實 3 年數據與精確 K 線。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.18 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 實作官方中文名稱動態解析器 & 發布 v1.0.17 (v1.0.17)

- **使用者需求 (User Prompt)**:
  - 要求輸入股票代號正確顯示名稱。
