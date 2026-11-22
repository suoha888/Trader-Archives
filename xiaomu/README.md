# 川沐｜Trumoo（@xiaomustock）实战推文分类归档

> 🌐 **在线阅读站**：[https://suoha888.github.io/Trader-Archives/xiaomu/](https://suoha888.github.io/Trader-Archives/xiaomu/)  
> 👤 **整理维护**：站主 **梭哈.AI**（[@SUOHA_AI](https://x.com/SUOHA_AI)）

## 档案规模
- **X 原创推文**：**3,103** 篇（已剥离他人转推与无意义寒暄，含 **1,596** 篇精选干货）
- **结构体系**：**6 大板块 · 13 个自然小节**（每节按「核心原则 → 实盘案例 → 踩坑避坑」逻辑排序）
- **核心原话/思维模型**：**6** 条
- **AI 问答助手**：本地全量 RAG 索引（`data/ai_rag_index.json`）+ Vercel Edge 流式网关，支持时间段检索与 `#t-XX` 锚点直达

## 开源数据文件
- [`data/xiaomu_tweets.csv`](data/xiaomu_tweets.csv) / [`.json`](data/xiaomu_tweets.json)：全量分类推文表
- [`data/xiaomu_featured.csv`](data/xiaomu_featured.csv) / [`.json`](data/xiaomu_featured.json)：S/A 级精选干货表
- [`data/xiaomu_mental_models.csv`](data/xiaomu_mental_models.csv) / [`.json`](data/xiaomu_mental_models.json)：核心思维模型与原话
- [`data/domains/`](data/domains/)：6 大板块独立切片（JSON + UTF-8-SIG CSV）
