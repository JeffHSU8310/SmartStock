# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 實作 1:1 K棒留白間隔 & 修復時間快選按鈕 & 發布 v1.0.23 (v1.0.23)

- **使用者需求 (User Prompt)**:
  - 要求：「K棒與K棒之間的間隔，再拉開要有一根K棒的距離。時間快選無作用。」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 設定 K 棒半寬 `w = 0.25`（實體 0.5 + 留白 0.5 ➔ 間隔精確等於一根 K 棒的寬度！）。
  - 修復 `set_view_range_months`：移除強行覆蓋 X 軸的 `autoRange()` 呼叫，點擊 `6個月`/`1年`/`2年`/`5年`/`10年` 按鈕 100% 精確生效！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.23 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 徹底根除台指期混入台積電舊數據 Bug & 發布 v1.0.22 (v1.0.22)

- **使用者需求 (User Prompt)**:
  - 要求根除台指期混入台積電 544 元舊數據問題。
