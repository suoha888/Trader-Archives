# MSTR、STRC 与比特币四年周期研究报告

> **作者**：华尔街没有名字 (@WallStreet0Name)  
> **发表日期**：Sun Jun 07 05:20:08 +0000 2026  
> **官方原推**：https://x.com/WallStreet0Name/status/2063491173193527624  
> **文章 ID**：`2063452852354486272`  

---

先给结论
 
 
第一部分：事实核查
表 1：Strategy BTC 持仓变化表
 
过去约 12 个月净 BTC 变化： 从 2025-06-02 披露的 580,955 BTC 到 2026-06-01 披露的 843,706 BTC，净增加约 262,751 BTC。这是用 Strategy 官方购买表直接计算，日期口径不是审计 TTM，会有报告日和交易日错位。来源：Strategy purchases（https://www.strategy.com/purchases）
 
关键事实核查表
 
 
MSTR 当前 mNAV 和 BTC 每股含量
Strategy 官方定义的 mNAV 是：
Strategy 企业价值 / BTC Reserve
这里的企业价值包括普通股市值、债务本金、优先股 notional，并扣减最近披露现金余额。Strategy 自己说明这个 mNAV 不是传统基金 NAV，也不是 ETF NAV。来源：Strategy notes（https://www.strategy.com/notes）
 
重要： 如果把债务和优先股当作 senior claims，普通股 residual BTC NAV 约为 $30.51B，普通股市值 $40.216B，对 residual NAV 的倍数约 1.32x。这个数字更接近普通股股东真正关心的剩余权益溢价，但不是 Strategy 官方 mNAV。
 
表 2：Strategy 资本结构表
以下债务逐项本金部分为基于官方历史发行和 2026-05-26 债务回购后的推算。官方最新总债务为约 $6.7B 至 $6.754B；逐笔最新本金需要用下一份 10-Q 或完整债务表进一步核实。来源：Strategy 2026-05-26 press release（https://www.strategy.com/press/strategy-completes-1-5-billion-debt-repurchase-and-achieves-btc-yield-of-13-3-ytd-now-holds-843738-btc_05-26-2026）
 
STRC 的核心条款来自 424B5：$100 stated amount，月付现金股息，股息由董事会宣派，未付股息会累积并按月复利；公司表示会根据价格调整股息率，使 STRC 价格接近 $100；STRC 不可转换，不代表 BTC 所有权，低于所有债务，且低于 STRF。来源：STRC 424B5（https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/bltf36014d495f58e41/69c0a25e7e4ec7915151d133/form-424B5_03-23-2026_strc-annex.pdf）
Strategy 官方还明确提示，STRF、STRC、STRE、STRK、STRD 这些优先股没有 BTC 抵押，现金股息不保证。来源：Strategy STRK learn（https://www.strategy.com/strk/learn）
 
第二部分：用大白话解释 MSTR 的模式
1. MSTR 表面是软件公司，市场实际如何定价
MSTR 还有软件业务，但软件业务已经不是估值主线。Q1 2026 总收入 $124.3M，毛利 $83.4M；同一时期数字资产账面规模 $51.65B，数字资产未实现亏损 $14.455B，净亏损 $12.543B。这个量级说明，财报波动主要由 BTC 公允价值会计和资本结构决定。来源：Strategy Q1 2026 earnings release（https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/blt00fe8d0c4c346ff1/69fa4c71b2944f11309d48d8/strategy-q1-2026-earnings-release_05-05-2026.pdf）
市场实际买卖的是：
 
所以 MSTR 的股价不是单纯由软件收入折现决定。Strategy 自己也提示，MSTR 普通股交易价格可能反映与软件业务基本面无关的市场动态，且公司不是 ETF，也没有 ETF 的申购赎回机制。来源：Strategy notes（https://www.strategy.com/notes）
2. MSTR 为什么被市场视为杠杆 BTC 资产
原因很简单：
 
学术研究到 2025 年 4 月的样本显示，BTC 通常是公司 BTC treasury 股的信息主导变量，MSTR 属于 BTC beta 大于 1 的公司之一；但最新滚动 beta 需要用日频价格序列重新计算，我没有找到截至 2026-06-07 的可靠公开滚动 beta 数据。来源：arXiv paper（https://arxiv.org/abs/2505.14655）
3. MSTR 的核心飞轮
飞轮是：
 
这个飞轮的关键不是“买 BTC”三个字，而是 能否用低成本或高估值资本买入 BTC。
表 4：MSTR 飞轮状态表
 
