# 合约算法镰刀（拾伍）：揭秘币安Stock Perp的Oracle算法及周末定价权的核心

> **作者**：danny (@agintender)  
> **发表日期**：Thu Aug 27 10:13:42 +0000 2026  
> **原文链接**：https://x.com/agintender/status/2092918469385969881 (Article: https://x.com/i/article/2092878928079962112)  
> **全文字数**：7471 字  

---

1987年的《华尔街》里，一笔股票订单从电话那头传进纽约证券交易所，书记写ticket，runner拿着单子穿过交易大厅，交易员在一片叫喊声里完成成交，新的价格再通过ticker传出去。今天手机上按一下按钮就结束的事情，当时是真的要靠人在交易大厅里跑。
《繁花》里的大上海也差不多。九十年代初，浦江饭店孔雀厅里坐着红马甲，大屏幕不停跳报价；再早一点，阿宝想买股票，还得让陶陶拿着现金去柜台买。交易大厅先有人喊出新报价，ticker才会跟着动；柜台有人买卖，行情板上才会出现新数字。但是人头攒动的时刻只会持续到下午4点。
 
休市，意味着结束。
Stock perp这个7 x 24物种的出现给这个看似平常的场景出了道难题。
假设星期五NVDA闭市价是100美元，Nasdaq关门。星期六英伟达突然出了重大新闻，有人觉得星期一应该是105，有人觉得应该是108。股票市场没开，没有新的NBBO，但Binance上的NVDA perpetual还在交易。107有人买，108有人卖。
问题就来了：
原来的交易大厅关灯以后，谁来接过报价板？
正常情况下，链条是：
股票市场成交 → Data Vendor → Binance Price Index → Mark Price
但到了周末，外部股票报价停了，Binance还要让这张24/7交易的perp继续报价、计算盈亏、收保证金和处理清算。总不能一直抱着星期五的100美元等到星期一。
于是2026年5月，Binance做了一件关键的事情：外面的股票市场不报价以后，它开始让自己的perp orderbook参与Price Index （oracle喂价）的产生。（有懂行的朋友们知道26年5月发生了什么事吗？！）
严格来说，Binance官方把它称为 Price Index Methodology 和 Mark Price Methodology，并不是单独一套“Oracle算法”。但从信息传播链来看，它干的就是Oracle的活儿：外部价格源掐断以后，到底拿什么继续告诉风险系统，“NVDA现在大概值多少”。
公式复杂只是这套算法的表象，关键点是它给价格安排了几层过滤网：
Orderbook → Impact Bid / Ask → Impact Mid → EWMA → Price Index → Mark Price → Margin / Liquidation
Binance周末不是简单地说：“场内成交多少钱，我就认这个标的现在值多少钱。”
它更像是在问：
“你们说NVDA值108？可以。先让我看看108后面有没有盘口，能不能持续，再决定这个108有多少资格进入Index。”
看不懂？没关系，拿上你的小咖啡，一起一步步的走进这套休市算法里。
 
一、先把三个价格搞清楚：Last、Index和Mark
看Binance stock perp，最容易搞混的是Index、Last和Mark。
假设星期五NVDA收100，到了星期六，可能同时出现：
Price Index：101
Last Price：108
Mark Price：103
 
