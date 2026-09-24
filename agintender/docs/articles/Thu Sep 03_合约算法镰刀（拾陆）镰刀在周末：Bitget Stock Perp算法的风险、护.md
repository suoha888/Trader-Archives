# 合约算法镰刀（拾陆）镰刀在周末：Bitget Stock Perp算法的风险、护栏与操纵面

> **作者**：danny (@agintender)  
> **发表日期**：Thu Sep 03 07:49:51 +0000 2026  
> **原文链接**：https://x.com/agintender/status/2095418983327605214 (Article: https://x.com/i/article/2095407947325317120)  
> **全文字数**：6439 字  

---

星期六，NASDAQ关门，NVDA没有现货价格，但Bitget上的Stock Perp还在交易。问题来了：如果华尔街不报价，谁有资格告诉你NVDA现在值多少钱？
Bitget的答案，是让自己的orderbook接班：2,000 USDT验盘口，300秒EMA慢慢认价，再用±10%的Index围栏和Mark限制防止价格跑太远。——这么做的目的就是为了要让Mark（标记价格）price会在周末随市场波动而变动，但是又不太要太出格。
听起来很稳，但真正危险的地方也藏在这里——当Index和Mark都开始听自己家的盘口，价格发现和自我循环之间，只差一张变薄的周末orderbook。
一、华尔街关门以后，谁来给股票报价？
Stock perp有个很现实的问题：股票会收盘，但世界不会。
星期五纽约下午四点以后，NASDAQ和NYSE关门，NVDA、TSLA这些股票不再产生新的现货成交，但星期六照样可能打仗，特朗普照样可以发帖，BTC更不会因为华尔街休息就停下来。既然Bitget上的NVDA、MSTR、TSLA perpetual还在24小时交易，那周末突然冒出来的新消息，总得有一个地方先反映。
以前最省事的办法，是美股收盘以后把Index锁在周五闭市的价格。星期五NVDA是100，星期六哪怕perp里面已经交易到105、108，Index还是100，等星期一再接回美股。这么做稳，但如果周末真的出了大新闻，Last、Index、Mark和funding就可能越拉越开。
Bitget在2026年6月4日改了这个玩法。传统市场关门以后，它不再让Index一直停在最后一个TradFi价格，而是让自己的perp orderbook接班，通过EMA继续往前推。简单说就是：美股开着，听华尔街；美股关了，开始听自己的盘口。
在深入Bitget的算法之前，给大家来个背景知识的补充，何谓Index，Impact、Oracle，Mark price？
 
如果你看到以上的介绍，还是一头雾水，不知所云何物，以下是（烧）省（脑）流版：
Bitget的做法，是让自己的orderbook接班。Index先拿2,000 USDT去“验盘口”，算出Impact Bid / Ask和IPD，再用300秒EMA一点点追：
Index_new = Index_old + (1 − β) × IPD
其中 β = exp(−Δt/300)。到了Mark Price，休市后则改成 Orderbook Quote → EMA → Mark，可以抽象成：
Mark_t = β·Mark_(t−1) + (1−β)·Q_t
最后Mark还要被限制在Index附近：
Actual Mark = clamp(Calculated Mark, Index×(1−d), Index×(1+d))
如果你感觉看懂了，那么恭喜你，可以关闭这个页面，或者转到更高阶的：https://agintender.substack.com/p/48bitget-stock-perp?r=8gs9xi 
如果感觉没看懂？！ 没看懂就对了，那就接着往下看吧～ 
二、外面有价格的时候，Bitget还是先听TradFi （oracle)
正常美股交易时段，Bitget的Stock Perp Index处于External Mode。官方列出的股票数据供应商包括Pyth、dxFeed、Massive和Intrinio，外面有新的股票价格，Bitget就把这些报价组成自己的External Index，大约每200ms更新一次。
这个时候Bitget没必要自己决定NVDA应该值多少钱。NASDAQ、NYSE里面有股票、ETF、期权、做市商和大量机构资金，整个传统市场的信息量摆在那里，Bitget只需要把这个价格搬进perp。
周末、节假日、每日维护，或者超过一半的外部价格源超过两小时没有更新，Index就会切进Internal Mode；等大部分外部价格源恢复，再切回External Mode。
所以Bitget的态度其实很简单：外面有人说话，我听外面；外面没声音了，我看场内的orderbook和交易。
三、第一关：不是看Last，而是拿2,000 USDT进去验牌
星期六的股票perp最容易骗人的，是Last Price。
 