什么时候有效
有效条件：
1. MSTR 能以高于 BTC 净资产的估值发行股票。
2. STRC 或其他优先股能接近面值发行。
3. 可转债投资人相信未来股价能超过转股价。
4. BTC 趋势向上，市场愿意给“买入更多 BTC”定价。
5. 市场相信 Strategy 不会被迫卖 BTC。
什么时候失效
失效条件：
1. mNAV 接近 1 或低于 1。
2. STRC 长期低于 $100，新增 STRC 等于高成本融资。
3. BTC 长期低于平均成本 $75,699。
4. USD Reserve 下降，市场担心分红和利息需要靠卖 BTC。
5. MSTR 普通股成交量下降，ATM 无法大规模卖出。
6. 可转债 out of the money，债务变成真现金偿还压力。
7. 市场不再相信“BTC 每股含量提升”能抵消稀释和 senior claims。
BTC Yield 是否真实创造价值
Strategy 的 BTC Yield 是一个 每股 BTC 含量变化指标，不是会计利润，不是现金收益率，也不是投资回报率。Strategy 官方 notes 明确说，这个指标不反映债务和优先股 senior claims，也可能在公司报告数字资产未实现亏损时仍然为正。来源：Strategy notes（https://www.strategy.com/notes）
结论：
 
MSTR 普通股是否等于直接买 BTC
不等于。
 
MSTR 相对 BTC 和 BTC ETF 的优劣
 
 
第三部分：用大白话解释 STRC 的模式
表 3：STRC 机制表
 
STRC 的招股文件说，公司预计主要通过 common ATM、USD Reserve、其他优先股、债务和股权融资来支付现金股息；同时文件也明确说，公司可能没有足够资金，或董事会选择不支付股息。来源：STRC 424B5（https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/bltf36014d495f58e41/69c0a25e7e4ec7915151d133/form-424B5_03-23-2026_strc-annex.pdf）
STRC 为什么支付高股息
因为它承担的不是普通债券风险，而是以下风险的组合：
 
STRC 的钱从哪里来
当前主要来源排序：
1. 普通股 ATM 融资。
2. STRC 或其他优先股融资。
3. USD Reserve。
4. 债务和再融资。
5. 必要时出售 BTC。
6 月 1 日 SEC 8-K 已经显示，32 BTC 出售的 proceeds 预计用于优先股 distributions。数量小，但路径已经被确认。来源：8-K 2026-06-01（https://assets.contentstack.io/v3/assets/bltf8d808d9b8cebd37/blt01aedf36c9f1b5b3/6a1cdb95487e7818fe49dd85/form-8-k_06-01-2026.pdf）
STRC 价格低于 $100 的影响
 
Q4 2025 文件里 Strategy 给出的 STRC 调整框架是：VWAP 低于 $95 时建议提高 50bp 或更多，$95 至 $98.99 时建议提高 25bp 或更多；但这仍由公司和董事会裁量。来源：Strategy Q4 2025 financial results（https://www.strategy.com/press/strategy-announces-fourth-quarter-2025-financial-results_02-05-2026）
一个通俗比喻
 
 
第四部分：最近卖出 32 枚 BTC 的市场解读
1. 数量影响
 
2. 为什么市场关注这么小的卖出
市场关注的不是 32 BTC 的卖压，而是 行为边界改变：
 
3. 这是否代表 Strategy 从“只买不卖”变成“必要时会卖”
是。 但需要限定：
 
4. 公告前后市场反应
 
5. 管理层解释
Strategy 2026-05-26 的资本结构更新中，CEO Phong Le 表示公司会主动管理可转债，并使用全套工具，包括纪律性出售 BTC。6 月 1 日的 32 BTC 出售与这个表态一致。来源：Strategy 2026-05-26 press release（https://www.strategy.com/press/strategy-completes-1-5-billion-debt-repurchase-and-achieves-btc-yield-of-13-3-ytd-now-holds-843738-btc_05-26-2026）
6. “数量小、信号大”是否成立
成立。
证据：
1. 数量只有 32 BTC，占总持仓 0.00379%。
2. SEC 披露用途直接指向优先股分红。
3. STRC 已经低于 $100，Strategy 的高息优先股融资成本上升。
4. 媒体和市场反应明显大于现货卖压本身。
5. 它证明 BTC 储备不是完全不可触碰的资产池。
 
第五部分：Strategy 接下来最可能的动作
已公告事实、管理层表态、市场推测
 
未来动作概率表
以下概率是 情景分析，不是官方指引。
 
 
第六部分：Strategy 是否会爆雷
爆雷框架
 
表 5：爆雷压力测试表
假设：
1. BTC 持仓 843,706 枚。
2. 债务 $6.754B。
3. 优先股 notional $15.5B。
4. 债务加优先股 claims 约 $22.254B。
5. 年化分红和利息约 $1.712B。
6. USD Reserve $900M，未考虑其他现金和软件经营现金流。
7. 没有假设强制保证金触发，因为没有找到官方证据显示 BTC 价格下跌会自动触发 forced liquidation。
 
哪个区间开始真正危险
 
