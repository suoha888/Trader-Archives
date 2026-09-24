# bStocks 的 B 面：不做更好的 Nasdaq，用 Perp 走出一条定价权之路

> **作者**：danny (@agintender)  
> **发表日期**：Fri Aug 14 12:26:51 +0000 2026  
> **原文链接**：https://x.com/agintender/status/2088240935276876180 (Article: https://x.com/i/article/2088217094961979392)  
> **全文字数**：15391 字  

---

鲁迅曾说过：不做更好，只做不同。如果最终目标是要拿下标的的定价权，那就不要去 Nasdaq 最强的地方硬碰硬，而是把战场搬到自己最擅长的 Perp、24/7、杠杆、链上库存和去中心化的野生/正规MM。
用Perp 拿下价格高地，用 bStocks 承接库存与纠错 ——拿下定价权。
1848 年，Chicago Board of Trade （CBOT）成立的时候，它还不是后来那个巨大的期货市场(CBOE)。芝加哥正在变成美国中西部谷物的集散地，铁路、运河把一船一船、一车一车的小麦和玉米送进城市。问题是，小麦不是股票。同样叫 wheat，不同农场、不同年份，根本不是同一种东西。买家如果连自己买到什么都不知道，就很难形成一个统一的市场价格。CBOT 最早做的事情之一，就是把这种混乱整理成可以交易的标准。1859 年获得伊利诺伊州授权后，CBOT 可以制定谷物等级，并由指定检验员判定质量；到了 1865 年，保证金和交割规则也开始制度化。
这件事听起来不像金融创新，更像仓库管理，但这个仓库改变了市场的结构。
谷物进入大型 elevator 以后，不再需要追问这一袋麦子来自哪一个农场。市场开始按照统一等级交易，例如某一种标准等级的小麦。美国联储在回顾这段历史时提到，这种 grading 和标准化仓储让买家知道自己买的是什么，也降低了交易成本，给流动性市场创造了条件。
然后才轮到期货。
农民可以提前卖未来的收成，粮商可以买未来的货，投机者不用把几千蒲式耳小麦搬回家，也能围绕未来价格下注。CBOT 从早期的 forward、“to-arrive”交易逐渐发展出标准化期货，到 19 世纪后半叶，芝加哥的谷物期货开始承担价格发现、风险管理和公开报价的功能。
这里有一个容易被忽略的地方。
最后跑得最快、交易量最大的是期货，但让期货不至于变成一场脱离实物的赌博的，是后面的谷仓。
 
背景
2026 年 8 月的一个周末，Binance 上 NVDA、TSLA、SNDK、SKHY 四只股票永续合计成交约 4.61 亿美元。星期天，四只 Perp 的价格都高于前一个现金市场收盘，星期一美国现金市场开门以后，四只却全部低开。单看 SNDK，那个周末 Perp 成交约 3.38 亿美元，Friday Cash Close 是 1,212.21 美元，Sunday 交易到 1,223.98 美元，Monday Cash Open 却落在 1,203.41 美元。
一个月前的美国独立日长周末，同一只 SNDK 给出了另一种答案。现金市场从 1,745 美元休市，但在周日 Binance 交易到 1,841.88 美元，周一 Cash Open 是 1,828.68 美元。现金市场重新开门后出现约 4.8% 的跳空，Binance 周末价格提前覆盖了这次上涨的大部分幅度，只是价格走过了头。
同一个产品，一次把周一的大跳空提前交易出来，一次在几亿美元成交以后把方向看反。这件事把 24/7 股票的问题从“交易时间延长”推到了市场结构：成交量不是定价权。
如果 Binance 的目标只是让用户星期六也可以买股票，延长交易时间就够了。但把 Direct Stock、TradFi Perp 和 bStocks 放在一起看，可以看到一套不同的结构。现金市场闭市以后，Perp 先承接交易方向、杠杆和高频交易，bStocks 提供可以持有、搬运、抵押和对冲的股票库存，链上协议把中心化交易所之外的资本接进来。等传统股票市场重新开门，再看这套 24/7 市场形成的价格有没有被美股市场接受。
这篇文章讨论的不是 bStocks 是不是另一种 tokenized stock，而是另一件事：如果 Binance 要争传统股票闭市后的第一版价格，为什么发动机要用 Perp，而 bStocks 又为什么会成为库存层和纠错层。
一、Binance 要争的不是多两个交易日，而是股市关门以后的价格
股票市场有一个时间上的缺口。纽约星期五下午 4 点收盘以后，公司还会发布消息，宏观政策会变化，产业链会发生新的事情，战争和政治也不会等 Nasdaq 上班。资金仍然在重新估值这些股票，只是这些判断暂时进不了美国现金股票的正式订单簿。
所以问题不是没有信息，而是信息出来以后应该去哪一个市场（用仓位）表达。如果某个市场可以在 NYSE、Nasdaq、KRX 、港交所休市的时候承接股票风险，它就有机会形成下一次正股市场开门之前的价格发现。
Binance 的三种产品刚好分成三个角色。Direct Stock 负责真实证券、公司行动和传统市场接口；bStocks 把股票变成一件可以持有、转换、转链和抵押的资产；TradFi Perp 负责多空、杠杆和连续交易。
 
