# RuleShift｜規則變了，記憶跟上了嗎？

一個可重現的 Agent 研究世界：模型必須處理退貨、出貨與地址變更，操作會留下真實狀態；世界的規則則會在任務之間改變。評分同時檢查「決定是否正確」與「事情是否真的完成」。

[English](README.md) · [實驗協定](docs/PROTOCOL.md) · [職缺與研究定位](docs/CONTEXT.md) · [學習與延伸路線](docs/LEARNING.md)

這個專案把三項能力放在一起：可驗證的 Agent 系統工程、公平的實驗設計，以及能讓人看懂失敗原因的互動介面。它不是聊天機器人包裝，也不把參考解法的滿分當成模型能力。

[Live demo / 線上互動](https://f0909172434.github.io/ruleshift/) · [Release evidence / 完整證據](https://github.com/f0909172434/ruleshift/releases)

![RuleShift interactive rule and memory laboratory](docs/assets/overview.png)

## 目前具備什麼

- 三種任務、四種規則變動時程，跨任務持續保留訂單與庫存狀態。
- 五種記憶策略，共用同一固定權重小模型、工具與預算。
- 逐步紀錄提示、模型輸出、工具操作、成本與世界快照。
- 不依賴另一個模型打分；透過獨立規格檢查結果並重播驗證。
- 繁體中文工作台，同時呈現「當前世界」與「實際觀察過的記憶」。

首輪正式設計為 800 次任務執行。這是單模型、合成零售世界的先導研究；即使做完全部任務，也不足以推論真實產品或一般智能能力。

## 啟動

安裝 Python 3.12、uv、Node.js 22 以上，然後：

```sh
git clone https://github.com/f0909172434/ruleshift.git
cd ruleshift
uv sync --frozen --extra dev
npm ci --prefix web
npm run build --prefix web
uv run ruleshift serve --port 8765
```

打開 <http://127.0.0.1:8765>。先查詢規則、完成任務，再推進時間到第四個任務，觀察規則與記憶如何分離。「參考解法」只用於檢查模擬環境，不代表 AI 表現。

環境與介面不需要下載模型。若要執行真模型實驗，目前使用 Apple Silicon 的 MLX 後端：

```sh
uv sync --frozen --extra dev --extra mlx
uv run ruleshift benchmark --smoke --output artifacts/runs/my-smoke
uv run ruleshift benchmark --output artifacts/runs/my-test
```

首次會下載固定版本的公開 Qwen3 4B 量化模型。不使用付費 API。完整安裝、續跑、證據格式與限制請見 [REPRODUCING.md](docs/REPRODUCING.md)。

## 如何讓它成為自己的能力

先親手重現一個模型失敗，說清楚它究竟是舊規則、重複操作還是錯誤結案。接著在開發集提出一個有明確成本的新策略；凍結策略後，另建未看過的新測試集，公開成功與失敗。能解釋負面結果，比只展示漂亮成功案例更有說服力。

程式採 Apache-2.0；自製合成資料與發布的研究紀錄採 CC BY 4.0（第三方內容權利另計）。本專案與 DeepSeek 無隸屬關係。

## 正式測試結果

已完成並驗證 **800／800** 個任務，所有 113 次失敗均保留。
沿用記憶與選擇性更新同為 **153／160（95.625%）**；每次查證為 **132／160（82.5%）**。
選擇性更新比沿用記憶多用 47 次工具呼叫、37 次查詢嘗試，**這輪結果沒有證明新策略優於簡單方法**。

預定的選擇性更新－每次查證差值為 +13.125 個百分點，20 條配對任務串的 bootstrap 區間為 [7.5, 18.125]。
相同五個種子跨情境重用，獨立性有限；另附五個種子分組的敏感度分析 [4.375, 18.75]，不替換原定結果。

[完整解讀與限制](docs/RESULTS.md) · [所有策略與成本](evidence/test-v1/summary.csv) · [完整性驗證](evidence/test-v1/integrity.json)

正式資料可從 Release 下載並離線驗證。線上版提供可拖曳的教學示意與真模型回放；完整世界操作請使用本機服務。

**解讀限制：** 無效工具參數迴圈與成功後重複修改地址，明顯影響本輪分數；策略差值不能直接解釋成記憶適應能力。兩個模型的審查、修正與保留限制見 [審查紀錄](docs/REVIEW.md) 和 [完整結果](docs/RESULTS.md)。