Last只告诉你上一笔交易在哪里成交，却不告诉你那个价格后面有没有真的流动性。假设NVDA星期五最后的External Index是100，周末盘口很薄，有人用一笔小单把Last打到108。如果直接拿Last做Index，那几十、几百USDT就可能把整个参考价格打高8%。
所以Bitget先设了一笔：
Impact Notional = 2,000 USDT
然后拿这2,000 USDT分别模拟扫bid和ask，算出：
P_impactBid
P_impactAsk
Impact Price看的是这2,000 USDT真正扫进盘口以后，平均能够在哪里成交：
Impact Price = 累计成交金额 ÷ 累计成交数量
举个例子：有人用50 USDT把Last打到108，但你真的拿2,000 USDT进去，绝大部分还是只能在100、101成交，那这个108的水分可想而知。
但如果周末真出了大消息，100附近卖盘撤掉，新的bid已经堆到106、107，ask也搬到108，那么2,000 USDT真的扫进去，也只能在107、108附近成交。这个时候系统看到的就不是一根针，而是整张能成交的盘口都开始移动了。
所以Last是在告诉你“刚刚有人在哪里成交”，Impact Price是在问：“如果我现在真的拿钱进去，这个价格还能不能成交？”
四、第二关：IPD加300秒EMA，你得在那里待一阵子
验完盘口以后，Bitget没有直接拿Impact Bid和Impact Ask的平均值做Index，而是先算一个IPD：
IPD = max(P_impactBid − S, 0) − max(S − P_impactAsk, 0)
这里的S就是当前Internal Index。
这公式看起来麻烦，其实只是看Index有没有掉出Impact Bid和Impact Ask形成的可成交区间。比如Index是100，Impact Bid已经107、Impact Ask是108，说明整个盘口都在Index上面，IPD为正，Index开始往上追。反过来，如果Index是108，而Impact Bid和Ask只有100、101，IPD就是负数，Index往下走。
如果Impact Bid是99.8、Index是100、Impact Ask是100.2，Index本来就在这个区间里面，IPD就是0，系统没必要乱动。
所以Bitget不是一直在追Last，而是在看：我的Index有没有掉出真正能够成交的价格走廊？
接下来才是EMA：
S_new = S_old + (1 − β) × IPD
其中：
β = exp(−Δt / τ)
Δt = min(Δt, c × τ)
默认参数是：
τ = 300秒
c = 0.1
更新频率 = 200ms
300秒就是5分钟。为了方便理解，如果假设输入一直不变，那么30秒大概吸收9.5%的变化，1分钟18.1%，3分28秒左右吸收一半，5分钟63.2%，10分钟86.5%。
但这只是理论时间尺度。真实市场里，Index越接近Impact Bid，IPD就越小；一旦Index重新进入Impact Bid和Impact Ask之间，IPD可能直接变成0。
 
所以“五分钟EMA”的意思不是五分钟一定追到新价格，而是：一张新的盘口不能只出现一秒，你得在那里持续一阵子，Bitget才会慢慢相信你。这无形中增加了操纵成本。
c=0.1也不是说价格一次最多涨10%。因为c×τ=30秒，它限制的是单次EMA使用的有效时间。即使系统中间停了几分钟，恢复以后也最多按照30秒计算，一次最多吸收大约9.52%的当期IPD，避免恢复时突然插针。
五、第三关：就算有人操纵盘口，Index外面还有一道±10%的墙
如果只有Impact Price和EMA，只要整个orderbook长时间待在一个新位置，Internal Index理论上还是可以一直追过去。
Bitget没有把这个权力全部交给自己的perp market。
休市期间，系统拿最后一个有效的External Price当reference，Internal Index默认只能在它上下10%以内活动。
假设NVDA星期五最后是100，那么周末Internal Index默认就在：
90 ≤ Internal Index ≤ 110
星期六如果真出了超级大利好，Last可以有人在120、125成交，Impact Bid和Ask也可以整个搬过去，但Internal Index到了110附近，就过不去了。
所以Bitget允许的不是完全自由的price discovery，而是有限的重新定价。它愿意让星期六的crypto market先对NVDA投票，但不愿意在NASDAQ回来以前，把上市公司的Reference Index完全交给一张周末流动性更薄的perp orderbook。
以后如果看到Last已经125，Impact盘口也在120以上，但Index只有110，不代表Bitget没看到新价格，而是它看到了，但风险系统只愿意认到这里。
六、问题来了：周末的orderbook到底有没有货？能不能成交？
讲完算法以后，实际的情况是怎么样：星期六的orderbook到底有没有交易、有没有仓位、有没有资格给股票重新报价？
 
