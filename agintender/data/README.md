# danny · agintender（@agintender）开源数据目录说明

> 本目录收录 **2,519** 篇经语义分类与复核的本人原创推文（精选 S/A 干货 **1,221** 篇），按 **7 大板块 · 20 个自然小节** 互斥归档，JSON 与 UTF-8-SIG CSV 100% 一一对应。

## 主表文件
- [`agintender_tweets.json`](agintender_tweets.json) / [`agintender_tweets.csv`](agintender_tweets.csv)：全量分类推文（2,519 篇）
- [`agintender_featured.json`](agintender_featured.json) / [`agintender_featured.csv`](agintender_featured.csv)：S/A 级精选干货（1,221 篇）
- [`agintender_mental_models.json`](agintender_mental_models.json) / [`agintender_mental_models.csv`](agintender_mental_models.csv)：核心原话与思维模型（6 条）
- [`ai_rag_index.json`](ai_rag_index.json)：本地全量 RAG 检索索引

## 分板块切片（`domains/`）
- `01` **永续合约与清算算法**（190 篇）：[`domains/01_perp_contract_mechanics.json`](domains/01_perp_contract_mechanics.json) · [`domains/01_perp_contract_mechanics.csv`](domains/01_perp_contract_mechanics.csv)
- `02` **美股 Perp 与衍生品创新**（265 篇）：[`domains/02_stock_perps_derivatives.json`](domains/02_stock_perps_derivatives.json) · [`domains/02_stock_perps_derivatives.csv`](domains/02_stock_perps_derivatives.csv)
- `03` **做市商与庄家博弈**（229 篇）：[`domains/03_mm_and_token_loan.json`](domains/03_mm_and_token_loan.json) · [`domains/03_mm_and_token_loan.csv`](domains/03_mm_and_token_loan.csv)
- `04` **上币暗流与金融网络**（251 篇）：[`domains/04_exchange_listing_power.json`](domains/04_exchange_listing_power.json) · [`domains/04_exchange_listing_power.csv`](domains/04_exchange_listing_power.csv)
- `05` **宏观周期、AI 与商业洞察**（370 篇）：[`domains/05_macro_ai_business.json`](domains/05_macro_ai_business.json) · [`domains/05_macro_ai_business.csv`](domains/05_macro_ai_business.csv)
- `06` **研究方法与杠杆风控**（268 篇）：[`domains/06_research_and_mindset.json`](domains/06_research_and_mindset.json) · [`domains/06_research_and_mindset.csv`](domains/06_research_and_mindset.csv)
- `07` **行业观察与日常动态**（946 篇）：[`domains/07_industry_and_daily.json`](domains/07_industry_and_daily.json) · [`domains/07_industry_and_daily.csv`](domains/07_industry_and_daily.csv)