如果要成为价格发现的源头，最适合冲在前面的不是 bStocks，而是 Perp。原因也不复杂：价格发现的第一步是让观点进入市场，而衍生品表达观点的成本是低于现货的。
二、为什么Perp更容易做到价格发现？
以 NVDA 为例，7 月 17 日至 22 日的一段样本里，NVDAB Spot 名义成交约 421 万美元，同期 NVDAUSDT Perp 约 4.18 亿美元，相差约 99 倍。只看周末，7 月 18 日 Perp 约为 bStocks 的 37 倍，7 月 19 日约为 68 倍。
 
这里比较的是 Binance 内部两种产品，不是 Binance Perp 和 Nasdaq NVDA 正股。美国现金股票的成交规模仍高于 Binance 股票 Perp。这个比较的意义，是看现金市场休息以后，新的方向订单更容易流向哪里。
现货买完以后可以放几个月，而Perp 会不断开仓、平仓、反手、调整杠杆、做 basis、收 funding，做市商也会不断重新 hedge。同样一块钱的资本，在 Perp 里可以贡献多次 gross turnover。做空的区别更大：星期六出现 NVDA 利空，没有 NVDAB 库存的人想在现货做空，需要先处理 borrow；Perp 只需要 Sell 就能表达方向。
因此，休市后的第一条价格路径可以写成 Information → Perp → Candidate Price。Perp 的作用是生产候选价格，而不是保证候选价格正确。这个区别决定了 bStocks 存在的意义。
三、研究口径：25 次“闭市—重开”的数据比较
为了观察这口价格是怎么形成的，我们收集并整理了 NVDAUSDT、TSLAUSDT、SNDKUSDT、SPCXUSDT和 SKHYUSDT 的交易数据。美国市场能够完整对应下一次 Cash Open 的样本有 25 次，其中 NVDA、TSLA、SNDK、SPCX 各 6 次，SKHY 1次。
一次样本从前一个 Cash Close 开始，经过 Pure Weekend、Sunday Price、Monday Premarket、Opening Auction，再到下一次 Cash Open。Sunday 19:59 ET 用来观察常规美股 Premarket 尚未开始时的价格，Monday 04:00 以后 Premarket 回来，09:25 之后 Opening Auction 信息进入，最后拿正式现金开盘作为验证点。
这批数据分别回答四种问题：
1. 价格部分看周末报价离下一次现金开盘有多远；
2. 流动性部分看屏幕价格可以承受多大的实际订单；
3. 成交量部分看市场转了多少钱；
4. 交易频次部分则看这些成交更像投资者的独立观点，还是程序化交易、做市和 HFT 形成的高周转市场。
一个市场有价格，不代表价格能执行；有成交，不代表成交来自独立判断；有流动性，也不代表它拥有价格发现能力。
四、价格调查：从 181.9bp 收敛至 11.3bp
这里的“误差”是某一时点 Binance Perp 价格与下一次 Cash Open 的绝对距离，统一换算成 basis points （bp）。
 
周日的结果是 13/25，也就是 52%。25 个样本里 13 次方向一致、12 次不一致，与 50% 的随机方向判断没有可辨识差别，所以这批数据不能证明 Binance 存在稳定的 Weekend Discovery。
 
