# 华尔街没有名字（@WallStreet0Name）实战推文与深度长文归档

> 🌐 **在线阅读站**：[https://suoha888.github.io/Trader-Archives/wallstreet0name/](https://suoha888.github.io/Trader-Archives/wallstreet0name/)  
> 👤 **整理维护**：站主 **梭哈.AI**（[@SUOHA_AI](https://x.com/SUOHA_AI)）

## 档案规模
- **时间跨度**：`2025-02-24` 至 `2026-09-23`
- **X 原创推文**：**2,211** 篇（从 2,730 条原始抓取中剥离转推、重复草稿与无意义寒暄，含 **668** 篇 S/A 精选干货）
- **结构体系**：**7 大板块 · 16 个自然小节**（每节按「核心原则 → 实盘案例 → 踩坑避坑」顺序编排，自动信号模板独立隔离于 7.2 节）
- **核心原话与模型**：**6** 条（每条均绑定核验存在的原推链接）
- **深度长文专区**：**13** 篇（共 **63,353** 字），已按 5 大主题分类并逐篇标定真实署名与来源：加密周期与宏观事件拆解（3 篇）、AI 产业链与美股/机器人深度研报（4 篇）、AI 投研提示词与自动化模板（3 篇）、宏观/尾部风险独立评估（1 篇）、跨境出金与港卡实操指南（2 篇）
- **AI 问答助手**：本地全量 RAG v9 索引（`data/ai_rag_index.json`，100% 覆盖全部原推与 13 篇完整长文）+ Vercel Edge 流式网关，支持历史年份语义区分、越界日期拒答与 `#t-XX` / `#art-XX` 锚点直达

## 开源数据文件
- [`data/wallstreet0name_tweets.csv`](data/wallstreet0name_tweets.csv) / [`.json`](data/wallstreet0name_tweets.json)：全量分类推文表（2,211 篇）
- [`data/wallstreet0name_featured.csv`](data/wallstreet0name_featured.csv) / [`.json`](data/wallstreet0name_featured.json)：S/A 级精选干货表（668 篇）
- [`data/wallstreet0name_mental_models.csv`](data/wallstreet0name_mental_models.csv) / [`.json`](data/wallstreet0name_mental_models.json)：6 条核心原话与思维模型
- [`data/wallstreet0name_articles_full.json`](data/wallstreet0name_articles_full.json) & [`docs/articles/`](docs/articles/)：13 篇深度长文结构化全文（含主题分类与真实来源标注）
- [`data/domains/`](data/domains/)：7 大板块互斥切片（JSON + UTF-8-SIG CSV 100% 守恒）
