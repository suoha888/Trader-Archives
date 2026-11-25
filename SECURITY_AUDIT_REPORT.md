# Trader-Archives 全栈安全审计报告（5 层并行集群审计）

> **审计日期**：2026-11-25  
> **审计范围**：`d:\Codex\顶级 KOL数据` 全工作区（涵盖公开 GitHub 仓库 `suoha888/Trader-Archives` 全部 93 个历史提交与 18 个静态网页、Vercel Edge AI 网关、164 个 Python/JS 流水线脚本、Skills/HTML 模板库及 1,160+ 数据湖文件）  
> **审计方式**：5 路专业安全审计集群并行全量只读取证（AST 静态分析 + 正则/熵值凭据考古 + Node.js V8 PoC 复现 + 跨层契约交叉核验）  
> **脱敏声明**：本报告中所有发现的真实密钥、Token 与敏感凭据均已脱敏（仅展示前缀/末位与长度），严禁回显完整密钥。

---

## 一、执行摘要（Executive Summary）

本次全栈 5 层安全审计累计检查 **18 个 HTML 页面、4 个 Serverless 网关文件、164 个流水线可执行脚本、17 个 Skill/模板与根目录治理文件、93 个 Git 历史提交（1,419 个文本 Blob，861.1 MB）及 1,179 个数据湖文本文件**。经跨层去重与人工逐行复核，确认 **34 项真实有效安全发现**（零误报），风险分布如下：

| 架构层 | 审计对象 | CRITICAL | HIGH | MEDIUM | LOW / INFO | 小计 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Layer 1 · 前端与客户端 Web 层** | `01_Trader-Archives` 总站 + 17 子站 | 0 | 2 | 3 | 3 | **8** |
| **Layer 2 · Serverless AI 网关层** | `05_AI_Mentor_Gateway_Vercel` | 0 | 3 | 3 | 2 | **8** |
| **Layer 3 · 数据流水线与脚本层** | `04_Pipeline` + `01_` 本地工具脚本 | 2 | 4 | 4 | 2 | **12** |
| **Layer 4 · Skills、模板与供应链层** | `03_KOL--ziliao` + `.agents/skills` | 1 | 3 | 4 | 1 | **9** |
| **Layer 5 · Git 历史与数据湖考古层** | `01_/.git` 全历史 + `02_` + `06_` | 1 | 2 | 3 | 1 | **7** |
| **去重后独立根因总计** | **全栈 5 层** | **4** | **11** | **13** | **6** | **34** |

> *注：部分跨层关联问题（如 `FE-02`/`PL-08`/`GIT-02` 的 `wallstreet0name` 第三方 `sk-` 密钥入库、`FE-04`/`PL-05`/`GIT-03` 的 `<script>` 内联 JSON 未转义、`FE-01`/`GW-01`/`GW-02` 的 AI 网关信任边界、`TM-01`/`PL-02`/`GIT-01` 的历史 23–30 枚 `atr_` 密钥传播链）在各层均保留独立编号以明确对应代码修复落点，汇总表已按独立根因去重。*

### 最紧迫的 4 项 CRITICAL 发现（需立即响应）
1. **[GIT-01] 公开 GitHub 历史永久暴露 45+ 个真实生产 AI API Key**：`suoha888/Trader-Archives` 历史 66+ 个提交中保留了 15 枚 `api.b.ai` (`sk-*`) 与 30+ 枚 `api.atria-asi.ai` (`atr_*`) 真实高熵密钥；GitHub 默认 Secret Scanning 无法识别 `atr_` 前缀。
2. **[PL-01] 采集脚本硬编码永久有效（无 `exp`）`ai.6551.io` HS256 JWT Token**：`collect_all_gch_arbitrage.py:10` 与 `harvest_gch_arbitrage.py:10` 明文写入 208 字符无过期时间 Bearer JWT。
3. **[PL-02] 15 个遗留 Stage 4 建站脚本硬编码 30 枚 `atr_*` 密钥（349 处）**：任意误运行即向公开 `index.html` 二次泄露密钥。
4. **[TM-01] `03_KOL--ziliao` 旧版 Skill 与即插即用 HTML 模板硬编码 23 枚 `atr_*` 密钥（65 处）且保持 `user-invocable: true`**，并与 `TM-03`（`git add -A` + 自动 `git push origin main`）形成高危误触发链路。

