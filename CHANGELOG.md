# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v6.0.5] - 2026-07-31

### 券商 API 登入與 CA 憑證驗證視窗 (SinoPac Shioaji API Real-Account Auth Modal)
- **前端 GUI 原生 Modal 設計 ([gui/index.html](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/gui/index.html), [gui/style.css](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/gui/style.css))**：
  - 設計「登入永豐金實盤 API (含憑證)」彈出式視窗，包含身分證字號、API Key、Secret Key、.pfx 憑證路徑（支援原生檔案總管選擇器）與憑證密碼。
  - 介面細緻配對暗灰沉浸風格與高彩亮橘 **【驗證憑證並連線】** 核心按鈕。
  - 頂部 Navigation Header 新增實盤連線狀態標籤（🔴 未連線 / 🟢 實盤已連線 / 🟡 模擬模式）。
- **Python 後端憑證激活雙引擎 ([src/sinopac_engine.py](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/src/sinopac_engine.py), [src/gui_host.py](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/src/gui_host.py))**：
  - 新增 `login_with_ca` 方法，整合 Shioaji API `login()` 與 `activate_ca()`。
  - 透過 `ApiBridge` 實現 pywebview 與 JavaScript 雙向非同步數據交會。

### 備註 (Notes)
- 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，已 Commit 並自動同步至 **origin/main**。

---

## [v6.0.4] - 2026-07-31

### 修正第一步：【看盤大廳與即時報價】永豐金 Shioaji 雙引擎強化 (Step 1 Market Quote Refinement)
- **C++ 核心算力強化 ([sinopac_cxx_bridge.hpp](file:///e:/Rot/src/data/sinopac_cxx_bridge.hpp))**：
  - 增強 K線型態識別算力（看漲吞噬 Bullish Engulfing、錘子強撐 Hammer Support、長紅突破 Long Bullish）。
- **Python 報價與全週期切換 ([sinopac_engine.py](file:///e:/Rot/src/sinopac_engine.py), [gui/app.js](file:///e:/Rot/gui/app.js))**：
  - 支援看盤大廳動態切換 **日K / 60分K / 5分K**，同步動態計算 MA5 與 MA20 均線柱狀圖。
  - 上市、上櫃與台指期貨實時報價漲跌高亮（亮紅 `#FF3B69` / 亮綠 `#00E676`）與點擊切換。
- **發布獨立執行檔**：
  - 重新打包獨立 GUI 執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe)。

### 備註 (Notes)
- 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，已 Commit 並自動同步至 **origin/main**。

---

## [v6.0.3] - 2026-07-31

### 規則 14 追加 (永豐金 Shioaji 官方文檔全庫研讀與實作規範)
- 寫入規則 14 於 `PROJECT_RULES.md`。

---

## [v6.0.2] - 2026-07-31

### 規則 13 細化 (累積至 0.0.99 再進位至 0.1.0 規範)
- 細化規則 13 於 `PROJECT_RULES.md`。
