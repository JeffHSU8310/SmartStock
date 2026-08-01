# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 10年數據預設6個月視角、精準十字線吸附與 MACD 三層圖表重構 & 發布 v1.0.19 (v1.0.19)

- **使用者需求 (User Prompt)**:
  - 提供旗艦看盤圖表截圖，要求：對齊主副圖樣式 (增加 MACD)、滑鼠游標精準對上每根 K 棒、週/月K時間改為第一個交易日、拉開 K 棒間距、資料抓取拉大到 10 年且預設顯示 6 個月，並增加 5 大時間快選按鈕。
  - 提供台指期 404 Data Not Found 日誌，要求徹底解決台指期主圖空白問題。

- **系統處理與決策 (System Action & Decision)**:
  - 修復 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 期貨 90 天查詢上限（解決 404 Data Not Found 警示），股票支援 10 年數據，週/月K取當週/當月第一個交易日。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 重構三層圖表 (K棒+MA, Volume, MACD)，實作十字線 `round(x)` 精準吸附，`set_view_range_months` 快選縮放與 K 棒間距美化。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 加入 `6個月`/`1年`/`2年`/`5年`/`10年` 按鈕列，頂部對齊用戶截圖樣式。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.19 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 未登入前主圖保持乾淨空白，登入後載入全真數據 & 發布 v1.0.18 (v1.0.18)

- **使用者需求 (User Prompt)**:
  - 要求未登入前主圖保持空白，登入後選擇商品才載入正確 K 線。