### 其余高危（HIGH）核心风险
- **Windows 平台 OS 命令注入（`PL-03`）**：现役 `harvest_kol_v5.py`、`classify_kol_llm_v5.py`、`incremental_harvest_ws0n.py` 使用 `subprocess.run(..., shell=(os.name == "nt"))` 拼接未校验的 `tid`/`handle`，上游数据投毒即可在开发机触发 `cmd.exe` 命令执行（RCE）。
- **SSRF 与 `file://` 本地文件读取（`PL-06`）**：现役 v5/v6 脚本使用原生支持 `file://` 的 `urllib.request.urlopen()`，且仅用 `"pbs.twimg.com" in murl` 子串匹配、`av_url`/`bn_url` 零校验、读取无字节上限。
- **AI 网关防滥用与提示词劫持缺口（`GW-01`, `GW-02`, `GW-03`, `FE-01`）**：可伪造 `Origin` + Edge 内存 `Map` 限流失效 + 客户端任意控制 `role: "system"` 导致可被当作免费通用 LLM 代理刷爆额度；部署脚本跨项目复用交易工程 `cb-desk/.env` 密钥并向 `preview`/`development` 下发、全局关闭 `ssoProtection`。
- **模板与生成器二阶 XSS（`TM-02`, `PL-04`, `PL-05`, `FE-03`, `FE-04`, `GIT-03`）**：旧模板 `renderSimpleMarkdown()` 已在 Node.js V8 实测复现零交互 `@keyframes` `onanimationstart` DOM XSS；现役 v5/v6 生成器与 16 个子站存在 `escHtml` 漏转义单引号（`onclick="showModalImage('...')"` 逃逸）、`href` 缺 `https?://` 白名单、`cached.ragCount` 未数值化及 `<script>` 内联 JSON 未转义 `<`/`>`/`&`/`U+2028`。
- **公开数据湖与 RAG 明文收录第三方 `sk-*` 密钥（`FE-02`, `PL-08`, `GIT-02`）**：`wallstreet0name/data/` 6 个文件（含 `ai_rag_index.json`）及 `02_` 镜像原样保留了推文中的 51 位真实格式 `sk-XPjnsaf****De37`。

---

## 二、分层详细安全发现（Layer-by-Layer Findings）

### Layer 1：前端与客户端 Web 层（`01_Trader-Archives_14位KOL全量网站与数据湖`）

| 编号 | 级别 | CWE / OWASP | 位置与影响面 | 核心缺陷与复现说明 | 修复方案 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **FE-01** | **HIGH** | CWE-602 / LLM01 | 16/17 动态子站 `*/index.html`（含 `thankucrypto` 与未跟踪 `17zxhold`） | 前端构造并发送 `role: "system"`、`model`、`max_tokens`，3 轮对话/300 字上限仅在客户端 JS 校验；`rag.block` 与用户提问直接拼接无不可信边界标签。 | 网关层强制 `systemPrompt` SHA-256 白名单 + 服务端硬编码模型 + 服务端不可覆盖防注入声明；前端将 `rag.block` 包裹在 `<untrusted_archive_excerpts>` 中。 |
| **FE-02** | **HIGH** | CWE-798 / CWE-200 | `wallstreet0name/data/` 6 个文件（含 `ai_rag_index.json`） | 推文 `2000843101716508867` 中自购中转站 API 密钥 `sk-XPjnsaf****De37`（51 chars）未经脱敏直接进入公开数据湖和 RAG 索引，AI 助手可直接检索复述。 | 立即脱敏全部派生公开文件（遵守 `AGENTS.md` 不修改 `*_ultra_raw.json` 原备）；流水线与 RAG 构建器新增统一出站 Secret Redactor。 |
| **FE-03** | **MEDIUM** | CWE-79 / A03 | 16/17 动态子站 `*/index.html` | ① `escHtml()` 漏转义单引号 `'`，导致动态 `onclick="showModalImage('${escHtml(p)}')"` 存在属性内 JS 字符串逃逸；② 动态 `tweetUrl`/`sourceUrl` 未校验 `https?://`；③ `rCls` 未强转整数；④ `sessionStorage` 中的 `cached.ragCount` 未强转 `Number` 即写入 `innerHTML`（全 `suoha888.github.io` 同源共享风险）。 | 废弃动态 `onclick` 改为 `data-modal-src` + 事件委托；`escHtml` 补全 `'` 转义；新增 `safeHttpUrl()` 白名单校验；`rCls` 与 `cached.ragCount` 强制整数化。 |
| **FE-04** | **MEDIUM** | CWE-79 / CWE-116 | 16/17 动态子站 `<script>`（5 站含原始 `<`，`yourquantguy` 含 `U+2028`） | 内联 `FALLBACK_TWEETS`、`EARLY_FALLBACK`、`CJ_AI_CONFIG` 未转义 `<`/`>`/`&`/`U+2028`/`U+2029`，一旦未来推文含 `</script>` 即触发零交互 Stored XSS。 | 统一使用 HTML-safe JSON 序列化（`<`→`\u003c`、`>`→`\u003e`、`&`→`\u0026`、转义 `\u2028`/`\u2029`）。 |
| **FE-05** | **MEDIUM** | CWE-693 / A05 | 全部 18/18 HTML 页面 | GitHub Pages 不支持自定义 HTTP 头，且全部页面 `<head>` 均缺失 `<meta http-equiv="Content-Security-Policy">` 与 `<meta name="referrer">`。 | 为全部页面 `<head>` 部署 CSP 白名单（限定 `connect-src` 仅至自有网关，禁止 `object-src`/`form-action`）及 `strict-origin-when-cross-origin` Referrer 策略。 |
| **FE-06** | **LOW** | CWE-1022 / A05 | 根 `index.html`（16 处外链 + 15 处 `onerror`） | 16 处 `target="_blank"` 缺失 `rel="noopener noreferrer"`；15 处头像 `onerror` 未置空 `this.onerror=null` 且回退第三方 `abs.twimg.com`（网络受限时形成无限报错死循环并泄露访客 IP）。 | 16 处外链补全 `rel="noopener noreferrer"`；15 处 `onerror` 改为 `this.onerror=null` + 本地轻量内联 SVG 占位图。 |
| **FE-07** | **LOW** | CWE-353 / A08 | 18/18 HTML（Google Fonts）；`laoemo/index.html:965`（PDF iframe） | 第三方 Google Fonts 动态 CSS 无自托管/SRI；冻结站 `laoemo` PDF `<iframe>` 无 `sandbox`。 | 通过 CSP 严格收敛 `style-src`/`font-src` 白名单；后续版本可考虑自托管 WOFF2 字体；冻结站 `laoemo/` 保持只读不改。 |
| **FE-08** | **LOW/INFO** | CWE-200 / CWE-538 | `01_` 根目录 4 个 `.gitignore` 忽略文件 | `analyze_kol_profiles.py`、`audit_all_subsites.py`、`full_audit_results.json` 含 `c:\Users\KALOS\Desktop\6551...` 及历史 23-Key 遥测，虽已被忽略未入库但滞留于公开仓库目录内。 | 建议迁出公开仓库目录或删除；同时修复 `.gitignore` 补全忽略规则防误加。 |

