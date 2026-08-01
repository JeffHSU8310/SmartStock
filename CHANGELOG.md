# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

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
  - 點擊自選股觸發全局訊號，連動刷新 K 線、五檔報價與下單工具欄。
- **五檔即時報價欄 ([src/widgets/five_bids_widget.py](file:///E:/SmartStock/src/widgets/five_bids_widget.py))**：
  - 設計買一~買五與賣一~賣五即時檔位、內外盤價格與張數對照欄（放在主圖區左方）。
- **快捷下單工具欄 ([src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 設計商品代碼、委託價格、張數、ROD/IOC/FOK 類型選擇與亮紅買進/亮綠賣出下單按鈕（放在主圖區左方）。
- **主圖區與副圖區繪製 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 主圖區 (K線圖) 佔據最大視覺版面，支援紅綠 K 棒、MA5/MA20 均線與十字游標跟隨；副圖區 (技術指標) 緊臨主圖下方，繪製成交量柱狀圖與指標。
- **系統訊息日誌欄 ([src/widgets/message_console.py](file:///E:/SmartStock/src/widgets/message_console.py))**：
  - 置於副圖正下方，Terminal 風格即時輸出 Shioaji API 訂閱、成交回報與系統廣播訊息。
