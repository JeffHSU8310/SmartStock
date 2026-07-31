# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v6.0.2] - 2026-07-31

### 規則 13 細化 (累積至 0.0.99 再進位至 0.1.0 規範)
- **細化規則 13 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md)**：
  - **規範內容**：**每次修改之版本號變更，必須嚴格依照 `+0.0.1` 遞增（如 v6.0.1 ➔ v6.0.2）；當小版號累積至 `0.0.99` 時，再進位至 `0.1.0`（如 v6.0.99 ➔ v6.1.0）**。
- **儲存庫與對話歷史同步**：
  - 更新 [`CONVERSATION_HISTORY.md`](file:///e:/Rot/CONVERSATION_HISTORY.md) 紀錄規則 13 進位細化。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v6.0.1] - 2026-07-31

### 規則 13 追加 (版本號遞增規範 +0.0.1)
- 寫入規則 13 於 `PROJECT_RULES.md`。

---

## [v6.0.0] - 2026-07-31

### 永豐金證券 Shioaji API 雙引擎整合發布 (SinoPac Shioaji API Integration)
- 實作 Python SinoPac Shioaji SDK 模組與 C++ SinoPac Shioaji 核心算力適配器。
