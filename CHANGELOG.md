# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.5] - 2026-08-01

### 🚀 永豐金 API 全真行情對接、K線切換修復、登入 Modal 與帳戶切換
- **圖片 1 提示彈窗文字高對比度修復 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 獨立客製化 `QMessageBox` 與 `QDialog` QSS 主題，採用高質感深灰背景 (`#16191E`) 與純白字體 (`#FFFFFF`)，徹底解決對比度看不清問題。
- **圖片 2 右上角登入/登出動態按鈕與憑證 Modal 整合 ([src/widgets/auth_dialog.py](file:///E:/SmartStock/src/widgets/auth_dialog.py), [src/utils/config_manager.py](file:///E:/SmartStock/src/utils/config_manager.py))**：
  - **移除獨立「⚙️ 憑證與系統設定」分頁**。
  - 右上角改為動態連線狀態按鈕：未登入時點擊彈出原生 **CA 憑證登入 Modal (`AuthDialog`)**；Modal 內新增 **【☑️ 記憶 API Key 與憑證設定】** 勾選框，加密保存於 `config.json`（已加入 `.gitignore`，恪遵 Rule 10）。
  - 登入成功後按鈕自動變為 **【🔴 永豐金實盤 (點擊登出)】**，點擊即可一鍵登出。
- **圖片 3 快捷下單「實盤 / 模擬帳戶選擇」整合 ([src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - **移除獨立「💼 Shioaji 實盤下單」分頁**，介面精簡為 3 大核心頁籤 (看盤大廳、智慧選股雷達、C++ 回測儀表板)。
  - 下單欄新增 **【帳戶選擇 (SinoPac 實盤帳戶 vs 模擬/虛擬交易帳戶)】** 下拉選單。
- **全真報價對接與商品點擊切換 K線修復 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 全面貫通永豐金官方 `api.snapshots()` 快照與 `api.kbars()` 真實 K 棒獲取。
  - 點擊自選股商品（台積電 2330、鴻海 2317、聯發科 2454、0050 等）時，主圖 K 線圖、副圖成交量、五檔報價與價格 100% 動態連動刷新。
  - 加入 `QTimer` 3 秒定時器持續刷新最新行情。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.4` 升級至 `v1.0.5`。

---

## [v1.0.4] - 2026-08-01

### 🐛 修復 Python 模組載入路徑與動態相容性 (Fix ModuleNotFoundError in Direct Script Launch)
- **路徑解析修復 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 在入口檔案頂端動態導入 `root_dir` 至 `sys.path`，修復當使用者在 CLI / PowerShell 執行 `python src/gui_host_qt.py` 時產生的 `ModuleNotFoundError: No module named 'src'` 錯誤。
  - 加入雙層安全 import 回退機制，確保不論在專案根目錄或子目錄中執行均 100% 順暢啟動。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.3` 升級至 `v1.0.4`。

---

## [v1.0.3] - 2026-08-01

### 📊 【看盤大廳 (Market Overview)】五大原生 UI 版面重構
- **自選股管理元件 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py))**：
  - 設計自選股管理清單（放在主圖區左方），支援新增 `QLineEdit`+`➕`、刪除 `🗑️` 選定自選、`⬆️` 上移與 `⬇️` 下移調整排序。