09:29:59 的 11.3bp 也不能被简单地认为是 Binance“预测周一开盘”的能力。到了这个时间，美国 Premarket 已经交易几个小时，Opening Auction 的信息也进入市场。Perp 如果仍然大幅偏离股票盘前报价，本身就会形成交易机会。
因此，从 181.9bp 收到 11.3bp 能说明 Binance Perp 在传统市场重新上线的过程中逐步接近下一次 Cash Open，却不能说明是 Binance 带着现金市场走。要回答这个问题，还需要把 Binance Perp、bStocks 和同一秒的美国 Premarket last、bid、ask 放到一起做 lead-lag。
如果 Premarket 先从 100 走到 105，Perp 后来才到 105，这是 follow；如果 Perp 先到 105，Premarket 后面向它靠，才有价格发现和价格领导的意义。
五、开盘前的价差不是一条直线：SNDK 在 09:25 只差 2bp，五分钟后反而偏离了
2026 年独立日长周末（7月3日-5日），NVDA、TSLA、SNDK 三只 Perp 从 Sunday 到 Opening Cross 前的路径就不同。
 
这么看起来 这时候的 NVDA 更像一条纠错路径。周日在 198.35 美元，而 Cash Open 最后是 194.42 美元，差约 202bp；09:25 回到 194.97，09:29:59 是 194.55，误差缩到 6.7bp。
TSLA 的方向从 Sunday 开始就是对的。Cash Close 是 393.45，Sunday 是 399.40，Cash Open 是 397.50。市场提前交易出上涨方向，只是 Sunday 的幅度超过了最终 Opening Gap。
 
SNDK 的路径更说明问题。09:25 时 Perp 在 1,828.97 美元，Cash Open 最后是 1,828.68 美元，差不到 2bp；到了 09:29:59，Perp 又掉到 1,825 美元，误差扩大到约 20bp。
这说明 Opening 前价格不会沿一条直线朝最终开盘价移动。Premarket 成交、NOII、做市商库存和最后几分钟的订单都会改变价格。研究谁拥有定价权，不能只看周日和周一09:29:59 两个时间段，而要看整段 lead-lag path。
六、Perp 不一定比 bStocks 更接近下一次 Open
另一组低频样本使用 NVDAB、TSLAB、MUB、COINB 的 UTC 日末价格，与下一次美股 Cash Open 做 handoff 比较，并对有数据的标的加入 Perp。
 
八个 bStocks 观察值的 handoff error 中位数约 117.2bp，六个可比 Perp 观察值约 118.9bp。
7 月 23→24 日的 NVDA 是一个好例子。NVDAB 是 207.97，Perp 是 207.99，下一次 Cash Open 是 207.45，两边都高约 25–26bp。这里 bStocks 的价值不是给出一个比 Perp 更接近正股市场的价格，而是把休市期间形成的股票价格保存成一份可以持有、转移、转换和融资的现货型库存。
Perp 负责让价格移动，bStocks 负责把价格变成资产。
七、股票拆开以后：NVDA 是纠错，TSLA 是 Overshoot，SNDK 是压力测试，SPCX 是产品实验
在 NVDA 的数据样本里，Sunday 与下一次 Cash Open 的平均绝对偏差约 113bp，方向 3/6；TSLA 约 81bp，方向 4/6；SPCX 约 149bp，方向 3/6；SNDK 达到约 351bp，方向 3/6。到了 09:29:59，四者的描述性平均偏差分别降到约 11.8bp、8.6bp、9.4bp 和 16.0bp。
 
NVDA 更适合看错误价格怎么修正。值得注意的是在独立日样本里，Sunday 198.35，Cash Open 194.42，偏差 202bp，之后价格一路向 194 美元附近回归。
TSLA 适合看 Overshoot。Cash Close 393.45，Sunday 399.40，Cash Open 397.50，方向对了，幅度超了。
SNDK 把两种状态放在同一只股票里。独立日长周末，它提前交易出大部分 +4.8% 的 Opening Gap；8 月另一个周末，Friday Close 是 1,212.21，Sunday 是 1,223.98，Monday Cash Open 却是 1,203.41，方向反了。
 
