# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v6.0.0] - 2026-07-31

### 永豐金證券 Shioaji API 雙引擎整合發布 (SinoPac Shioaji API Integration)
- **實作 Python SinoPac Shioaji SDK 模組 ([sinopac_engine.py](file:///e:/Rot/src/sinopac_engine.py))**：
  - 成功安裝並整合 `shioaji` Python SDK (v1.7.1)。
  - 支援模擬環境測試與真實 API 登入、合約查詢 (TWSE/TPEx/TAIFEX) 與 Tick/KBar 實時報價訂閱。
- **實作 C++ SinoPac Shioaji 核心算力適配器 ([sinopac_cxx_bridge.hpp](file:///e:/Rot/src/data/sinopac_cxx_bridge.hpp))**：
  - 為 C++ 核心引擎提供高效能低延遲的報價資料流結構。
- **雙引擎發布封裝 (v6.0.0 Release)**：
  - 打包發布獨立執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe) 與綠色封裝包 [`TaiwanSmartQuant_v6.0_SinoPac_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v6.0_SinoPac_Standalone.zip)。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v5.0.0] - 2026-07-31

### 五大全彩版面與 C++/Python 雙引擎重構發布 (Five Rich-Color Layout Tabs Release)
- 全新重構五大功能版面，發布獨立桌面軟體 `TaiwanSmartQuant_GUI.exe`。
