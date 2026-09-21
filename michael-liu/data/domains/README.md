# 憨厚的麦总历年 5,344 篇推文 · JEV 领域分类开放数据集

> 本目录为 **憨厚的麦总（@Michael_Liu93）** 历年 5,344 篇推文基于 **JEV (TypeSafe System 1)** 大模型评估生成的全景分类数据集，包含 7 大领域分卷，同时提供带 BOM 的 UTF-8-SIG CSV（Excel 零乱码直开）与标准 JSON 格式，完全开源免费，适合量化研究、回测与 AI Agent 知识库投喂。

## 目录分类明细

| 序号 | 领域代码 | 中文分类 | 篇数 | 核心内容简介 | JSON 文件 | CSV 文件 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `01` | `macro_cycle` | **宏观周期与逃顶大典** | **177 篇** | 美联储降息剧本、存储半导体/贵金属/BTC见顶信号 | [`01_macro_cycle.json`](01_macro_cycle.json) (150.3 KB) | [`01_macro_cycle.csv`](01_macro_cycle.csv) (62.2 KB) |
| `02` | `mindset_risk` | **交易心法与风控纪律** | **652 篇** | 仓位容错率、止损纪律、知行合一、拒绝带单 | [`02_mindset_risk.json`](02_mindset_risk.json) (499.0 KB) | [`02_mindset_risk.csv`](02_mindset_risk.csv) (173.3 KB) |
| `03` | `us_stocks_tech` | **美股科技与跨市场合力** | **125 篇** | NVDA/半导体基本面研报、美股合力vs币圈博弈 | [`03_us_stocks_tech.json`](03_us_stocks_tech.json) (109.2 KB) | [`03_us_stocks_tech.csv`](03_us_stocks_tech.csv) (46.4 KB) |
| `04` | `altcoin_trading` | **二级山寨与右侧交易** | **845 篇** | 破位做空、买点确认、山寨轮动逻辑 | [`04_altcoin_trading.json`](04_altcoin_trading.json) (691.6 KB) | [`04_altcoin_trading.csv`](04_altcoin_trading.csv) (266.6 KB) |
| `05` | `meme_pvp` | **Meme堑壕与PVP庄盘** | **577 篇** | PVP vs 庄盘辨别、翻倍出本、筹码穿透 | [`05_meme_pvp.json`](05_meme_pvp.json) (472.1 KB) | [`05_meme_pvp.csv`](05_meme_pvp.csv) (185.6 KB) |
| `06` | `onchain_flow` | **巨鲸与链上衍生品** | **124 篇** | 聪明钱雷达、资金费率与清算监控 | [`06_onchain_flow.json`](06_onchain_flow.json) (111.5 KB) | [`06_onchain_flow.csv`](06_onchain_flow.csv) (49.6 KB) |
| `07` | `discard` | **历年日常碎念与互动** | **2844 篇** | 日常生活随笔、非干货回复全景无损留存 | [`07_daily_chatter.json`](07_daily_chatter.json) (1938.1 KB) | [`07_daily_chatter.csv`](07_daily_chatter.csv) (568.6 KB) |

## 字段说明

- `id`: Twitter 推文唯一 ID
- `date`: 推文发布北京时间 (YYYY-MM-DD HH:MM:SS)
- `jev_depth`: JEV 模型判定的专业技术与逻辑深度 (0.0 ~ 4.0)
- `jev_is_substantive`: JEV 模型判定的干货概率 (0.0 ~ 1.0)
- `jev_has_rule`: JEV 模型判定的具体交易/买卖实操规则判别 (0.0 ~ 1.0)
- `is_featured`: 是否入选网站核心精选思维库
- `likes` / `retweets` / `replies` / `views`: 社交互动数据
- `text`: 推文清洗去重后的原始完整正文
- `images_count` / `local_images`: 本地关联实盘高清截图
- `url`: 原推直达链接