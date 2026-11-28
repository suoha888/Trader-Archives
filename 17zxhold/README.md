# 5块的糖（@17zxhold）实战推文分类归档

> 🌐 **在线阅读站**：[https://suoha888.github.io/Trader-Archives/17zxhold/](https://suoha888.github.io/Trader-Archives/17zxhold/)  
> 👤 **整理维护**：站主 **梭哈.AI**（[@SUOHA_AI](https://x.com/SUOHA_AI)）

## 档案规模
- **主区 X 原创推文**：**535** 篇（已剥离他人转推与无意义寒暄，含 **52** 篇精选干货）
- **结构体系**：**5 大板块 · 11 个自然小节**（每节按「核心原则 → 实盘案例 → 踩坑避坑」逻辑排序）
- **核心原话导读**：**6** 条
- **AI 问答助手**：本地全量 RAG 索引（`data/ai_rag_index.json`）+ Vercel Edge 流式网关，支持时间段检索与 `#t-XX` / `#art-XX` 锚点直达

## 开源数据文件
- [`data/17zxhold_tweets.csv`](data/17zxhold_tweets.csv) / [`.json`](data/17zxhold_tweets.json)：主区分类推文表
- [`data/17zxhold_featured.csv`](data/17zxhold_featured.csv) / [`.json`](data/17zxhold_featured.json)：S/A 级精选干货表
- [`data/17zxhold_mental_models.csv`](data/17zxhold_mental_models.csv) / [`.json`](data/17zxhold_mental_models.json)：核心原话与导读
- [`data/domains/`](data/domains/)：5 大板块独立切片（JSON + UTF-8-SIG CSV）