SPCX 的位置不一样。它的 Sunday MAE 约 148.8bp，方向也是 3/6，但这只股票从 Pre-IPO Perp 一路走到公开股票、TradFi Perp 和 SPCXB，同一个风险在 Binance 里经历了“先有衍生品价格、后有现金股票”的产品迁移。它更适合拿来观察一套 24/7 价格体系怎样和后来出现的现金市场接轨。
所以闭市价格不适合只分“对”和“错”，而是可以进一步分为：Direction Discovery、Magnitude Discovery、Correction Dependency。（后文会介绍）
八、SPCX：从 Pre-IPO Perp 到公开股票，Perp到股的定价实验
SPCX 和 NVDA、TSLA、SNDK 有一个结构上的差别。Binance Futures 在 2026 年 5 月推出 Pre-IPO Perpetual 时，第一只合约就是 SPCXUSDT，用来交易 SpaceX 未来公开市场估值。SpaceX 上市以后，SPCXUSDT 转为标准 TradFi Perp；同时也增加了 SPCX Direct Stock 和 SPCXB。也就是说，这只股票先有衍生品价格，后有可以验证它的公开现金市场，再补上可以持有和上链的 bStocks。
这给了一个少见的实验环境。对 NVDA 和 TSLA 来说，Binance 是在一个成熟市场外额外增加的 24/7 风险层；SPCX 则经历了“Pre-IPO Perp → Public Stock → TradFi Perp → bStocks”的迁移。等现金股票出现以后，原来那个不停交易的衍生品价格才第一次有了固定的 Monday Cash Open 可以反复校验。
六个完整周末的 SPCXUSDT 数据如下：
 
六次 Sunday Price 的方向是 3/6，距离下一次 Cash Open 的平均绝对偏差约 148.8bp，中位数约 134.4bp。到了 Monday 04:00，平均偏差降到 114.1bp；08:00 是 102.0bp；09:00 是 53.8bp；09:25 是 29.3bp；09:29:59 则降到 9.4bp。08:00 以后六次方向都与最终 Opening Gap 一致，但这时候 Premarket 已经回来，所以这条曲线证明的是价格接力和收敛，不是 Binance 单独完成了价格发现。
SPCX 还把 Overshoot 这件事表现得很集中。在 Sunday 方向看对、同时 Opening Gap 超过 50bp 的三个周末里，7 月 20 日 Sunday Move 约为最终 Gap 的 2.79 倍，7 月 27 日约 1.60 倍，8 月 10 日约 1.34 倍。所以这个事情可能上线时间的关系不大，即使上线市场也会overshoot。
8 月 10 日的路径更说明问题。Friday Close 是 133.11 美元，Sunday 已经到 135.57，Monday Cash Open 是 134.95。这个 Sunday Price 只比最终 Open 高约 46bp，但 Monday 08:00 SPCXUSDT 一度冲到 138.80，离最终 Cash Open 扩大到约 285bp；09:29:59 又回到 134.86，只差约 6.7bp。价格可以靠近，也可以在 Premarket 回来以后重新走开，再收回来。
此外，SPCX 的成交结构也不是一个安静的现货市场。六个周末 SPCXUSDT 合计成交约 15.46 亿美元，约为 NVDA 同口径的 10 倍；底层 fills 约 358 万笔，平均 3.45 笔/秒。它的规模处在 SNDK 和 NVDA 之间，更像一台全天运行的程序化风险机器。对 bStocks 来说，这个案例的意义很直接：Perp 转得越快，只要存在客户净订单流，做市商就越需要 SPCXB 或 SPCX 这样的库存腿去承接 delta。
所以 SPCX 不是“Binance 已经拿到周末定价权”的证明。它更像整套产品栈的缩影：Perp 先生产候选价格，SPCXB 把价格保存成资产，Stock 提供现金市场出口，borrow 和跨市场套利决定错误价格能不能被双向攻击。它让我们看见 Binance 如果要争闭市定价权，这套基础设施可能长什么样。
九、周末的交易量调查
从六个周末的数据统计来看，NVDAUSDT 累计成交约 1.54 亿美元，TSLAUSDT 约 1.07 亿美元，SPCXUSDT 约 15.46 亿美元，SNDKUSDT 达到 29.22 亿美元。
 