> **Layer 1 洁净核验**：当前 18 个 HTML 均 **0 硬编码密钥**、**0 外部 JS CDN**、**0 `eval`/`document.write`/`postMessage`/`location.hash` 注入**；AI 输出 `formatAiExquisiteOutput` 先调用 `escHtml` 且无 Markdown 外链解析，锚点受正则白名单严格约束；冻结站 `laoemo/index.html` 高度洁净。

---

### Layer 2：Serverless AI 网关层（`05_AI_Mentor_Gateway_Vercel`）

| 编号 | 级别 | CWE / OWASP | 位置 | 核心缺陷与复现说明 | 修复方案 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **GW-01** | **HIGH** | CWE-306 / API4 | `api/chat.js:1,16-66,95-137` | 仅校验可由 `curl` 伪造的 `Origin`/`Referer`；Edge Runtime 多 Isolate 内存 `IP_BUCKETS` 跨实例/冷启动失效，且 IPv6 未按 `/64` 归一化，可被脚本绕过限流耗尽付费额度。 | ① IPv6 `/64` 归一化 + 有界内存桶降级；② 内置 Upstash Redis REST 分布式滑动窗口限流支持（环境变量零入侵启用）；③ 建议在 Vercel Dashboard 开启 Edge Firewall WAF 限流与上游硬消费封顶；④ 二阶段接入 Cloudflare Turnstile。 |
| **GW-02** | **HIGH** | CWE-20 / LLM01 | `api/chat.js:176-218` | 透传客户端任意 `role: "system"`（最高 2,600 字符），允许将垂类网关劫持为通用免费 LLM 代理；未强制 `nonSystemAll.length >= 1` 与最后一条必须为 `user`；3,400 字符硬截断会误截合法 `augmentedUser`（最大 ~3,560 字符）。 | 利用 Web Crypto API 实施 **16 子站 `systemPrompt` SHA-256 加密白名单**（含冻结 `thankucrypto` 与 `17zxhold`，100% 零破坏兼容），服务端前置不可覆盖防越狱指令，强校验末条为 `user`，当前 `user` 上限微调至 `3800`。 |
| **GW-03** | **HIGH** | CWE-798 / CWE-522 | `deploy_gateway.py:9-36,68-94` | 硬编码读取 `C:\Users\KALOS\.gemini\config\mcp_config.json` 与无关交易工程 `cb-desk/.env` 跨边界复用密钥；密钥下发至 `["production","preview","development"]` 且全局关闭 `ssoProtection: None` 导致 Preview 公网裸奔。 | 改为仅读取专属环境变量 `VERCEL_TOKEN`、`TRADER_ARCHIVES_AI_GATEWAY_KEY`、`TRADER_ARCHIVES_GEMINI_KEY`；目标收窄为 `["production"]`；改为 `{"ssoProtection": {"deploymentType": "preview"}}`；立即轮换解耦 `cb-desk` 密钥。 |
| **GW-04** | **MEDIUM** | CWE-400 / API4 | `api/chat.js:50-56,151-218` | `req.json()` 无字节上限（可达 4 MB）；`rawMessages.length` 未封顶（可发送 5 万条 `system` 触发 3 次 $O(N)$ 扫描）；`String(m.content)` 内存放大；`IP_BUCKETS` 超 1000 键后无上限且每笔全表扫描。 | `Content-Length` + 流式读取双层 `32 KB` 硬上限（超限返回 `413`）；强校验 `messages.length <= 6` 与 `typeof m.content === 'string'`；`IP_BUCKETS` 设 `2000` 容量硬顶与 10 秒最小清理间隔。 |
| **GW-05** | **MEDIUM** | CWE-400 / CWE-1088 | `api/chat.js:68-89,226-278` | 上游 `fetch` 缺 `AbortController` 超时且未透传 `req.signal`（客户端断开仍空烧 960 tokens）；同密钥 `401`/`403` 无效重试；对外泄露 `402` 欠费状态码。 | 组合 `req.signal` 与 15s TTFB 超时至 `AbortController`；单请求内按 Provider 短路 `401`/`403`；对外将 `402` 统一映射为 `503`。 |
| **GW-06** | **MEDIUM** | CWE-942 / API8 | `api/chat.js:3,10,18-26` | 生产环境无条件放行全球任意 `http://localhost:*`/`127.0.0.1:*` 跨域调用；CORS 冗余放行未使用的 `Authorization` 请求头。 | 将 `ALLOWED_LOCALHOST_RE` 收敛至 `process.env.ALLOW_LOCALHOST_ORIGINS === 'true'` 开关（生产默认关闭）；`Access-Control-Allow-Headers` 收紧为 `'Content-Type'`。 |
| **GW-07** | **LOW** | CWE-693 / API8 | `vercel.json:1-3`, `api/chat.js:96-306` | `vercel.json` 仅空壳配置；API 响应缺 `X-Content-Type-Options`、`X-Frame-Options`、`Referrer-Policy`、`CSP`、`HSTS`、`Cache-Control: no-store` 及 405 `Allow` 头。 | 在 `api/chat.js` 与 `vercel.json` 补齐全部安全响应头与 `Cache-Control: no-store`。 |
| **GW-08** | **LOW** | CWE-209 / CWE-532 | `deploy_gateway.py:57-149` | 异常直接打印未脱敏原始 Vercel HTTP 响应体与完整 deployment JSON；写 `gateway_endpoint.txt` 前未校验生产域名。 | 封装脱敏报错函数过滤凭据与超长响应体；校验 `best_domain == f"{PROJECT_NAME}.vercel.app"`。 |