三个价格都是NVDA，但回答的是不同问题。
Last Price就是刚刚最后一笔真实成交。有人用一张市价单把薄薄的卖盘扫到108，Last就是108。它最接近“刚才有人在哪里成交”，也最容易被薄盘口打一根针。
Price Index是Binance风险体系的参考价。美股正常交易时，它主要来自外部Data Vendors；到了周末和节假日，equity TradFi Perps进入Orderbook EWMA Mode，Price Index改从Binance自己的Global Orderbook里计算。2026年5月16日起，这套模式取代了旧的Fixed Mode。
Mark Price才是风险系统最关心的价格。它参与保证金和清算判断，所以你可以在108成交，但不代表系统马上承认NVDA“值108”。
所以这篇文章真正研究的是：
星期六没有Nasdaq报价以后，Binance怎样把场内交易者的买卖意愿，一步一步加工成一个敢拿去做风险管理的价格。
二、2026年5月16日：Nasdaq下班，Binance自己的盘口开始接班
旧的Fixed Mode很简单：外部股票价格一旦不可用，Price Index就停在最后一个有效值。星期五NVDA是100，周末就继续拿着100。
这样做的好处是安全、保守，但问题也明显。
星期六如果英伟达出了重大新闻，Binance自己的NVDA perp已经交易到105、108，Index却还抱着100不放，这个“参考价”反而脱离了市场。
所以Binance切到了 Orderbook EWMA Mode。
休市后的链条变成：
Binance Global Orderbook
↓
Impact Bid / Impact Ask
↓
Impact Mid
↓
EWMA
↓
Price Index
这一步改变的不只是算法。
正常交易时，是Nasdaq先交易，Data Vendor再把结果传给Binance：
Nasdaq → Data Vendor → Binance
到了周末，则变成：
Binance交易者 → Binance Orderbook → Binance Index
至少在Nasdaq没有新价格的这段时间里，Binance开始生产一个属于自己市场的NVDA参考价。
三、第一道过滤：别拿Last骗我，先看看盘口
这里是Binance整套Perp算法很关键的一层，看订单簿Impact的冲击，也应用到Stock perp。
 
假设NVDA星期五收100。星期六盘口很薄，有人拿一笔不大的市价单，把最后成交打到了108。
如果Binance直接用Last：
100 → 108
风险控制几乎没法做。
所以Binance不会只看最后一笔成交，而是计算 Impact Bid Price 和 Impact Ask Price。
它问的是：
假设现在有一笔指定规模的订单进来，按照眼前的盘口，平均会成交在哪里？
这笔规模由 Impact Margin Notional 决定：
Impact Margin Notional = 200 USDT / Initial Margin Rate at Maximum Leverage
假设某张股票perp最高杠杆是10倍，对应Initial Margin Rate约10%，那么：
Impact Margin Notional ≈ 2,000 USDT
注：这里只是举例，实际数值要看对应合约的杠杆和保证金参数。
假设Last已经被打到108，但100—101附近还有大量挂单。那么模拟一笔2,000 USDT的订单进去，平均成交价可能还在101附近，Impact Ask就不会跟到108。
反过来，如果真的出了重大新闻，100附近的卖盘撤掉，新的bid堆到107，ask堆到108，而且这个区域有足够深度，Impact Bid和Impact Ask才会一起往上走。
接下来：
Impact Mid = (Impact Bid + Impact Ask) / 2
所以Impact这一层的意思是：
你说NVDA值108没问题，但别只拿一笔108给我看。你得让一整段可以执行的盘口也搬过去。
Last看的是一个点；Impact Price看的是盘口和订单簿结构。
这是第一道过滤。
四、第二道过滤：盘口搬到108了，也得在那里待一会
即使Impact Mid已经从100移动到108，Binance也不会马上把Price Index改成108。
 
后面还有EWMA。
Orderbook → Impact Mid → EWMA → Price Index
EWMA可以简单写成：
EWMA(t) = α × P(t) + (1 − α) × EWMA(t−1)
α越大，系统越快相信新价格；α越小，过去价格的权重越大。
说得直白一点就是：
108我看见了，但你先在那里待一会。
如果Impact Mid只跳到108几秒钟，很快又掉回来，EWMA不会全部吃进去。
如果新的bid和ask持续在107—108附近，Impact Mid一直站在那里，Index才会逐步被拉过去。
Binance公开文件只写 “EWMA determined by Binance RCH”，没有公开α、half-life或者τ，同时还说明Index movement本身有限制。
这样看，前两层过滤的分工就很清楚了。
Impact Price过滤空间：你要把一段盘口搬过去。
EWMA过滤时间：你还得让这段盘口站得住。
一个负责问“后面有没有钱”，另一个负责问“这个价格能不能持续”。
所以Binance防的并不只是一笔坏成交，还有判断是不是“假的价格发现”。
Last跑进来说：“我看到108了。”
Impact Price问：“108附近到底有多少盘口？”
EWMA再问：“这些盘口待多久了？”
两道闸门都过以后，这个价格才慢慢纳入Index的参考范围。
五、第三道保护：为什么Mark周末只能离Index跑3%
接下来还有一道屏障。
Binance当前规则下，equity TradFi Perps的Mark Price相对Price Index，在weekend和holiday通常最多偏离±3%；其他session一般是±5%。
这里最容易误解的是：
±3%不是说NVDA周末最多只能涨3%。
它限制的是：Mark相对当前Index最多能跑多远。
 