从上表来看，成交量出现了清楚的梯队：SNDK 六个周末 29.22 亿美元，SPCX 15.46 亿美元，NVDA 1.54 亿美元，TSLA 1.07 亿美元。SPCX 约为 NVDA 的 10 倍、TSLA 的 14 倍，但只有 SNDK 的一半左右。这个排序和公司市值、传统股票知名度并不是线性关系，所以 gross volume 不能直接翻译成自然投资需求。
还有一个数据值得注意：开盘前最后五分钟，SNDK 六次平均仍有约 2,664 万美元成交，SPCX 约 1,888 万美元，NVDA 约 249 万美元，TSLA 约 201 万美元。Opening Cross 临近时，Perp 不是停在那里等结果，而是在继续重新交易价格。
Volume 这个数据的核心是：这些成交是谁做的、以什么频率发生、每单多大。
十、交易频率调查：SNDK 每秒 7.3 笔，SPCX 每秒 3.45 笔
把 SNDK 的 29.22 亿美元和 SPCX 的 15.46 亿美元拆到逐笔成交以后，市场形态发生了变化。
 
SNDK 六个周末一共有约 757 万个 fills，平均每秒约 7.3 笔；SPCX 约 358 万个 fills，平均每秒约 3.45 笔；NVDA 约 64 万个 fills，平均每秒约 0.62 笔。三只股票的差距首先体现在交易频率。
 
有意思的事，单笔金额的差距没有成交频率那么大。SNDK 平均 raw fill 约 386 美元，SPCX 约 432 美元，NVDA 约 241 美元。SPCX 的中位金额约 171 美元，也和 SNDK 的 173 美元接近。SNDK 和 SPCX 的大额 turnover 不是靠少数超级大单堆出来的，而是靠更密集的成交
由于我们无从得知交易账户的信息、我们也不知道这些 fills 来自多少独立参与者，机构，做市商，但从交易的体量和频率观察，本文倾向于，“这几十亿美元的成交并不代表同等规模独立投资观点”的论点。（aka 不是机构在下注）
我们认为，SNDK 和 SPCX 都形成了高转速股票衍生品市场，只是 SNDK 的转速更高。
（SNDK 分析：https://substack.com/@agintender/note/c-311284509?utm_source=notes-share-action&r=8gs9xi ）
SPCX 交易量的 24 小时分布还能再进一步分析：
美东时间 00:00–06:00 仍贡献约 20.8% 的周末 gross notional 和约 20.9% 的 raw fills，对应这段深夜时段平均约 2.9 fills/秒。六个周末的 taker buy/sell notional imbalance 约为 -1.16%，整体接近双向平衡。这个形态更像做市、程序化交易和跨市场套利共同形成的全天候市场。
十一、每单大小也提示，Perp 和 bStocks 可能承接的是两类订单
SNDK Perp 的平均 raw fill 约 386 美元，SPCX 约 432 美元，NVDA 约 241 美元；SPCX 和 SNDK 的 aggTrade 中位金额分别约 171 美元和 173 美元。Binance Research 对 bStocks 的报告称约 93% 的 bStocks 交易属于 fractional trade，中位成交额只有 18.81 美元，约 80% 的 tokenized-stock 交易来自新兴市场用户。（https://www.binance.com/en/research/analysis/opportunity-only-tokenized-stocks-unlock）
需要注意的是，本文 Binance Research的数据口定义不同，所以不能直接用 386 除以 18.81，然后推出 Perp 用户的平均仓位是 bStocks 用户的 20 倍。不过如果把它们放在一起，可以看出一种产品分工：bStocks 更容易承接小额现货、长期库存、跨时区 retail 和链上用户，Perp 更容易集中杠杆、basis、做市、HFT 和高周转资金。
一个市场负责形成可持有的股票库存，另一个市场负责让同一份风险高速换手。只有做市商和套利者把两边连接起来，才可能形成一套价格网络，而目前这两个不同的产品还没有联动起来，这是一个可以发力的点。
十二、Perp 成交越大，bStocks 的库存作用越突出
既然 Perp 成交量可以是 bStocks 的几十倍，为什么 Binance 还需要 bStocks？答案在做市商的账本里。
客户和 Market Maker 的 Perp 仓位是镜像关系。客户净 Long，MM 就是 Short Perp，需要买入正 delta 的 bStocks 或 Stock；客户净 Short，MM 就是 Long Perp，需要卖掉 bStocks 库存，或者借 bStocks 以后卖。
 
