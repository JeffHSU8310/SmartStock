# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

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
- **C++ 核心算力引擎 ([src/core/](file:///E:/SmartStock/src/core/), [src/technical/](file:///E:/SmartStock/src/technical/), [src/strategy/](file:///E:/SmartStock/src/strategy/), [src/backtest/](file:///E:/SmartStock/src/backtest/))**：
  - 建立 C/C++ 高效數據結構 (`types.hpp`)。
  - 實現 C++ 技術指標算力 (MA5, MA20, RSI, MACD, KD) 與 K 線型態識別算法 (`indicators.cpp`)。
  - 實現 C++ 多維度 AI 量化選股器 (`robot_selector.cpp`) 與事件驅動歷史回測引擎 (`backtest_engine.cpp`)。
- **Python PySide6 原生 GUI 視窗與 K 線圖表 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py), [src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 使用 **PySide6 (Qt6 for Python)** 打造獨立原生 5 大面板 (看盤大廳、智慧選股雷達、C++ 回測儀表板、Shioaji 實盤下單、CA 憑證登入)。
  - 使用 **pyqtgraph** 原生 GPU/CPU 畫布繪製高幀率蠟燭 K 棒、均線、成交量與動態十字游標。
- **永豐金 Shioaji 券商 API 深入整合 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 整合 CA 憑證激活 (`activate_ca`)、即時行情 Snapshot、全週期 K線歷史下載與委託下單回報。

---