Block Scholes用Bitget公开API和historical order book data做过研究。2026年5月14日，Bitget的NVDA-USDT perp在mid price上下2%范围内，单边daily median resting depth大约有410万美元。拿Bitget BTC/USDT现货做参照，同口径大约550万美元。也就是说，活跃时段的NVDA perp盘口已经不是一个小玩具市场。
但到了周末，成交量会掉很多。Block Scholes统计2025年9月至2026年5月的数据发现，Bitget这些RWA perp周末成交量相对工作日普遍减少65%到90%。NVDA少88%，QQQ少87%，SPY少67%。成交虽然少很多，但top-of-book spread没有同比例扩大，说明做市商并不会因为周末而消失。
不同股票的差别也很大。2026年8月28日星期五，Bitget MSTR perpetual成交约3550万美元；星期六还有910万美元，星期日1090万美元。更有意思的是OI，三天大概是1480万、1510万、1620万美元。成交少了，但持仓仓位却没同比例减少。
MSTR会这样不奇怪，因为它背后是BTC。BTC如果周末突然大涨，MSTR对应的风险和市场对星期一合理价格的预期也会跟着变，信息很自然会先跑进MSTR perp。
但TSLA的相关性就没这么强。同一个周末，Bitget TSLA perp从星期五约1350万美元成交，掉到星期六约83万美元、星期日约100万美元。也就是说，周末单日只剩星期五的6%—7%左右。
这刚好解释了Bitget为什么不能简单说“周末全部听自己的orderbook”。MSTR背后还有BTC这条24小时信息链，TSLA周末却可能一下少掉九成成交。Impact、EMA和±10% band，说到底都是在解决一个问题：这张星期六的盘口，我到底敢信多少？
2026年2月28日还有一个更好的现实案例。当天是星期六，美国对伊朗发动打击，美股没有开盘，但Bitget上的RWA perp继续交易。Block Scholes记录到，Gold perp大约涨200bps，NVDA跌44bps，QQQ跌31bps，SPY跌14bps。与此同时，NVDA的bid-ask spread从约0.6bps扩大到3.4bps，QQQ从3.7bps扩大到11.8bps，盘口深度也明显下降。
这至少证明一件事：传统市场关门以后，Bitget自己的perp会吸收新信息并重新报价。
但这还不能直接证明周末perp已经完成了“正确的价格发现”。要证明这一点，还得看星期一NASDAQ重新开门以后，周末perp给出的价格是不是比星期五旧价格更接近真正的开盘成交。
七、Mark price的结构
这里以Bitget 2026年4月28日发布的Stock Perps说明：传统股票市场正常交易的时候，Mark Price使用Standard Method；传统市场休市以后，Mark Price改成：
Order Book Quote Data → EMA → Mark Price
这说明周末以后，不只是Index开始听自己的orderbook，Mark也开始从自己的盘口里面拿信息。
但Mark这套EMA没有Index那么透明。Bitget没有继续告诉你order book quote具体取Best Bid/Ask mid、Impact Price，还是经过别的处理；也没有公开这台EMA的β、τ和half-life。
所以不能因为Index的τ是300秒，就想当然第认为Mark也是300秒。我们只能确定：休市Mark会听orderbook quote，而且会经过EMA平滑；这台EMA到底多快，目前没有公开。
此外，Bitget另外还有一道Mark deviation constraint：
Actual Mark = clamp(Calculated Mark, Index × (1 − d), Index × (1 + d))
目前NVDA、TSLA、MSTR、COIN等很多主要stock perp的d是5%。
比如Internal Index是102，场内价格已经跑到108，Calculated Mark也算到108，那么最终Mark最多就是：
102 × 1.05 = 107.10
所以Index外面的±10%和Mark相对Index的±5%并不是一回事。Index影响Mark，而Mark决定是否清算。 
前者在限制周末Reference Index能走多远，后者在限制真正拿来算PnL和强平的Risk Price能离Index多远。
最后
随着Tradfi/RWA的产业链和交易逐渐成为了交易所的主流交易，将会衍生出不同的交易方式、套利机会和投资组合。我相信Stock perp在不久的将来，将会成为新的金融基础设施，而了解底层的算法和机制将有助于我们了解这个未来形态的金融战争机器。
如果对各家交易所的算法的内容感兴趣的，也可以关注我的substack：https://substack.com/@agintender ， 目前已经分享了Binance、Trade.xyz ，OKX ，Bitget，Gate等交易所的合约算法。 
知其然，且知其所以然。
后记
Last、Mark和Index之间的距离
说到这里以后，最值得看的已经不是“300秒EMA是什么意思”，而是星期六真的出了新闻以后，Last、Mark和Index到底谁先动、谁落后、又花多久重新靠在一起.......
欲知后事如何，还请移步substack：
https://agintender.substack.com/p/48bitget-stock-perp?r=8gs9xi
