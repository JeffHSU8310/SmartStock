# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 永豐金 Shioaji API 實盤登入與 CA 憑證驗證視窗 (v6.0.5)

- **使用者需求 (User Prompt)**:
  - 要求設計可以填入相關資料的視窗功能（包含身分證字號、API Key、Secret Key、.pfx 憑證檔案路徑、憑證密碼，以及「驗證憑證並連線」按鈕），100% 配對使用者提供之視窗截圖設計。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`gui/index.html`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/gui/index.html) 與 [`gui/style.css`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/gui/style.css) 新增 Modal 彈窗與亮橘核心按鈕，完全符合圖片佈局與主題暗灰質感。
  - 於 [`src/sinopac_engine.py`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/src/sinopac_engine.py) 實作 `login_with_ca` 方法，綁定永豐金 `api.login()` 與 `api.activate_ca()`。
  - 於 [`src/gui_host.py`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/src/gui_host.py) 與 [`gui/app.js`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/gui/app.js) 實作 `ApiBridge` 非同步傳輸與原生檔案選擇器 (File Dialog)。
  - 更新 [`CHANGELOG.md`](file:///C:/Users/jeffn/.gemini/antigravity/worktrees/Rot/fix_rot_repository_issues/CHANGELOG.md) 至 `v6.0.5` (恪遵 Rule 13 `+0.0.1` 遞增)。
  - 執行 Git Commit 並全數自動 Push 同步至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v6.0.5 (永豐金 API 憑證登入視窗完成)
  - **下一步選擇**: 【智慧選股雷達】/【C++ 回測儀表板】/【消息面重訊】/【數據 CRUD & Telegram】
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 修正第一步：【看盤大廳與即時報價】永豐金 Shioaji 雙引擎強化 (v6.0.4)

- **使用者需求 (User Prompt)**:
  - 開始一步一步修正功能，並選擇優先修正「【看盤大廳與即時報價】串接永豐金 Shioaji 實時股票/期貨 Tick 與全週期 K線圖報價」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/data/sinopac_cxx_bridge.hpp`](file:///e:/Rot/src/data/sinopac_cxx_bridge.hpp) 強化 C++ 型態識別演算法 (看漲吞噬、錘子強撐、長紅突破)。
  - 於 [`src/sinopac_engine.py`](file:///e:/Rot/src/sinopac_engine.py) 與 [`gui/app.js`](file:///e:/Rot/gui/app.js) 實作全週期切換 (日K / 60分K / 5分K) 與台股亮紅/亮綠即時動態行情。
  - 編譯驗證 C++ 核心與打包獨立 GUI 執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v6.0.4` (恪遵 Rule 13 `+0.0.1` 遞增)。
  - 執行 Git Commit 並全數自動 Push 同步至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v6.0.4 (看盤大廳與即時報價強化完成)
  - **下一步選擇**: 【智慧選股雷達】/【C++ 回測儀表板】/【消息面重訊】/【數據 CRUD & Telegram】
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 追加規則 14：永豐金 Shioaji 官方全庫文檔研讀與實作規範 (v6.0.3)

- **使用者需求 (User Prompt)**:
  - 要求學習永豐金 Shioaji 官方文檔，並將研讀規範寫入規則。