> **Layer 2 洁净核验**：网关文件零硬编码密钥、无 `.env`/`.vercel` 残留；上游 URL 与模型硬编码无 SSRF/路径注入；上游鉴权用 `Bearer` 头而非查询参数；不向客户端泄露堆栈或上游错误文本。

---

### Layer 3：Python 数据流水线与自动化脚本层（`04_Pipeline` + `01_` 脚本）

| 编号 | 级别 | CWE / OWASP | 位置与数量 | 核心缺陷与复现说明 | 修复方案 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **PL-01** | **CRITICAL** | CWE-798 / A07 | `Stage1_2/collect_all_gch_arbitrage.py:10`, `harvest_gch_arbitrage.py:10`（2 文件） | 硬编码 208 字符 `ai.6551.io` HS256 JWT（`eyJhbGci****...`），Claims 无 `exp` 过期字段，为永久生产凭据。 | 立即前往 `ai.6551.io` 吊销轮换；删除明文 Token 改为仅从 `os.environ["TWITTER_TOKEN"]` 读取。 |
| **PL-02** | **CRITICAL** | CWE-798 / A02 | 15 个遗留 Stage 4 生成器（349 处，30 枚唯一 `atr_*` Key） | 旧版独立建站脚本保留 14–30 枚明文 `atr_*` 密钥，任意误执行即向公开 HTML 二次泄密。 | 吊销全部 30 枚 `atr_*` Key；清零 15 个脚本中的全部密钥并植入废弃熔断守卫，强制收敛至 `build_kol_site_v5.py`。 |
| **PL-03** | **HIGH** | CWE-78 / A03 | **现役 3 个主力脚本**：`harvest_kol_v5.py`、`classify_kol_llm_v5.py`、`incremental_harvest_ws0n.py`（6 处调用） | Windows 宿主机下 `subprocess.run(["tinyfish", "fetch", url], ..., shell=(os.name == "nt"))` 将未校验的 `tid`/`handle` 交给 `cmd.exe /c`，`&`/`|`/`%VAR%` 直接触发本地 RCE。 | 彻底移除 `shell=(os.name == "nt")`，固定 `shell=False`（自动解析 `.cmd` 为直接执行 `node <cli.js>` 并阻断 Shell 元字符）；严格正则校验 `tid`（纯数字）与 `handle`（`[A-Za-z0-9_]{1,15}`）。 |
| **PL-04** | **HIGH** | CWE-79 / CWE-116 | 16 个遗留 Stage 4 生成器 | 原始 `json.dumps` 嵌入 `<script>` 未转义；推文与 AI 响应零转义写入 `innerHTML`；Markdown 链接允许 `javascript:` 与双引号属性逃逸。 | 全部遗留脚本植入废弃熔断守卫（与 PL-02 同步收口），禁止再生成页面。 |
| **PL-05** | **HIGH** | CWE-79 / CWE-83 | **现役旗舰生成器**：`build_kol_site_v5.py`、`build_ws0n_site_v6.py`、`build_thankucrypto_site_v5.py`、`unify_all_14_legacy_subsites.py` | 服务端与前端内联 `onclick="showModalImage(...)"` / `onclick="askPreset(...)"` 存在引号逃逸；外链 `href` 缺 `https?://` 白名单；JSON 仅 `.replace("</", "<\\/")` 未转义 `<`/`>`/`&`/`U+2028`。 | 接入统一 `security_utils.py`：`safe_json_for_script()`、`safe_http_url()`、全面改用 `data-*` + 事件委托、补全 `escHtml` 单引号转义与 CSP `<meta>`。 |
| **PL-06** | **HIGH** | CWE-918 / A10 | **现役 3 脚本**（`harvest_kol_v5.py`、`classify_kol_llm_v5.py`、`incremental_harvest_ws0n.py`）+ 10 旧下载器 | `urllib.request.urlopen()` 原生支持 `file://`；仅用 `"pbs.twimg.com" in murl` 子串绕过；`av_url`/`bn_url` 零校验；自动跟随重定向且 `r.read()` 无字节上限。 | 封装统一 `safe_download_twimg()`：强制 `urlparse` 校验 `https` + 精确域名白名单（`pbs.twimg.com`/`abs.twimg.com`），改用 `requests` `allow_redirects=False` + `stream=True` + 15 MB 硬上限。 |
| **PL-07** | **MEDIUM** | CWE-22 / A01 | `harvest_kol_v5.py`、`build_kol_site_v5.py`、`build_kol_rag_v5.py`、`classify_kol_llm_v5.py` + 6 旧下载器 | `--slug ./thankucrypto` 可绕过 `slug in FROZEN_SLUGS` 精确字符串检查；`local_images` 的 `images/../../` 绕过前缀检查；`tid` 未校验拼接路径。 | 强制 `validate_slug()`/`validate_tid()`，基于 `Path.resolve().is_relative_to()` 校验所有目录边界与冻结守卫。 |
| **PL-08** | **MEDIUM** | CWE-200 / A02 | `classify_kol_llm_v5.py`、`build_kol_rag_v5.py`、`build_ws0n_rag_v9.py`、`audit_kol_v5.py` | 清洗与 RAG 管线无出站密钥脱敏导致 `wallstreet0name` `sk-*` 进入公开数据湖；审计脚本仅扫 HTML 漏检 `data/*.json`。 | 在清洗与 RAG 管线接入 `redact_secrets()`；扩展 `audit_kol_v5.py` 扫描全部 `data/*.json`/`*.csv` 与 Web 安全门禁。 |
| **PL-09** | **MEDIUM** | CWE-200 / CWE-522 | `Stage5/_probe_atria_new.py` & `_probe_atria.py` | 爬取外部 JS 中任意含 `/v1` 的 URL 并直接附带明文 `Authorization: Bearer <atr_key>` 发起 POST。 | 清空并废弃两份一次性探活脚本。 |
| **PL-10** | **MEDIUM** | CWE-547 / CWE-200 | 73/164 脚本（含 3 现役核心脚本跨项目读 `.env`、`build_skill.py` 写 C 盘） | 现役 `classify_kol_llm_v5.py`、`run_track_a_tweets.py`、`run_track_b_articles.py` 硬编码读取外部实验目录 `.env`；`_check_ai_billing.py` 跨读 `cb-desk/.env` 与 `C:\Users\KALOS\.gemini\config\mcp_config.json`。 | 现役脚本移除跨项目硬编码 `.env` 路径，仅读环境变量或显式 `PIPELINE_ENV_FILE`；废弃 C 盘写入脚本与跨读凭据探活脚本。 |
| **PL-11** | **LOW** | CWE-1022 / A05 | `sync_global_hub_v5.py:472` 及旧版 Hub/生成器脚本 | 总站卡片生成模板中 `target="_blank"` 缺失 `rel="noopener noreferrer"`。 | `sync_global_hub_v5.py:472` 补齐 `rel="noopener noreferrer"`，并纳入 `audit_kol_v5.py` 自动断言。 |
| **PL-12** | **LOW** | CWE-434 / CWE-377 | 8 旧图片下载器；`unify_all_14_legacy_subsites.py:1452` | 旧下载器缺 `PIL.Image.verify()` 与原子写入；`unify_all_14_legacy_subsites.py` 写入固定路径 `_verify_vm_scripts.js` 未清理。 | `unify_all_14_legacy_subsites.py` 改用 `tempfile.TemporaryDirectory()` 校验并自动销毁；清理残留 `_verify_vm_scripts.js`。 |