Perp 解决的是交易速度，bStocks 解决的是风险放在哪一层资产负债表里。如果客户净订单持续向一个方向流，MM 的 delta 就会积累，不能永远留在 Perp 内部转手，总要有一条库存腿承担风险。
所以 Perp 的高成交量不是 bStocks 失败的证据，反而是 bStocks 存在的理由的之一。衍生品转速越高，对库存、融资和借券的需求就越大，对散户可能没什么感觉，但是这对于做市商来说则是一个必需品。
十三、bStocks 不是“支点”，1:1 backing 更像 terminal constraint
说到这里，大家可能会把 bStocks 叫作 Perp 的现货锚定点，容易把它想成 USDT 对美元的那一套。但是在不同场景下作用是不同的，至少在股票周末不是这样的。
星期六把 NVDAB 转成 NVDA Stock，不代表 Nasdaq 同一秒有现金市场让另一条套利腿完成。你拿到的是一份能够接回真实股票的库存，不是一个可以马上完成的 Cash Arbitrage。
所以 1:1 backing 更像 terminal constraint。市场知道 bStocks 最后能够接回真实股票，也知道 Cash Market 会再次打开，因此价格可以在休市时偏离，但偏差超过资金成本、库存成本、event risk 和执行摩擦以后，会产生等待传统市场重新开放再收掉价差的激励。
因此 bStocks 的工作不是告诉 Perp“正确价格是什么”，而是给 Perp 的候选价格配上一份可以持有、对冲和套利的库存。
这就是为什么把 bStocks 看成是“库存层”和“纠错层”更准确。
十四、bStocks 上链以后，重点是让库存转起来
如果 NVDAB 只能留在 Binance Spot 账户里，它只是 CEX 内部的一层现货库存。bStocks 上链以后，它可以进入 DEX、Lending、Collateral 和 Margin 系统，市场结构就改变了。
PancakeSwap 上线了包括 TSLAB、NVDAB、MUB、SNDKB 在内的 bStocks 池；Lista 支持部分 bStockss 抵押借 Stablecoin；Aster 允许符合条件的 bStockss 进入 Multi-Assets Mode；Youcanshortit.com 让用户可以杠杆借出bStocks；Pundi X Basket 让用户自由定制自己的投资组合和指数ETF，让其他散户可以跟单。
 
它们解决的不是同一件事，但方向是一致的：让 NVDAB、SNDKB、SPCXB 不只躺在钱包里，而是可以被交易、抵押、融资、做市和对冲。
 
这里要区分“增加用途”和“增加流动性”。一枚 NVDAB 被锁进 Lending Protocol 做 collateral，utility 增加了，但它未必给市场增加新的买卖盘。只有当这份库存能被做市商、套利者或空头借出来，再进入 CEX、DEX 或 Perp 对冲，它才开始增加市场里的可用库存。
所以理想的链上循环不是“Binance → Wallet → DEX”，而是 bStocks → DEX / Lending / Credit Pool → Market Maker → Perp Hedge → CEX → Stock Conversion。同一份 bStocks 被不同账户重复使用，库存才会产生周转。
 
对 bStocks 来说，TVL 不是最关键的指标。更值得看的是一份股票库存能被使用多少次。100 万美元 NVDAB 如果只是锁在协议里，它仍然是 100 万美元静态资产；如果其中一部分能够被 MM 借出来报价，再用 Perp 对冲，成交后重新回到库存池，它才开始变成市场基础设施。
Binance 自身研究还报告过 2,806 名用户参与 bStocks、Perp 和 Equity 之间的近似套利式交易，涉及约 2.16 亿美元，约 58.5% 的 bStocks 用户同时使用 Perp 和/或 Equity。（所以“野生”量化一直存在，而我们应该想着激活他们成为 bStocks的种子用户）
上链以后，一条路径可以是 NVDAB 抵押以后借 Stablecoin，Stablecoin 再回 CEX 做 NVDAUSDT Perp；另一条路径可以是 NVDAB 进入 DEX LP，再用 NVDAUSDT Perp 对冲 LP 的股票 delta。
于是 bStocks 把 CEX Perp、CEX Spot、真实 Stock、DEX、Lending 和 Stablecoin 放进同一个风险网络。
这也是 bStocks 和普通“股票代币”之间的差别。
十五、这套系统缺的不是更多 ticker，而是 borrow
拿 NVDAB 抵押后借 USDT，是融资。借 NVDAB 出来，再把 NVDAB 卖掉，才是 stock borrow。两件事都会出现“借”，但对价格发现的作用不同。
如果 Perp 贵、bStocks 便宜，套利者可以 Long bStocks + Short Perp。这条交易是相对来说容易执行，买便宜的现货、卖贵的衍生品，会压缩 Perp 溢价。
 
