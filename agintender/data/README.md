# danny · agintender（@agintender）开源数据目录说明

> 本目录收录 **1,295** 篇经语义分类与复核的本人原创推文（精选 S/A 干货 **413** 篇），按 **6 大板块 · 16 个自然小节** 互斥归档，JSON 与 UTF-8-SIG CSV 100% 一一对应。

## 主表文件
- [`agintender_tweets.json`](agintender_tweets.json) / [`agintender_tweets.csv`](agintender_tweets.csv)：主区分类推文（1,295 篇）
- [`agintender_featured.json`](agintender_featured.json) / [`agintender_featured.csv`](agintender_featured.csv)：S/A 级精选干货（413 篇）
- [`agintender_mental_models.json`](agintender_mental_models.json) / [`agintender_mental_models.csv`](agintender_mental_models.csv)：核心原话与导读（6 条）
- [`agintender_early_archive.json`](agintender_early_archive.json) / [`agintender_early_archive.csv`](agintender_early_archive.csv)：早期英文 Builder 档案 (2017–2024)（509 篇）
- [`ai_rag_index.json`](ai_rag_index.json)：本地全量 RAG 检索索引

## 分板块切片（`domains/`）
- `01` **永续合约算法与清算博弈**（291 篇）：[`domains/01_perp_algorithms_liquidation.json`](domains/01_perp_algorithms_liquidation.json) · [`domains/01_perp_algorithms_liquidation.csv`](domains/01_perp_algorithms_liquidation.csv)
- `02` **庄家控盘、做市黑盒与上币生态**（272 篇）：[`domains/02_mm_listing_exchange_games.json`](domains/02_mm_listing_exchange_games.json) · [`domains/02_mm_listing_exchange_games.csv`](domains/02_mm_listing_exchange_games.csv)
- `03` **美股 Perp、币股 DAT 与金融合规**（181 篇）：[`domains/03_stock_perps_dat_compliance.json`](domains/03_stock_perps_dat_compliance.json) · [`domains/03_stock_perps_dat_compliance.csv`](domains/03_stock_perps_dat_compliance.csv)
- `04` **潮汕钱庄、灰黑金与地缘商业史**（95 篇）：[`domains/04_shadow_finance_geopolitics.json`](domains/04_shadow_finance_geopolitics.json) · [`domains/04_shadow_finance_geopolitics.csv`](domains/04_shadow_finance_geopolitics.csv)
- `05` **AI 时代、算力产业与个人方法论**（157 篇）：[`domains/05_ai_industry_research_methods.json`](domains/05_ai_industry_research_methods.json) · [`domains/05_ai_industry_research_methods.csv`](domains/05_ai_industry_research_methods.csv)
- `06` **交易纪律、周期体感与 OG 随笔**（299 篇）：[`domains/06_discipline_market_notes.json`](domains/06_discipline_market_notes.json) · [`domains/06_discipline_market_notes.csv`](domains/06_discipline_market_notes.csv)