假设Index还是100，但场内算出来的Mark已经到了106，那么Mark上线被卡在：
100 × 1.03 = 103
但如果EWMA继续把Index推到102，Mark上限就变成：
102 × 1.03 = 105.06
如果Index来到105：
105 × 1.03 = 108.15
所以这不是一堵固定的值，更像是随着时间和价格波动的防护栏。
Index往前走一步，Mark的活动范围也跟着往前。
这样做的目的，是允许周末市场继续产生新价格，但同时又能降低Mark突然远离Index的概率，直接把一大片杠杆仓位打爆清算。
六、周末结束以后，两套价格不能直接硬切过去
还有一个容易被忽略的问题：两套价格体系换班的时候怎么办？
星期五外面的股票市场还开着，Binance Price Index主要跟着Data Vendor。
到了周末，系统切换到：
Global Orderbook → Impact Mid → EWMA
等外部市场重新有价格，又要roll回来。
问题是，两套价格可能差很多。
假设Binance周末Index是108，外部价格恢复以后是104。
如果直接：
108 → 104
这4美元不是市场交易出来的，而是算法换挡roll over的间隙造出来的。
所以Binance使用weighted blend渐进切换：
Price Index = (1 − t / Window Length) × Old Mode Index + (t / Window Length) × New Mode Index
当前Clearing Procedures把：
Window Length = 30 seconds
写进了规则。
于是大概会变成：10秒：106.67；15秒：106；30秒：104
 