如果 bStocks 贵、Perp 便宜，交易应当反过来做：Short bStocks + Long Perp。问题是，没有可借库存就做不了这个交易。折价时有现金就可以买，高估时却不是所有人都有货可以卖。
所以 bStocks 的成熟度不应该只看 listing 数量。Borrow Depth、Borrow Rate、可借库存，以及事件周末 borrow 是否稳定，会决定这套市场有没有双向纠错能力。
没有 borrow，bStocks 只是一个资产层，没办法在平台上发挥出应有的优势。
Borrow 补上以后，它才接近证券库存市场。
做市需求带动Borrow → Borrow 需求带动利率上升 → 利率上升吸引越来越多的deposit → bStocks 的交易量和需求带起来 ，如此反复
十六、CEX 的 bStocks 要做深，核心还是 Borrow 的生态联动
回到 Binance CEX，bStocks 的流动性瓶颈更清楚。客户大量卖 NVDAB 时，做市商可以买入 NVDAB，同时 Short NVDAUSDT 对冲，Bid Side 主要消耗现金；客户大量买 NVDAB 时，MM 必须不断把股票卖给客户，库存卖完以后，如果没有 Borrow，只能缩小 Ask Size、提高报价，或者退出市场。
 
所以 bStocks 的现货盘口天然有一个库存问题。没有 Borrow，做市商手上有多少股票，就只能围绕多少股票报价；有了 Borrow以后，库存从一个硬上限变成一个有价格的资源。MM 可以借 NVDAB 卖给客户，同时 Long Perp 或用 Stock 对冲。借券需求上升，Borrow Rate 上升，又可以吸引持有人把更多 bStocks 放进库存池。
 
Borrow 还解决了前文的反向 Basis 问题。Perp 贵、bStocks 便宜时，Long bStocks + Short Perp 谁都能做；bStocks 贵、Perp 便宜时，需要 Short bStocks + Long Perp，如果此时没有可借库存，那么这条套利链就无法起到作用。
当然，Borrow 不是单独工作的。CEX 流动性要做深，还需要 Stock ↔ bStocks Conversion 补充库存，Portfolio Margin 降低 bStocks 与 Perp 对冲的资本占用，Market Maker Program 再把这些库存转成 Bid 和 Ask。Maker Rebate 可以让做市商和Pundi X Basket 等协议愿意开机器人，但 Borrow 决定机器人手里有没有货。
所以总结起来：
Perp 负责产生订单，bStocks 负责提供股票库存，Borrow 负责让库存流动。
如果 Borrow 做起来，bStocks 才会从“可以交易的股票代币”，往“可以被做市、融资和双向套利的证券库存”再走一步。
比起华尔街，币圈最大的武器就是去中心化。用 Borrow 调动所有“去中心化”的正规/野生做市商来参与这场周末的博弈。
十七、终局不是 bStocks 对 Perp，而是四个市场能联动起来
假设未来 borrow、conversion 和链上深度都成熟，同一个 NVIDIA 风险可能同时有四个价格。
 
这时候 cross-venue trader 最先关心的不会是 NVIDIA 明年 EPS，而是哪个市场贵、哪个市场便宜。
 
DEX NVDAB 在 201，Perp 在 199.60，可以卖贵的一腿、买便宜的一腿；没有 bStocks 库存就 borrow，没有现金就拿资产做 collateral，不想承担 NVDA 总体方向，就在另一条腿锁住 delta。现金市场重新开放以后，再根据 Stock、bStocks 和 Perp 的 basis 调整库存。
这时候 bStocks 不再是一种独立交易产品，而是一种让 Stock ⇄ CEX Spot ⇄ DEX ⇄ Perp ⇄ Credit 之间能够迁移风险的资产格式。
价格也不是某一家交易所喊出来的，更不是流动性挤出来的，而是不同市场的套利者拿资产负债表不断压价差以后形成的。
十八、以后判断 bStocks 成熟度，不该只看 Volume 、流动性和上线数量
如果只用 AUM、24h Volume 和 ticker 数量衡量 bStocks，就真的埋没了它在市场结构里发挥的作用 —— 这本是个要超脱三界的魔丸，结果你就拿来打个酱油？！
Volume 和流动性只是其中一项指标，而且 gross volume 还会受到程序化回转和高频交易影响。
如果 Binance 想把 bStocks 做成周末股票市场的库存层，Borrow Depth、可执行现货深度、Conversion Capacity 和 Perp-bStocks basis 的稳定性，这可能比多上几百只 ticker 、单只现货的深度更重要。
100万的买/卖1和1000万的买/卖1，本质是没有区别的，而且要是说到深度为什么不去 Nasdaq 呢？比起深度，哪个价格才是“正确”的才更有价值。
为什么是这样？因为“不正确”的流动性本质就是套利的燃料。
本文整理了对应的能力及其对应的指标：
 