> **Layer 3 洁净核验**：163 个 `.py` AST 扫描确认 **0 `eval`/`exec`/`pickle`/`yaml.load`/`os.system`**、**0 `verify=False` TLS 绕过**、**0 `git add -A`/`--force`**；全部 15 个 `kol_profiles/*.json` 洁净；现役 v5/v6 生成器本身 0 硬编码密钥。

---

### Layer 4：Skills、模板库与供应链层（`03_KOL--ziliao` + `.agents/skills`）

| 编号 | 级别 | CWE / OWASP | 位置 | 核心缺陷与复现说明 | 修复方案 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **TM-01** | **CRITICAL** | CWE-798 / A02 | `03_/KOL--ziliao/` 4 个文件（`SKILL.md`、`SKILL_v1`、`ai_mentor_module.html`、`handbook_skeleton.html`，共 65 处 / 23 枚唯一 `atr_*`） | 明文硬编码 23 枚 `atr_*` Key，模板前端携带 `Authorization: Bearer` 直连并在 `console.log` 打印前缀。 | 立即吊销 23 枚 Key；彻底清除 4 文件全部明文密钥，模板迁至零密钥 Vercel 网关。 |
| **TM-02** | **HIGH** | CWE-79 / A03 | `templates/ai_mentor_module.html:599,616`、`handbook_skeleton.html:1098,1115`、`SKILL_v1:401,413` | `renderSimpleMarkdown()` 未转义 `"` 与 `'` 且外链正则 `[^\)]+` 放行双引号；**已在 Node.js V8 实测复现**利用 CSS `@keyframes fadeInMsg` 的 `onanimationstart` 零点击 DOM XSS。 | 补全 `"`/`'` 转义、收紧外链正则 `https?:\/\/[^\s"'<>()]+` 并用 `new URL()` 严格校验协议为 `https:`/`http:`。 |
| **TM-03** | **HIGH** | CWE-250 / LLM06 | `03_/KOL--ziliao/SKILL.md:4,366,483-484` & `SKILL_v1:4,435-440` | 已废弃旧版 Skill 仍设为 `user-invocable: true`，且指令 Agent 执行 `git add -A` + 无授权 `git push origin main` + 23-Key 注入，直接违背 `AGENTS.md`。 | 将工作区内两份旧 Skill 设为 `user-invocable: false` 并删除危险指令（另提示用户同步清理 C 盘全局同名技能 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao\SKILL.md`）。 |
| **TM-04** | **HIGH** | LLM01 / CWE-918 | `.agents/skills/kol-archive-builder/SKILL.md`、`methodology_v2.md`、`handbook_skeleton.html:970` | 特权 Agent 通读原始推文/外链缺失 Prompt Injection 不可信数据隔离规范；`t.co` 短链探活无目标域名与公网 IP 白名单；旧模板提示词写明“严禁拒绝回答”。 | 在 `kol-archive-builder` 及 `methodology_v2.md` 写入不可信语料隔离铁律与 `t.co` 重定向白名单；清除旧模板“严禁拒绝回答”条款。 |
| **TM-05** | **MEDIUM** | CWE-1333 | `templates/ai_mentor_module.html:593-594`, `SKILL_v1:259` | 防复述正则 `(?:\s*|\d+[\.、]\s*|\*+\s*)*` 存在嵌套可空量词，**已在 Node.js V8 实测复现 $O(2^n)$ 指数 ReDoS**（24 字符 258 ms，30 字符单次约 16.5 秒），流式每片触发 2 次可令页面永久卡死。 | 重写为线性无回溯正则 `^\s*(?:(?:\d+[\.、]|\*+)\s*)*(?:...)[^\n]*(?:\n+|$)`（移除内部 `\s*` 与冗余 `/g`）。 |
| **TM-06** | **MEDIUM** | CWE-693 / CWE-1022 | `templates/handbook_skeleton.html:10-20,789-863`、`ai_mentor_module.html`、`SKILL.md:229` | 缺 CSP/Referrer-Policy；残留无关第三方 `https://api.b.ai` 预连接；4 处 `_blank` 缺 `rel="noopener noreferrer"`；L20 `@import` 前藏 UTF-8 BOM 破坏首行样式。 | 移除 `api.b.ai` 预连接与隐藏 BOM；补齐 CSP、`Referrer-Policy` 与 `rel="noopener noreferrer"`。 |
| **TM-07** | **MEDIUM** | CWE-1104 / A06 | `opentwitter/package.json`；`04_Pipeline` 全目录 | 全工作区 160 个 Python 脚本 0 依赖锁文件（解析 4,892 张不可信图片与网页的 `Pillow`/`requests`/`playwright` 未锁版本）；`opentwitter/package.json` 用顶级名 `"twitter"` 且缺 `"private": true`。 | 为 `04_Pipeline` 新增锁定版本的 `requirements.txt`；`opentwitter/package.json` 改为 `"private": true` 及作用域包名 `"@trader-archives/opentwitter-skill"`。 |
| **TM-08** | **MEDIUM** | CWE-598 / CWE-214 | `opentwitter/SKILL.md:51-514,269-315` | WebSocket `?token=` URL 查询参数传递；19 处 `curl -H "Authorization: Bearer $TWITTER_TOKEN"` 暴露于进程命令行；远程写/删监控接口缺二次确认标注。 | 更新示例改用 `curl -K -` stdin / Python `os.environ`；标注 WebSocket 日志脱敏及写操作人工确认要求。 |
| **TM-09** | **LOW** | CWE-693 / A04 | `.agents/skills/kol-archive-builder/references/audit_checklist.md:23,41-51` | 凭据扫描正则漏检 `ghp_`、`github_pat_`、`eyJ` JWT、`Bearer`；验收清单缺少 XSS/CSP/外链 `rel` 安全回归项。 | 补全密钥正则集合并新增 Web 安全自动化验收门禁清单。 |

