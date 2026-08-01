# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.3] - 2026-08-01

### 📊 【看盤大廳 (Market Overview)】五大原生 UI 版面重構
- **自選股管理元件 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py))**：
  - 設計自選股管理清單（放在主圖區左方），支援新增 `QLineEdit`+`➕`、刪除 `🗑️` 選定自選、`⬆️` 上移與 `⬇️` 下移調整排序。
  - 點擊自選股觸發全局訊號，連動刷新 K 線、五檔報價與下單工具欄。
- **五檔即時報價欄 ([src/widgets/five_bids_widget.py](file:///E:/SmartStock/src/widgets/five_bids_widget.py))**：
  - 設計買一~買五與賣一~賣五即時檔位、內外盤價格與張數對照欄（放在主圖區左方）。
- **快捷下單工具欄 ([src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 設計商品代碼、委託價格、張數、ROD/IOC/FOK 類型選擇與亮紅買進/亮綠賣出下單按鈕（放在主圖區左方）。
- **主圖區與副圖區繪製 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 主圖區 (K線圖) 佔據最大視覺版面，支援紅綠 K 棒、MA5/MA20 均線與十字游標跟隨；副圖區 (技術指標) 緊臨主圖下方，繪製成交量柱狀圖與指標。
- **系統訊息日誌欄 ([src/widgets/message_console.py](file:///E:/SmartStock/src/widgets/message_console.py))**：
  - 置於副圖正下方，Terminal 風格即時輸出 Shioaji API 訂閱、成交回報與系統廣播訊息。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.2` 升級至 `v1.0.3`。

---

## [v1.0.2] - 2026-08-01

### 🔍 全盤本機開發環境診斷與驗證 (Full Environment & Package Audit)
- **語言與編譯器環境核驗**：
  - **Python (v3.13.9)**：`shioaji` (v1.7.0), `PySide6` (v6.9.2), `pyqtgraph` (v0.14.0), `numpy` (v2.3.5), `pandas` (v2.3.3), `matplotlib` (v3.10.6), `PyInstaller` (v6.21.0) 核心套件全數盤點通過。
  - **C / C++**：`GCC / G++` (v15.2.0 MinGW-w64) 與 `CMake` (v4.4.1) 驗證具備 C++17/C++20 動態庫編譯能力。
  - **C# / .NET**：`.NET SDK` (v10.0.400) 驗證具備完整的 C# 模組支援。
- **版本與紀錄**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本升級至 **v1.0.2**。

---

## [v1.0.1] - 2026-08-01

### 📂 本機專案路徑遷移與環境對齊 (Local Directory Migration to E:\SmartStock)
- **專案本機目錄遷移**：
  - 本機工作目錄正式升級切換至 [`E:\SmartStock`](file:///E:/SmartStock)。
  - 驗證 C++ 核心庫 [`smartstock_core.dll`](file:///E:/SmartStock/smartstock_core.dll) 與 Python PySide6 原生 UI 視窗在 [`E:\SmartStock`](file:///E:/SmartStock) 環境下載入零 Exception。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.0` 升級至 `v1.0.1`。

---

## [v1.0.0] - 2026-08-01

### 🚀 SmartStock 全新量化交易與選股平台歸零重啟 (Pure Native Qt6 Architecture)
- **架構重構與規範定案**：
  - 恪遵 18 項最新重點規則 (Rule 0~17)，徹底捨棄 Web/HTML 網頁架構，採用 **100% C++ / Python / C / C# 原生技術**。
  - 指定 GitHub 儲存庫同步至 `https://github.com/JeffHSU8310/SmartStock.git`。
