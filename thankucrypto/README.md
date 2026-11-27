# allincrypto 熬鹰资本 (@thankUcrypto) · 实盘交易全平台开源档案（四源物理隔离版）

> 🌐 **在线沉浸式阅读**：[https://suoha888.github.io/Trader-Archives/thankucrypto/](https://suoha888.github.io/Trader-Archives/thankucrypto/)  
> 🤖 **外部 AI / Agent 一键全量直取入口**：[`llms.txt`](llms.txt) · [`DATASET_MANIFEST.json`](DATASET_MANIFEST.json) · [`data/platforms/`](data/platforms/)  
> 👤 **站主与整理维护**：**梭哈.AI**（[@SUOHA_AI](https://x.com/SUOHA_AI)）· [关注站主 X 主页 ↗](https://x.com/SUOHA_AI)  
> 🏛️ **所属开源项目**：[Trader-Archives 总站](https://suoha888.github.io/Trader-Archives/) · [GitHub 仓库首页](https://github.com/suoha888/Trader-Archives)

---

## 四大来源严格物理隔离总览（零交叉混排 · 外部 AI 全量直取）

本档案收录 **[@thankUcrypto](https://x.com/thankUcrypto)（熬鹰资本）** 跨平台公开一手原创资料。为防止多平台语料交叉混淆并让外部 AI 一键拿到全量结构化原文，所有数据已在 [`data/platforms/`](data/platforms/) 下按来源**物理分舱为纯 UTF-8（无 BOM）流式 `.jsonl`**，同时完整保留前端兼容的 JSON / Excel CSV / Markdown 全文包：

| 来源分舱 | 平台与账号 | 时间跨度 | 全量规模 | 独立物理隔离舱 (`.jsonl` 无 BOM) | Markdown 全文包 |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **01** | **X (Twitter)** `@thankUcrypto` | `2021-12` – `2026-11` | **3,420 篇**主表原推（7板块28节，S/A精选 1,100 篇）+ **62 篇**长推线程与复盘补遗 + **6 条**核心原话 | [`data/platforms/01_x_twitter/`](data/platforms/01_x_twitter/) | [`docs/thankucrypto_contract_handbook.md`](docs/thankucrypto_contract_handbook.md) |
| **02** | **早期微博** `allincrypto熬鹰者` | `2022-05` – `2025-05` | **943 篇**跨平台查重独占原帖（含 42 篇经典长文）+ **13 篇**经典段落与长微博补遗 | [`data/platforms/02_weibo/`](data/platforms/02_weibo/) | [`docs/weibo/`](docs/weibo/)（经典专卷 + 六阶段全文） |
| **03** | **官方深度专访与电台原声** | `2025-06` – `2025-10` | **3 场**专访拆为 **4 个独立话语单元**（区分媒体精编 3,102 字与本人 73.5 分钟原声逐字稿 19,778 字，主表合计 40,841 字）+ **1,759 条**秒级语音分段 | [`data/platforms/03_interviews/`](data/platforms/03_interviews/) | [`docs/interviews/`](docs/interviews/)（3 份独立全文） |
| **04** | **币安广场实盘直播** `@god_of_trader_tony` | `2026-04-18` – `2026-09-01` | **57 场**回放对账（**56 场**实质直播 317.9h / 录播 224.9h + 1 场 53s 无声断流片段）· **3,337 段**完整校对逐字稿（精确 **1,280,026 字**）· **1,337 条**干货切片 · **558 组 / 52,838 根**币安真实 K 线 · **1,310 个**发言时刻价格锚点 | [`data/platforms/04_binance_square_lives/`](data/platforms/04_binance_square_lives/) | [`docs/lives/`](docs/lives/)（56 份逐字稿 + 总索引 + 目录） |

---

## 目录结构与外部 AI 读取指南

### A. 外部 AI / Agent 自动化发现与物理隔离包（推荐 AI 优先读取）
- [`llms.txt`](llms.txt) — 遵循 `llmstxt.org` 标准的全量索引清单（含四大平台防混排说明与全部 `.jsonl` / `.json` / `.csv` / 65 份 `.md` 的 GitHub Pages 及 `raw.githubusercontent.com` 绝对直链）
- [`DATASET_MANIFEST.json`](DATASET_MANIFEST.json) — 机器可读全量文件清单（逐文件列出所属平台、编码 `utf-8` vs `utf-8-sig`、精确记录条数、字节大小、SHA-256 校验和与直链）
- [`data/platforms/`](data/platforms/) — **四大来源严格物理隔离 `.jsonl` 舱**（详见 [`data/platforms/README.md`](data/platforms/README.md)，含全量 128 万字直播逐字稿 `binance_lives_transcripts_3337_blocks.jsonl`）
- [`data/ai_rag_index.json`](data/ai_rag_index.json) — 全平台本地 RAG 检索知识库（`v=17`，共 **6,002 条**，已按 `T`［纯 X］/ `W`［纯微博］/ `A`［专访］/ `L`［币安直播］物理分键并将事后复盘涨跌隔离至 `h24` 字段）

### B. 网页与表格兼容数据文件（每条记录均带 `source_platform` 标记）
- [`index.html`](index.html) — 独立在线阅读页（7 大板块 28 节纯 X 推文 + 深度专访专区 + 早期微博时间轴 + 币安广场直播双视图与交互式真实 K 线图 + 四源隔离数据直取区 + 全平台 AI 问答助手）
- [`data/domains/`](data/domains/) — X 原推 7 大板块有序分类存档（JSON + Excel `UTF-8-SIG` CSV，详见 [`data/domains/README.md`](data/domains/README.md)）
- [`data/thankucrypto_tweets.json`](data/thankucrypto_tweets.json) / [`thankucrypto_tweets.csv`](data/thankucrypto_tweets.csv) — X 全量 3,420 篇分类总表
- [`data/thankucrypto_featured.json`](data/thankucrypto_featured.json) / [`thankucrypto_featured.csv`](data/thankucrypto_featured.csv) — X 核心精选干货表（774 篇 S / 高分 A）
- [`data/thankucrypto_weibo.json`](data/thankucrypto_weibo.json) / [`thankucrypto_weibo.csv`](data/thankucrypto_weibo.csv) — 早期微博独占原创总表（943 篇，段落级零 X 重复）
- [`data/thankucrypto_articles_full.json`](data/thankucrypto_articles_full.json) — 3 场一手深度专访与电台直播原声逐字稿结构化 JSON
- [`data/thankucrypto_binance_lives.json`](data/thankucrypto_binance_lives.json) / [`thankucrypto_binance_lives.csv`](data/thankucrypto_binance_lives.csv) — 56 场币安广场实盘直播结构化 JSON 与汇总表（内嵌同期 X 对照推文已显式标注 `source_platform="x_twitter"` 与 `is_live_speech=false`）
- [`data/thankucrypto_binance_klines.json`](data/thankucrypto_binance_klines.json) — 558 组真实币安历史 15m/30m 蜡烛线数据包（52,838 根 OHLCV 蜡烛线）
- [`data/thankucrypto_binance_dry_goods.csv`](data/thankucrypto_binance_dry_goods.csv) — 1,337 条直播全量干货切片总表（含全部 1,310 个发言时刻价格锚点明细列 `all_kline_pins_detail`）
- [`docs/lives/`](docs/lives/) — 56 场币安广场实盘直播完整时间戳校对逐字稿（[`DRY_GOODS_MASTER_INDEX.md`](docs/lives/DRY_GOODS_MASTER_INDEX.md) 7 大专题总索引 + [`README.md`](docs/lives/README.md) 目录 + 56 份单场全文）
- [`docs/weibo/`](docs/weibo/) — 早期微博独立 Markdown 全文包（[`00_classic65_exclusive.md`](docs/weibo/00_classic65_exclusive.md) 经典专卷 + [`01_weibo_2022_2025_full_timeline.md`](docs/weibo/01_weibo_2022_2025_full_timeline.md) 全量时间轴）
- [`docs/interviews/`](docs/interviews/) — 3 场深度专访独立 Markdown 全文存档
- [`docs/thankucrypto_contract_handbook.md`](docs/thankucrypto_contract_handbook.md) — X 7 大板块精选文字速查手册
- `images/` — 本地实盘与专访配图归档（共 **576 张**有效图片：含 X 实盘配图 568 张、深度专访配图 6 张、头像 2 张；其中主站正文卡片直接内嵌渲染 555 张）

## X 原推 7 大板块速览（共 3,420 篇）

| 序号 | 板块名称 | 小节数 | 总条数 | 精选干货 (S/A) | 分类存档 |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 01 | **仓位管理** | 4 节 | 307 | 183 | [`01_position_management.csv`](data/domains/01_position_management.csv) |
| 02 | **行情与开单** | 3 节 | 294 | 120 | [`02_market_and_entry.csv`](data/domains/02_market_and_entry.csv) |
| 03 | **山寨与做空** | 4 节 | 389 | 202 | [`03_altcoin_and_short.csv`](data/domains/03_altcoin_and_short.csv) |
| 04 | **事件与美股** | 5 节 | 626 | 192 | [`04_events_and_us_stocks.csv`](data/domains/04_events_and_us_stocks.csv) |
| 05 | **止损与出金** | 3 节 | 228 | 138 | [`05_stoploss_and_withdrawal.csv`](data/domains/05_stoploss_and_withdrawal.csv) |
| 06 | **心态与带单** | 5 节 | 466 | 260 | [`06_mindset_and_copytrading.csv`](data/domains/06_mindset_and_copytrading.csv) |
| 07 | **实盘记录与其他** | 4 节 | 1,110 | 5 | [`07_live_records_and_others.csv`](data/domains/07_live_records_and_others.csv) |

---

*由站主 **梭哈.AI**（[@SUOHA_AI](https://x.com/SUOHA_AI)）独立整理维护 · 开源分享，仅供学习复盘，非投资建议，请 DYOR。*