比 BTC 价格更重要的指标
1. STRC VWAP 是否低于 $95、$90、$80。
2. STRC 股息率是否继续上调。
3. USD Reserve months 是否低于 6、3、1。
4. mNAV 是否跌到 1 或低于 1。
5. 普通股 ATM 每周卖出金额是否下降。
6. 优先股 ATM 是否暂停。
7. 债务到期和 put 日期前的再融资能力。
8. BTC 是否跌破 Strategy 平均成本 $75,699 后继续下行。
9. 是否出现连续 BTC 出售。
10. ETF 是否持续大额净流出。
 
第七部分：Strategy 对 BTC 价格的影响
表 6：MSTR 对 BTC 影响路径表
 
Strategy 买入规模对比
 
如果 Strategy 卖出不同数量 BTC
 
回答核心问题
 
 
第八部分：比特币四年周期是否还在重演
表 7：比特币四年周期对比表
历史价格为主流现货指数近似值，不同交易所和指数会有小差异。当前周期高点以 Reuters 报道 2025-10-06 BTC 突破 $125,000、最高约 $125,653 为参考。来源：Reuters 2025-10-06（https://www.reuters.com/business/bitcoin-hovers-near-all-time-high-2025-10-06/）
 
2024 年减半将区块奖励从 6.25 BTC 降至 3.125 BTC，每天新增供应约 450 BTC；相比 ETF 每周数十亿美元流入流出和 Strategy 单次数十亿美元买入，新增供应的边际影响已经小于过去周期。来源：Le Monde 2024-04-10（https://www.lemonde.fr/economie/article/2024/04/10/le-halving-quand-le-bitcoin-orchestre-sa-propre-rarete_6226962_3234.html）
当前周期像 2017、2021，还是完全不同
结论：时间像 2021，结构完全不同。
 
是否出现提前见顶信号
已出现的信号：
1. BTC 从 2025 年 10 月高点 $125k 附近回撤到 $61k 附近，回撤约 50%。
2. Reuters 报道 BTC ETF 出现超过 $2B 的净流出。
3. MSTR 出现首次小额 BTC 出售，改变市场叙事。
4. STRC 跌破 $100 面值，融资成本上升。
5. 宏观上 Nasdaq 大跌、短端收益率上升，风险资产承压。来源：Reuters 2026-06-04（https://www.reuters.com/legal/transactional/standard-chartereds-crypto-bull-sticks-100000-bitcoin-call-despite-painful-week-2026-06-04/）
没有足够证据的部分：
 
这些需要 Glassnode、CryptoQuant、Coin Metrics 或同等链上终端刷新。我不编数字。
四年周期的本质是什么
更准确的拆解：
 
MSTR 是否可能成为新的周期变量
是，但不是主导变量。
MSTR 的作用是：
1. 牛市时增加结构性买盘。
2. 高 mNAV 时放大 BTC 上行。
3. 熊市时通过 STRC、mNAV、融资窗口和小额 BTC 出售放大市场焦虑。
4. 如果极端情况下大规模卖 BTC，可能成为熊市中的强变量。
但当前证据不支持 “MSTR 单独打破 BTC 四年周期”。
 
第九部分：今年下半年布局 BTC 现货的资产配置分析
长期持有 BTC 现货真正赚的是什么钱
长期 BTC 现货赚的不是公司利润，也不是分红。它赚的是：
1. 固定供应下，全球储值需求上升带来的货币溢价。
2. 网络共识扩大带来的流动性溢价。
3. 法币购买力下降或财政赤字长期化背景下的资产替代需求。
4. 机构配置比例从 0 到低个位数的再定价。
5. 交易所、ETF、托管和监管成熟带来的风险溢价下降。
失效条件：
1. 全球监管系统性打压。
2. BTC 安全性或共识出现严重问题。
3. 长期 ETF 和机构资金持续流出。
4. 市场证明 BTC 不能在高利率环境中保有储值溢价。
5. 竞争资产分流主要资金。
MSTR 风险和 BTC 本身风险的区别
 
结论： MSTR 爆雷不会让 BTC 协议失效，但会造成短中期流动性冲击和信心冲击。
对只买 BTC 现货的人是否需要过度担心 MSTR
不需要过度担心，但必须监控。
合理处理方式：
1. 不把 MSTR 当作 BTC 本身。
2. 把 MSTR 当作 BTC 市场杠杆温度计。
3. 如果 STRC < $90、mNAV < 1、USD Reserve 持续下降、BTC 销售扩大，同时 ETF 继续净流出，应降低加仓节奏。
4. 如果 Strategy 只做小额卖出，ETF 流出放缓，BTC 重新站回关键价格区，MSTR 风险不应阻止长期配置。
表 8：下半年 BTC 配置方案
 