---

### Layer 5：Git 历史、数据湖与凭据考古层（`01_/.git` + `02_` + `06_`）

| 编号 | 级别 | CWE / OWASP | 位置 | 核心缺陷与复现说明 | 修复方案 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **GIT-01** | **CRITICAL** | CWE-798 / CWE-312 | `01_/.git` 66+ 历史提交（`0fddd45` ~ `475da30`） | 公开 Git 历史永久暴露 **15 枚 `api.b.ai` (`sk-*`) + 30~31 枚真实高熵 `api.atria-asi.ai` (`atr_*`) 密钥**（另含 22 枚规律合成 `atr_` 串）；`HEAD` 已清零但任意 `git clone` 仍可一键全量提取。 | **P0 立即吊销全部 45+ 枚历史密钥**；经确认后使用 `git-filter-repo` 清洗历史并联系 GitHub 清理缓存；PR 中新增 GitHub Actions 自动凭据扫描工作流（显式覆盖 `atr_`）。 |
| **GIT-02** | **HIGH** | CWE-200 / CWE-312 | `wallstreet0name/data/` 6 文件 + `02_` 6 镜像文件 | 同 `FE-02`/`PL-08`：公开数据湖与 RAG 索引中现网残留 `sk-XPjnsaf****De37`（自 `ea2bd68` 跨 49 个提交）。 | 脱敏全部 10 份派生数据文件（`01_` 与 `02_` 各 5 份，保留只读 `*_ultra_raw.json`）；建议业主后续评估是否剥离公开仓库中的 `*_ultra_raw.json`。 |
| **GIT-03** | **HIGH** | CWE-79 / A03 | 16 个子站 `*/index.html` 内联 JSON | 同 `FE-04`：16 个子站 `FALLBACK_TWEETS` 未做 `\u003c` 转义，5 站已出现原始 `<`；`xiaomu` 语料已实证外部 `<p>`/`<br>` 标签会进入数据湖。 | 全部 14 个非冻结跟踪子站及现役生成器统一转为 HTML-safe JSON 序列化。 |
| **GIT-04** | **MEDIUM** | CWE-200 / CWE-359 | 15 个已追踪 + 1 个未追踪 `*_tweets_ultra_raw.json`（43.5 MB） | 公开仓库纳入全量原始未过滤备份，包含 26,000+ 条回复、320 条嵌套第三方原推及逾万名非目标推友 ID/显示名（含第三方邮箱）。 | 遵守 `AGENTS.md` 不修改/删除存量 `*_ultra_raw.json`，先在 `.gitignore` 加入 `*_ultra_raw.json` 阻断未来增量入库，并供业主决定是否将存量从公开 Git 仓库剥离至本地私密目录。 |
| **GIT-05** | **MEDIUM** | CWE-200 / CWE-538 | `01_/.gitignore`、`17zxhold/data/17zxhold_harvest_report.json` | `.gitignore` 含 UTF-8 BOM 导致首条 `.DS_Store` 规则失效且缺关键安全忽略项；未跟踪 `17zxhold/data/` 混入内部采集遥测报告（暴露 6551/OpenCLI 状态）。 | 重写 `.gitignore` 为无 BOM UTF-8 (LF) 并加入 `*_harvest_report.json`、`*_ultra_raw.json`、`*.key`/`*.pem`/`*cookie*`/`.env*` 等全面规则。 |
| **GIT-06** | **MEDIUM** | LLM01 / CWE-77 | 16 子站 `*/index.html` + `ai_rag_index.json` | 外部抓取语料直接以纯中文括号拼入 `user` 消息，未做不可信边界定界隔离（`17zxhold` 更将其置于提问之后高权重位置）。 | 前端与生成器统一以 `<untrusted_archive_excerpts>` 包裹并过滤闭合标签，配合网关防越狱指令协同生效。 |
| **GIT-07** | **LOW/INFO** | CWE-200 | `ztzzbtc/data/*`（公开招聘邮箱）、`xiaomu/data/*`（72 处 `<p>`/`<br>`） | 推文转述残留 HTML 标签与 KOL 公开招聘邮箱（已核验无 XSS 触发）。 | 建议后续清洗剥离残留 HTML 标签并在 README 提供数据更正/删除联络方式。 |

