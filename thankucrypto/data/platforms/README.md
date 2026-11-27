# 四大来源物理隔离开源数据舱（`data/platforms/`）

为方便外部 AI Agent、量化研究脚本与 RAG 知识库直接读取并**彻底杜绝多平台语料交叉混排**，本目录将 **allincrypto 熬鹰资本 (`@thankUcrypto`)** 的全部公开一手资料按来源物理拆分为 **4 个互不混杂的独立子目录**。

## 核心隔离与格式规范

- **编码统一**：本目录下所有 `.jsonl` 文件均为 **纯 `UTF-8`（无 BOM）**，每行一个独立合法 JSON 对象，支持任意语言流式逐行读取（避免单体大 JSON 被 Web Fetch 截断，亦无 Excel CSV 的 `﻿` BOM 首列陷阱）。
- **来源零串味**：每个子目录仅存放单一平台语料，每行均显式携带 `source_platform` 与 `content_kind`。
- **实盘实时 vs 事后复盘严格分层**：在 `04_binance_square_lives/` 中，所有同日 X 推文正文已从直播会话中剥离（仅保留外部推文 ID 引用），且播中实时价格（`realtime_during_live` / `realtime_pins`）与下播后 24h/72h 复盘涨跌幅（`hindsight_after_live` / `hindsight_24h`）物理分层嵌套，防止量化回测产生未来数据泄漏。

## 四大物理隔离舱目录

### 1. [`01_x_twitter/`](01_x_twitter/) — X (`@thankUcrypto`) 本人原创推文舱（2021-12 至 2026-11）
- [`x_tweets_curated_3420.jsonl`](01_x_twitter/x_tweets_curated_3420.jsonl)：主站 7 大板块 28 小节全量 **3,420 篇**本人原创推文。
- [`x_tweets_supplement_recovered.jsonl`](01_x_twitter/x_tweets_supplement_recovered.jsonl)：从原始时间线找回的 **62 篇**本人长推线程续写段（含 2023-08 经典 15 段回撤复盘线程第 4、9 段）与独立长篇复盘帖。
- [`x_mental_models_6.jsonl`](01_x_twitter/x_mental_models_6.jsonl)：6 条核心交易心法原话与对应原推证据链。

### 2. [`02_weibo/`](02_weibo/) — 早期微博（`allincrypto熬鹰者`）独占原创舱（2022-05 至 2025-05）
- [`weibo_exclusive_943.jsonl`](02_weibo/weibo_exclusive_943.jsonl)：已剥离转发并与 X 推文完成段落级查重的 **943 篇**早期微博独占原帖（按 `s1..s6` 六阶段划分）。
- [`weibo_supplement_recovered.jsonl`](02_weibo/weibo_supplement_recovered.jsonl)：从《65 条经典长文》与原始微博归档找回的 **13 篇**本人独占经典段落与长微博补遗。
- *(配套整卷 Markdown 阅读版位于 [`../../docs/weibo/`](../../docs/weibo/)。)*

### 3. [`03_interviews/`](03_interviews/) — 官方一手深度专访与电台原声舱（2025）
- [`interviews_4_units.jsonl`](03_interviews/interviews_4_units.jsonl)：将 3 场深度专访按话语属性拆分为 **4 个独立单元**（OKX 第一期问答、币安华语电台 Odaily 第三人称媒体精编稿、币安华语电台 73.5 分钟第一人称直播原声逐字稿、OKX 复采篇），显式标注 `text_origin`，不把媒体第三人称转述与本人原话混编。
- [`binance_radio_20250718_raw_segments.jsonl`](03_interviews/binance_radio_20250718_raw_segments.jsonl)：2025-07-18 币安华语电台 73.5 分钟原声录音的全部 **1,759 条**秒级起止时间戳语音分段。

### 4. [`04_binance_square_lives/`](04_binance_square_lives/) — 币安广场（`@god_of_trader_tony`）实盘直播回放舱（2026-04 至 2026-09）
- [`binance_lives_manifest_57.jsonl`](04_binance_square_lives/binance_lives_manifest_57.jsonl)：主页全部 **57 场**公开回放原始清单（含 56 场实质直播 + 1 场 53.67 秒无声断流重连片段 `39654841083641`）。
- [`binance_lives_sessions_56_pure.jsonl`](04_binance_square_lives/binance_lives_sessions_56_pure.jsonl)：**56 场**实质直播纯单源场次汇总（不含 X 推文正文，实时行情与播后复盘分层）。
- [`binance_lives_slices_1337_pure.jsonl`](04_binance_square_lives/binance_lives_slices_1337_pure.jsonl)：**1,337 条**全量实战干货切片（逐字原话 `verbatim_quote` 与提炼摘要分层，含全部 **1,310 个**币安历史 K 线发言时刻价格锚点）。
- [`binance_lives_transcripts_3337_blocks.jsonl`](04_binance_square_lives/binance_lives_transcripts_3337_blocks.jsonl)：**56 场全部 `3,337` 段清洗后完整时间戳逐字稿（精确 `1,280,026` 字，覆盖 224.87 小时录播语音）**，供外部 AI 直接摄入全量口播上下文。
- *(配套 52,838 根真实 K 线数据包位于 [`../thankucrypto_binance_klines.json`](../thankucrypto_binance_klines.json)，58 份 Markdown 逐字稿位于 [`../../docs/lives/`](../../docs/lives/)。)*