三种情景
以下为 情景分析，不是预测承诺。
 
 
第十部分：交易视角
先给交易结论
当前没有单一、清晰、高胜率的交易机会，因为三个核心变量同时不稳定：BTC 刚经历大幅下跌，STRC 低于面值，MSTR mNAV 已经压缩但还没有完全进入极端折价。
更可执行的方案是：
1. 长期配置者：分批买 BTC 现货或 ETF。
2. 交易员：等 MSTR、STRC、BTC、ETF 流量共振后再做相对价值。
3. 收益型投资者：STRC 只适合小仓位信用交易，不能当作低风险现金替代品。
4. 波动率交易：缺少当前 MSTR 期权 IV、skew、gamma、borrow 和 dealer positioning 数据，不给明确波动率建议。
交易结构表
 
 
最终结论
1. 一句话结论
MSTR 是 BTC 加融资飞轮加信用结构的复合资产，STRC 是高息永续优先股，32 枚 BTC 出售本身不重要，但它证明 Strategy 在压力下会动用 BTC 储备；这会放大 BTC 周期波动，但不足以单独打破 BTC 四年周期。
2. MSTR 的本质
MSTR 是上市 BTC treasury 公司。普通股持有人买到的是 BTC 敞口、mNAV 溢价、融资飞轮、期权波动和最后剩余权益。软件业务仍存在，但不是主要定价因素。
3. STRC 的本质
STRC 是 Nasdaq 上市、无 BTC 抵押、无强制到期、月付现金股息、股息率可调的永续优先股。它的收益来自 Strategy 支付股息，不来自 BTC 链上收益。
4. Strategy 当前最关键的三条风险
1. STRC 低于面值导致融资成本上升。
2. mNAV 压缩导致普通股 ATM 飞轮变弱。
3. USD Reserve 下降，市场担心分红和利息需要靠卖 BTC。
5. Strategy 当前最关键的三条支撑
1. 仍持有 843,706 BTC，规模极大。
2. 债务大多是长期可转债，目前没有找到 BTC 价格自动触发强制卖出的证据。
3. 仍有普通股、优先股、债务回购、BTC 小额出售等多种资本结构工具。
6. 32 枚 BTC 出售的真实含义
数量小，信号大。 数量只有 0.00379% 的持仓；但用途指向优先股分红，说明 BTC 储备可被用于资本结构现金需求。这改变了市场对 Strategy “永久只买不卖”的假设。
7. Strategy 是否会爆雷
当前不是马上爆雷。真正风险路径是：BTC 下跌，STRC 低于 $90，mNAV 跌破 1，普通股 ATM 关闭，USD Reserve 持续下降，债务和优先股现金需求无法通过融资覆盖。真正危险区大致从 BTC $30k 附近开始，$20k 附近进入严重偿付压力。
8. Strategy 是否会打破 BTC 四年周期
单独不会。它会改变周期形态，放大牛市买盘，放大熊市脆弱性，但 BTC 周期仍主要由全球流动性、ETF 资金、实际利率、长期持有人行为和杠杆清算决定。
9. 下半年 BTC 现货配置是否仍有意义
有意义，但不能按直线牛市假设配置。更稳妥的方法是分批买入、限制仓位、用 ETF flow、STRC、mNAV、USD Reserve 和链上指标决定节奏。只想长期持有 BTC 的人，没有必要碰 MSTR 或 STRC。
10. 普通投资者最容易犯的三个错误
1. 把 MSTR 当作 BTC 现货。
2. 把 STRC 当作安全债券或现金替代品。
3. 只看股息率，不看股息来源、清偿顺位和融资窗口。
11. 交易员最应该盯的十个指标
1. BTC 现货价格和 $75,699 Strategy 平均成本。
2. MSTR mNAV。
3. STRC 价格、VWAP 和 $95/$90/$80 阈值。
4. STRC 股息率调整公告。
5. USD Reserve months。
6. 每周 ATM proceeds。
7. Strategy BTC 买入或卖出 8-K。
8. BTC ETF 净流入净流出。
9. MSTR 期权 IV、skew、open interest、gamma。
10. 美元实际利率、DXY、Nasdaq 风险偏好。
12. 当前最优策略
 
13. 需要进一步核实的数据
1. 最新逐项债务本金和转股条款，需要下一份 10-Q 或完整债务表。
2. STRC 最新 30 日历史波动率、borrow cost、机构持仓。
3. MSTR 期权链 IV、skew、dealer gamma。
4. Glassnode、CryptoQuant、Coin Metrics 最新 MVRV、NUPL、Puell、RHODL、Realized Cap、LTH supply。
5. 2026-06-08 STRC 半月付息投票最终结果。
6. 未来 8-K 是否继续出现 BTC 出售。
7. ETF 发行商每日净流量和持仓变化。
14. 结论置信度

---
*收录于《Trader-Archives · 华尔街没有名字 实战交易与周期心智全书》*