不是一秒钟从108跳到104，而是用30秒慢慢完成交接。
这不是为了让K线好看、也不是为了不让社区在x上骂而已
它是在防止：因人为定价制度本身制造不必要的波动。
七、把五层机制连起来，Binance到底做了什么？
Price Index从外部Oracle切换场内Oracle的转变路径：
Nasdaq / Data Vendor下班
↓
Binance Orderbook接班
↓
Impact Bid / Ask检查可执行深度
↓
Impact Mid形成场内参考价
↓
EWMA检查价格能不能持续
↓
Price Index逐渐移动
↓
Mark受到deviation限制
↓
Margin / Liquidation
看着复杂，实际上可一点都不简单，每一步都有自己的作用：
Impact Price防的是针。 别拿一笔108来骗我，你得把一段orderbook搬过去。
EWMA防的是阵风。 搬过去还不够，你得在那里待一阵。
Index movement limit控制速度。 Index不是毫无约束地追盘口跑。
Mark deviation保护清算系统。 周末Mark不能一下离Index太远，要异动也要慢慢来。
30秒transition负责换班。 外部市场和Binance orderbook切换的时候，不要自己打出价格断层。
什么？！你说还是太复杂？
单独看每一条的论述，确实有点枯燥，但如果你把思路打开，把整个结构联动起来，它其实是在连续追问几个问题：
有没有人在这个价格交易？
看orderbook。
2. 后面有没有足够的盘口？
看Impact Price。
3. 这个价格能不能站住？是不是真的市场价格
看EWMA。
4. 够不够资格进入风险系统？
看Mark和deviation constraint。
5. 外面的股票市场醒了，怎么把报价板交回去？
用transition。
ps：如果你通篇都没看懂，至少记得这5个问题就足够了。
八、所以Binance到底是在跟踪股票，还是开始生产股票价格？
Nasdaq开门的时候，答案很简单。
NVDA在股票市场里发生大量交易，外部Data Vendor把价格送给Binance，Binance再计算自己的Index和Mark。
这时候Binance是一个price taker。股票市场先说话，Binance听。
但到了周末，关系变了。
Nasdaq没有新成交，外部vendor没有新的股票价格，Binance的NVDA perp却还在24小时交易。
有人觉得星期一应该105，就去105买；有人觉得值108，就把ask撤到108；做市商看到新闻以后重新调整库存，原来100附近的流动性逐渐消失。
这些orderflow先改变Impact Price → Impact Price推动EWMA → EWMA再推动Index。
于是一个原本只属于Binance场内的价格判断，开始获得“参考价格”的身份。
所以2026年5月的Orderbook EWMA升级改变的不只是一个参数。
以前是：Nasdaq负责生产价格，Binance负责复制；
现在到了没有外部报价的时段，它变成：
Binance交易者先把信息交易出来，订单簿负责提取盘口和价格，Impact检查有没有深度，EWMA检查能不能站住，最后算法决定它有没有资格进入Index。
Binance从纯粹的价格接受者，变成了一个有条件的价格生产者。
当然，Binance周末交易出来的108，并不等于NVDA股票的“真实价格”。
它生产的是“Nasdaq沉默期间，Binance市场对下一份股票价格的可交易共识”。
而这个价格到底是不是共识，还是噪音，要等星期一重新开盘后方见真章。
九、考试结果要等Nasdaq重新开门方见分晓
假设星期六英伟达出了新闻，Binance NVDA perp先从100交易到108，Impact Price跟过去，EWMA Index也慢慢来到107、108。
接下来才是重点。
如果其他market maker看到Binance这个价格，会不会调整其他stock perp的报价？
如果套利机器人同时在几个venue做市，Binance的变化会不会通过inventory management传出去？
到了星期一Nasdaq开门，NVDA第一笔、前一分钟、前五分钟的成交，到底更接近星期五的100，还是Binance周末的108？
从过往的数据（2026年7月）来看，这个周末定价权的争夺战正在往Stock perp的方向靠近，从下表中，我们能看出距离美股开盘30分钟前的差距已经控制在100bps以内了：
 
 
关于详细的数据分析，有兴趣的小伙伴欢迎移步： https://x.com/agintender/status/2088240935276876180?s=20
结语：价格是实时流动的，只是换了个显示屏
从《华尔街》里拿着ticket跑过交易大厅的runner，到《繁花》里盯着行情板的红马甲，再到今天Binance服务器里不断计算的Impact Price和EWMA，金融市场已经完全换了样子。
但底层问题没有变：
一条新信息出现以后，总得有人拿真金白银表达。
过去，这个地方是NYSE，是Nasdaq，是上海证券交易所。
股票市场关门以后，这个位置暂时空出来。
Binance现在做的，就是在这段空白时间里摆了一张新的报价板。
它不直接相信最后一笔成交，也不继续抱着星期五的收盘价，装作世界没有变化，而是要求自己的交易者用盘口深度和时间证明一个新价格，再把这份证明逐渐写进Index。
所以Orderbook EWMA表面上只是一套休市算法。
往深一点看，它回答的是另一个问题：
当Nasdaq不说话的时候，谁有资格先说NVDA值多少钱？
价格是什么固然重要，但知道价格从哪里来更重要。
知其然，且知其所以然
后记
那你说Binance这套前无古人的 休市后的Stock perp的 Oracle 算法会不会有问题？怎么通篇都是歌颂赞美之词？难道就没有限制和风险？
哈哈哈，这必然是有的，而且风险和影响还不小。
如果你看完之后，仍然感觉意犹未尽，或者还有一些讲解不到位的地方，我们把完整版的内容放到了 substack，有兴趣的小伙伴可以移步：
https://agintender.substack.com/p/nasdaqstock-perporacle247?r=8gs9xi&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true
