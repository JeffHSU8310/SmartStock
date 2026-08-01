# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.0] - 2026-08-01

### 🚀 SmartStock 全新量化交易與選股平台歸零重啟 (Pure Native Qt6 Architecture)
- **架構重構與規範定案**：
  - 恪遵 18 項最新重點規則 (Rule 0~17)，徹底捨棄 Web/HTML 網頁架構，採用 **100% C++ / Python / C / C# 原生技術**。
  - 指定 GitHub 儲存庫同步至 `https://github.com/JeffHSU8310/SmartStock.git`。
- **C++ 核心算力引擎 ([src/core/](file:///e:/Rot/src/core/), [src/technical/](file:///e:/Rot/src/technical/), [src/strategy/](file:///e:/Rot/src/strategy/), [src/backtest/](file:///e:/Rot/src/backtest/))**：
  - 建立 C/C++ 高效數據結構 (`types.hpp`)。
  - 實現 C++ 技術指標算力 (MA5, MA20, RSI, MACD, KD) 與 K 線型態識別算法 (`indicators.cpp`)。
  - 實現 C++ 多維度 AI 量化選股器 (`robot_selector.cpp`) 與事件驅動歷史回測引擎 (`backtest_engine.cpp`)。
- **Python PySide6 原生 GUI 視窗與 K 線圖表 ([src/gui_host_qt.py](file:///e:/Rot/src/gui_host_qt.py), [src/widgets/candlestick_chart.py](file:///e:/Rot/src/widgets/candlestick_chart.py))**：
  - 使用 **PySide6 (Qt6 for Python)** 打造獨立原生 5 大面板 (看盤大廳、智慧選股雷達、C++ 回測儀表板、Shioaji 實盤下單、CA 憑證登入)。
  - 使用 **pyqtgraph** 原生 GPU/CPU 畫布繪製高幀率蠟燭 K 棒、均線、成交量與動態十字游標。
- **永豐金 Shioaji 券商 API 深入整合 ([src/sinopac_engine.py](file:///e:/Rot/src/sinopac_engine.py))**：
  - 整合 CA 憑證激活 (`activate_ca`)、即時行情 Snapshot、全週期 K線歷史下載與委託下單回報。

---
