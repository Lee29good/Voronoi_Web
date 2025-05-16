
# 🧭 Voronoi_Web 專案說明文件

本專案為一套以 Python 開發、可視化 Voronoi Diagram 的互動式圖形系統，支援從滑鼠點擊、檔案讀取、步驟執行等方式構建 Voronoi 圖。包含完整 GUI 操作介面與 Divide-and-Conquer 演算法，支援結果輸出及視覺化分析。

---

## 📌 基本資訊

- 🧑‍💻 開發者：李明儒 (M133040055)
- 🧪 所屬單位：中山大學 資工所碩一
- 🛠 開發語言：Python 3.12.7
- 📁 可執行版本支援 Windows（Mac 使用者可用原始碼手動打包）
- 🔗 GitHub: [Voronoi Diagram Repo](https://github.com/Lee29good/Voronoi-diagram)
- 頁面瀏覽: https://lee29good.github.io/Voronoi_Web/M133040055_Introduction.html
  - 簡介
  - 軟體規格書
  - 軟體說明
  - 程式設計
  - 軟體測試與實驗結果
  - 結論與心得
  - 附錄

---

## 🧮 功能特色

- 點擊畫布建立種子點
- 自訂座標、新增指定數量的隨機點
- 支援完整步驟拆解：包含畫左半邊 Voronoi → 右半邊 → 合併圖
- Divide and Conquer 演算法進行快速區域劃分
- 可讀取 / 輸出 `.txt` 格式的點與邊資訊
- 實驗結果圖像化展示最多支援 100 點運算

---

## 🖼 軟體介面

- 畫布大小：600 x 600 px
- 主要控制項：
  - 添加點（滑鼠 / 手動輸入 / 隨機）
  - 執行（一次性執行 / 一步一步執行 / 顯示下一組資料）
  - 輸入 / 輸出文字檔
  - 畫面清除

---

## 📂 專案結構建議

```
Voronoi_Web/
├── Voronoi.py                # 主演算法與 GUI 程式入口
├── input.txt                 # 測試點資料
├── output.txt                # 執行輸出結果
├── requirements.txt          # Python 套件依賴
├── M133040055_Introduction.html # 專案完整說明 HTML
├── styles.css                # (選擇性) UI 美化樣式
├── assets/ 或 Picture/        # 各種圖片資源
└── README.md
```

---

## 📥 安裝與執行方式

### 1️⃣ 建立虛擬環境（建議）

```bash
python3 -m venv venv
source venv/bin/activate  # Windows 請使用 venv\Scripts\activate
```

### 2️⃣ 安裝依賴套件

```bash
pip install -r requirements.txt
```

> `tkinter`, `math`, `random` 為標準庫，不需額外安裝。

### 3️⃣ 執行主程式

```bash
python3 Voronoi.py
```

---

## 📦 requirements.txt 套件清單

```
numpy
pandas
matplotlib
```

---

## 🧪 測試案例與結果

- 2 點 → 中垂線構成
- 3 點 → 外心與中垂線
- 4~6 點 → 分割與合併處理
- >7 點 → 使用 Divide and Conquer 實作

🎯 最終結果支援到 100 點且可正確運算出完整 Voronoi 區域圖。

---

## 🧠 核心演算法模組

- `Voronoi Class`：儲存所有點與邊
- `ConvexHull()`：Jarvis March 求解
- `Merge()`、`HyperPlane()`：雙圖合併與中垂線追蹤
- `FindCommonTangent()`：找出上、下公切線
- `FindIntersection()`：向量交點計算

---

## 📜 結語與心得

本專案融合幾何演算法、圖形化 UI、檔案 I/O、資料結構與視覺化，完成了一個完整且可互動的 Voronoi Diagram 平台，適用於教學、研究與展示用途。感謝所有實驗過程中協助與 debug 的夥伴。

---

## 🔖 聯絡方式

- 📬 Email: Lee910404@google.com
- 🏫 所屬單位: 國立中山大學 資工所
- 📞 電話: +666 666 6666
