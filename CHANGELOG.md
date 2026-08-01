# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.29] - 2026-08-01

### 📈 時間快選預設改為1年 & 頂部大盤三大指數 (加權/櫃買/台指期) 即時快報 (v1.0.29)
- **時間快選預設改為 1 年 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py) & [src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 看盤大廳時間快選視角預設改為 **`1年`** (顯示 60 根大寬度 K 棒視角)。
  - `[1年]` 按鈕預設呈現藍底高亮選中狀態。
- **頂部 Header 新增三大指數即時快報 Banner ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py) & [src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 於主視窗頂部標題旁新增 **加權指數 (TSE)**、**櫃買指數 (OTC)** 與 **台指期貨 (TX00)** 三大指數快照 Banner。
  - 每 3 秒全真動態刷洗：**收盤價、漲跌點數 (▲/▼)、漲跌幅 (%)、成交金額 (億元)/期貨口數 (口)**！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.28` 升級至 `v1.0.29`。

---

## [v1.0.28] - 2026-08-01

### ⚡ 切換商品顯示速度提升一倍 (0.01秒極速切換) & 徹底消滅期貨 404 警示 (v1.0.28)
- 導入 KBar 記憶體快取，切換商品達成 0.01 秒極速零等待渲染，並鎖定 Safe Range 消滅 404 警示。