> **Layer 5 洁净核验**：全历史 93 个 commits 与 `01_`/`02_`/`06_` 数据湖中 **0 处** `AIza*`、`ghp_`/`gho_`/`github_pat_`、`AKIA*`、PEM 私钥、Twitter/微博 Cookie、钱包私钥/助记词或真实 XSS/CSV 注入/Prompt Injection 载荷；`.git/config` 无嵌入 Token；提交历史中无本机路径 `KALOS` 泄露。

---

## 三、修复范围、边界与人工动作清单（Remediation Scope & Owner Actions）

### 3.1 自动化代码修复清单（本次直接落地并验证）
1. **公开仓库 PR（分支 `security/full-stack-audit-remediation` -> `main`）**：
   - 修复 `.gitignore`（去 BOM + 补全敏感/遥测/原始备份忽略规则）；
   - 加固根 `index.html`（CSP + Referrer-Policy + 16 处 `rel="noopener noreferrer"` + 15 处离线 SVG `onerror`）；
   - 加固全部 **14 个非冻结已追踪 KOL 子站**（CSP + Referrer-Policy + `escHtml` 补单引号 + `data-modal-src` 事件委托去内联 `onclick` + `safeHttpUrl()` + `rCls`/`cached.ragCount` 强整数化 + HTML-safe `<script>` JSON 转义 + `<untrusted_archive_excerpts>` RAG 边界隔离）；
   - 脱敏 `wallstreet0name/data/` 全部 5 份派生数据文件（`tweets.json/.csv`、`domains/07_*.json/.csv`、`ai_rag_index.json`）；
   - 新增自动化安全回归门禁脚本 `scripts/security_verify.py`、GitHub Actions 工作流 `.github/workflows/security-audit.yml` 与本审计报告 `SECURITY_AUDIT_REPORT.md`。