结语：Perp 抢定价权，bStocks 决定这个价能不能变成市场价格
如果我们把价格、成交量、交易频次、盘口和股票等等数据放在一起比较后，bStocks 的定位将远超所谓的 “tokenized stock”。
Perp 以后将会成为新的衍生品宠儿，除了交易量、监管、税收、操作之外，还是因为华尔街最终会知道 OI > 股票的意义。OI 就是钱，而且还无需稀释控制权、无需对外披露、无税收管制的钱。
Binance 如果要争传统股票闭市后的定价权，前面冲出去的是 Perp。NVDA 的一段样本里，Perp 成交量达到 bStocks 的 99 倍；SNDK 六个纯周末成交 29.22 亿美元；SPCX 六个纯周末成交 15.46 亿美元；SKHYNIX 六个 UTC 周末窗口累计超过 24 亿美元。这些数字说明，传统股票关门以后，有一部分风险交易正在迁移到 24/7 衍生品市场。
同一批数据也说明，Volume 和 Price Discovery 不能画等号。SNDK 一个周末几亿美元可以把方向看反，四只股票合计 4.61 亿美元也可以一起错。SPCX 加入后，25 个美国闭市—重开样本的 Sunday 方向是 13/25，仍然只有 52%。SNDK 的 29.22 亿拆开以后是每秒约 7.3 个 fills，SPCX 的 15.46 亿则是每秒约 3.45 个 fills；这些高周转数字不能直接解释成同等规模的独立投资意见。
Perp 解决了“市场可以继续报价”的问题，但一个价格要获得可信度，还需要解决“报价错了以后谁来修正”的问题。
bStocks 就是这个答案。它可以成为做市商 hedge Perp 的库存腿，成为 basis trader 的现货腿，成为长期投资者的底仓，成为 Lending 的 collateral，成为 DEX LP 的股票资产，也可以通过 Stock Conversion 管理跨时段 inventory。如果 borrow 补齐，它还会成为空头可以使用的证券库存，让高估的一边也能被套利。
所以 Perp 和 bStocks 的关系应该是：
Perp 负责生产第一版价格，bStocks 负责把第一版价格变成一件可以被持有、融资、搬运和证伪的资产。
有一天，如果星期六 NVIDIA 出现重大消息，NVDAUSDT 的价格先动了，NVDAB 跟着重新定价，Perp-bStocks basis 拉开，borrow rate 变化，DEX LP 开始被搬，做市商调整库存，套利者压缩价差；随后美国 Premarket 上线，再到 09:30 Opening Cross，那时候值得观察的已经不是 Binance 周末有没有猜对，而是 
谁的价格向谁靠拢。
如果 Binance 一直在 Premarket 出现以后追着传统市场跑，它是一家 24/7 股票交易所。如果 Cash Market 重新开门以后，开始向过去几十小时在 Perp、bStocks、DEX、Lending 和库存市场里反复交易出来的价格靠拢，而且外部 OTC、风控和行情系统也开始引用这套价格，那么 Binance 拿到的就不只是多几个交易小时，而是：
股票市场的定价权。
这个才是迈向30亿用户的底气。
后记
如果想知道更多关于如何在 Binance上做市、套利 bStocks的技巧，欢迎关注 我的substack ，https://substack.com/@agintender ，我会在这里分享我的实际操作经验，以及 bStocks目前的不足、缺陷以及交易机会。
最后
仅以此文献给那些陪我走过童年的长辈们
死亡并不难面对，难面对的是还活下来的人该怎么继续。。。  
一路生花，一路走好