2. **工作区非 Git 层全量加固（直接落地并验证）**：
   - **Layer 2 (`05_AI_Mentor_Gateway_Vercel/`)**：全面加固 `api/chat.js`（16 子站 `systemPrompt` SHA-256 白名单 + 32 KB 请求体上限 + `messages.length<=6` + IPv6 `/64` 与 Upstash Redis 限流接口 + `AbortController`/`req.signal` + 生产关闭 `localhost` CORS + 全套安全响应头）、`vercel.json`、`deploy_gateway.py`（解耦 `cb-desk/.env` 与 C 盘路径、收窄 `production` Env、恢复 Preview `ssoProtection`、报错脱敏与域名校验）。
   - **Layer 3 (`04_Pipeline/`)**：新增公共安全模块 `security_utils.py`；清除 `PL-01` 永久 JWT 与 `PL-02` 349 处 `atr_*` 密钥并熔断废弃旧脚本；修复现役 v5/v6 脚本 `PL-03` OS 命令注入、`PL-05` 二阶 XSS、`PL-06` SSRF/`file://`、`PL-07` 路径遍历与冻结守卫绕过、`PL-08` 密钥脱敏与审计扩展、`PL-10` 跨项目 `.env` 硬编码、`PL-11`/`PL-12` 并新增版本锁定 `requirements.txt`。
   - **Layer 4 (`03_KOL--ziliao` & `.agents/skills/kol-archive-builder/`)**：禁用旧版 `KOL--ziliao`（`user-invocable: false`）、清除 65 处 `atr_*` 密钥及 `git add -A`/`git push` 指令；修复旧模板 `TM-02` DOM XSS 与 `TM-05` ReDoS；移除 `api.b.ai` 与 BOM；加固 `kol-archive-builder` Prompt Injection 隔离规则、`t.co` 重定向白名单与审计清单；加固 `opentwitter/package.json` 与 `SKILL.md`。
   - **Layer 5 (`02_14位KOL纯享数据包/`)**：同步脱敏 `02_华尔街没有名字_WallStreet0Name/data/` 5 份派生镜像文件。

### 3.2 严格遵守工作区红线未自动修改的项 & 需业主手动执行的云端操作
以下操作受限于工作区只读规范、C 盘净空规范或需云端控制台授权，已保留原状并在下方给出精确指令：
1. **【P0 云端必做】密钥吊销与轮换**：
   - `api.b.ai`：吊销历史上泄露的 15 枚 `sk-*` 密钥（`GIT-01`）；
   - `api.atria-asi.ai`：吊销历史上泄露的 30+ 枚 `atr_*` 密钥（`GIT-01` / `PL-02` / `TM-01`）；
   - `ai.6551.io`：吊销硬编码的永久 JWT Token 并签发新 Token 写入环境变量 `TWITTER_TOKEN`（`PL-01`）；
   - Vercel / `cb-desk`：为 `trader-archives-ai-gateway` 签发独立带预算封顶的 `TRADER_ARCHIVES_AI_GATEWAY_KEY` / `TRADER_ARCHIVES_GEMINI_KEY`，轮换原共享的 `cb-desk` 密钥，并重新执行 `deploy_gateway.py` 部署加固后的网关（`GW-03`）；同步在 Vercel Dashboard 开启 Edge Firewall Rate Limiting（`GW-01`）。
2. **【P1 历史清理】公开 Git 历史重写与 `*_ultra_raw.json` 处理**：
   - 按 `AGENTS.md` 第 3 条，本次严禁修改或删除任何 `*_ultra_raw.json` 原始备份。若需从公开仓库彻底消除 `wallstreet0name_tweets_ultra_raw.json` 及历史 66+ 个提交中的明文密钥，请在完整备份后执行 `git filter-repo` 替换密钥并从公开历史剥离 `*_ultra_raw.json`，强制推送后联系 GitHub 清理缓存。
3. **【P1 冻结标杆站】`thankucrypto/` 与 `laoemo/`**：
   - 按 `AGENTS.md` 第 3 条，本次保持两座冻结模范站零改动；`thankucrypto` 的 AI 网关已通过服务端 SHA-256 白名单完成保护。若后续决定解冻同步前端 CSP 与 `escHtml` 补丁，可直接运行本 PR 附带的加固脚本对其执行一键同步。
4. **【P1 本机 C 盘旧 Skill】**：
   - 按 C 盘净空规则，本次未触碰 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao\SKILL.md`，请手动将其设为 `user-invocable: false` 或删除，防止宿主环境误触发旧版 23-Key 技能。
