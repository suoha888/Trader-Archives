# Trader-Archives 全栈六层安全审计报告（CSO Security Audit Report）

> **审计日期**：2026-11-25  
> **审计范围**：`d:\Codex\顶级 KOL数据` 全工作区（6 大架构层：公开前端与 17 个 KOL 子站、Vercel Edge AI 网关与云部署、6 阶段 Python 采集建站流水线、Agent Skills 与模板供应链、数据湖/导出包/RAG 索引、Git 历史考古与仓库安全）  
> **审计架构**：12-Agent 并发集群（6 路专职领域安全审计 Agent + 6 路独立盲审交叉验证 Agent，严格执行 Pre-emit 代码引证门禁与误报过滤）  
> **目标公开仓库**：[`suoha888/Trader-Archives`](https://github.com/suoha888/Trader-Archives)（Visibility: **PUBLIC**，默认分支 `main`，基准提交 `5e18e9a`）

---

## 一、执行摘要（Executive Summary）

本次集群审计共扫描工作区 **1,472+ 文本源码与配置文件**、**18 个静态 HTML 页面**、**180 个流水线/建站/审计脚本**、**13 个 Agent Skill 与模板文件**、**306 份 CSV / 16 份 RAG 索引（34,869 条文档）** 以及公开 GitHub 仓库全部 **93 个历史提交（1,390 个非媒体历史 blob）**。

- **候选发现总数**：54 项（F01–F54）
- **独立盲审结论**：`VERIFIED` 27 项、`DOWNGRADED` 25 项、`FALSE_POSITIVE` 2 项（F09、F38 已剔除）、`UNVERIFIED` 0 项
- **合并去重后有效安全议题**：**20 项**（对应 52 条跨层独立验证记录）

| 严重级别 | 跨层独立验证记录数 | 合并去重后核心议题数 | 核心风险焦点 |
|---|---:|---:|---|
| **CRITICAL** | 5 | **3** | 公开 Git 历史永久泄露 45 枚真实 LLM API Key；19 份本地模板/技能残留 30 枚明文 Key 且存在回流风险；Vercel 付费 AI 网关无鉴权且仅凭可伪造 `Origin`/`Referer` 放行 |
| **HIGH** | 9 | **6** | 网关允许客户端任意替换 `system` 提示词（通用免费 AI 代理）；Edge 单实例内存限流可绕过；采集脚本硬编码无 `exp` 的生产 JWT；25 脚本跨项目收割 `mcp_config.json` 与 `cb-desk/.env`；Windows `shell=True` OS 命令注入；遗留技能指令 `git add -A && git push origin main` |
| **MEDIUM** | 17 | **9** | 公开数据湖/RAG 再分发第三方明文 `sk-` 密钥；全站 16 子站 RAG 无隔离拼接存在实态提示词注入；建站器与前端多处 DOM XSS / 上下文逃逸汇点；图片下载 SSRF / `file://` 读取；`--slug` 路径穿越绕过冻结目录保护；上游 `fetch` 无超时与密钥同步漂移；`_probe_atria_new.py` 向动态爬取 URL 外发 Bearer Key；仓库缺失 `.gitignore` 规则/Gitleaks CI/`SECURITY.md`；Skill 供应链边界缺失 |
| **LOW / INFO** | 21 | **2** | 缺失 CSP / 安全响应头 / `Referrer-Policy` / `noreferrer`；`sessionStorage` `cached.ragCount` 未转义；生产 CORS 放行 `localhost`；306 份 CSV 缺 CWE-1236 公式中和；`*_ultra_raw.json` 含第三方邮箱；`17zxhold_harvest_report.json` 泄露采集遥测；`xiaomu` 残留 `<p>` 碎片 |

### 正向安全基线确认（Verified Positive Controls）
1. 公开仓库 `HEAD`（`5e18e9a`）中全部 18 个 HTML 页面均已清除维护者自有前端硬编码 API Key，统一迁移至服务端 Vercel Edge 网关，且**零第三方 CDN JavaScript 依赖**。
2. 全站 16 个活跃 AI 研报子站的 `formatAiExquisiteOutput()` 经实测已对 LLM 直接输出进行 HTML 转义，且锚点正则严格受限，无直接由 LLM Markdown 触发的 XSS。
3. 现役 v5/v6 生成器已对内联 JSON 做 `.replace("</", "<\\/")` 处理，**在线上 18 个页面中无活跃 `</script>` 逃逸漏洞**（候选 F09 经独立盲审确认为误报）。
4. 全工作区未检出 `os.system`、`os.popen`、`pickle.load`、`yaml.load` 或 `requests(..., verify=False)`。

---

## 二、攻击面测绘（Attack Surface Map）

```text
ATTACK SURFACE MAP — Trader-Archives Full Stack
══════════════════════════════════════════════════════════════════
CODE & WEB SURFACE
  Public static pages:      18 HTML (1 root hub + 17 KOL subsites, GitHub Pages)
  Frozen benchmark sites:    2 (thankucrypto/, laoemo/ — strictly read-only per AGENTS.md)
  Client-side DOM sinks:   172 innerHTML sites across 16 AI subsites; 32 sessionStorage ops
  Unauthenticated APIs:      1 Vercel Edge endpoint (/api/chat) proxying paid LLM keys
  Authenticated endpoints:   0
  Local pipeline scripts:  180 Python/JS scripts (Stage 1–5 + ws0n_v6_rebuild + root utils)
  Executable Agent Skills:  13 files (03_KOL--ziliao + .agents/skills/kol-archive-builder)
  Published datasets:      306 CSVs + 16 ai_rag_index.json (34,869 docs) + 16 ultra_raw JSONs

INFRASTRUCTURE & REPO SURFACE
  Git repository:            1 PUBLIC repo (suoha888/Trader-Archives, 93 commits)
  CI/CD workflows:           0 (missing secret scanning & security gates)
  Security policy / hooks:   0 (no SECURITY.md, .gitleaks.toml, CODEOWNERS, git hooks)
  Cloud deploy targets:      2 (GitHub Pages + Vercel Edge Functions)
  Secret management:         Mixed (Vercel env vars + cross-project .env + mcp_config.json + legacy hardcoded pools)
```

---

## 三、全层合并安全发现详单（20 项核心议题，映射 F01–F54）

> [!CAUTION]
> 为遵循最小泄露原则，下文中所有真实密钥、JWT 令牌及敏感凭据均已脱敏（仅保留前缀与末 4 位）。

### 3.1 CRITICAL（P0 — 立即处置）

#### SEC-01：`suoha888/Trader-Archives` 公开 Git 历史永久暴露 45 枚真实 LLM API 密钥
- **严重程度**：CRITICAL ｜ **独立验证置信度**：10/10（VERIFIED）｜ **集群映射**：`F01`, `F02`, `F47`
- **位置**：公开仓库 `01_Trader-Archives_14位KOL全量网站与数据湖` 历史提交 `0fddd45382`..`9355f712a8`（如 `452aed79e6:metabape/index.html:18168`、`09623fcbd2:index.html:6535`、`9355f71^:kuigas/index.html:21087`）
- **实证代码摘录（已脱敏）**：
  ```js
  // commit 452aed79e6: metabape/index.html L18167-18176 (30 枚真实 atr_* 密钥)
  const ATRIA_CONFIG = {
      apiUrl: 'https://api.atria-asi.ai/v1/chat/completions',
      keys: ['atr_4KCk...HMnV', 'atr_M7r-...Ux4d', 'atr_XEsZ...FsCS', ...]
  };
  // commit 09623fcbd2: index.html L6591-6609 (15 枚真实 sk-* 密钥)
  const CJ_AI_CONFIG = {
      apiUrl: 'https://api.b.ai/v1/chat/completions',
      keys: ['sk-1q7t0...ml09', 'sk-1q6lh...2scv', ...]
  };
  ```
- **利用场景**：攻击者克隆公开仓库 `https://github.com/suoha888/Trader-Archives.git` 或通过 GitHub API 遍历历史 commit，一键提取全部 30 枚真实 Atria `atr_*` 密钥（波及 15 个 HTML 文件、51 个快照提交）与 15 枚 `api.b.ai` `sk-*` 密钥（波及 15 个快照提交），批量用于未授权 LLM 推理代理并耗尽配额/产生账单。
- **事件响应剧本（Incident Response Playbook — 需仓库所有者手动执行）**：
  1. **立即吊销（Revoke）**：在 `api.atria-asi.ai` 与 `api.b.ai` 控制台撤销全部 45 枚已暴露密钥（不可依赖“余额已用完”）；
  2. **轮换（Rotate）**：若仍需使用对应供应商，重新生成独立密钥并仅存服务端环境变量；
  3. **清洗历史（Scrub History）**：使用 `git filter-repo --replace-text` 清除历史提交中的密钥（因涉及强推重写公开 `main` 历史，需所有者审批执行）；
  4. **清除远端缓存**：联系 GitHub Support 清除远端悬空对象缓存；
  5. **防回流**：在仓库启用 GitHub Secret Scanning + Push Protection，并落地 `.gitleaks.toml` 与 CI 门禁（本 PR 实现）。

#### SEC-02：遗留 `KOL--ziliao` 可调用技能与 19 个本地模板/脚本残留 30 枚明文 Atria 密钥
- **严重程度**：CRITICAL ｜ **独立验证置信度**：10/10（VERIFIED）｜ **集群映射**：`F04`, `F27`, `F39`
- **位置**：`03_KOL--ziliao_核心Skill与模板库/KOL--ziliao/SKILL.md:370`、`SKILL_v1_单站初版备份.md:211`、`templates/ai_mentor_module.html:436`、`templates/handbook_skeleton.html:946`；`04_Pipeline/Stage4_象牙白研报子站生成/` 下 15 个遗留脚本（合计 351 处）；及全局激活副本 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao\SKILL.md`
- **利用场景**：AI Agent 或维护者一旦误调用旧版 `KOL--ziliao` Skill 或运行任意遗留 `build_*_site.py`，就会将 14–30 枚明文 `atr_*` 密钥重新注入前端 `index.html` 并推回公开仓库。
- **修复策略**：彻底清除工作区 `03_` 与 `04_` 全部 19 个文件中的明文密钥数组并切换为无密钥网关模板；同步提醒用户卸载 C 盘全局 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao`（遵守 C 盘净空规范，不擅自修改 C 盘）。

#### SEC-03：Vercel Edge 付费 AI 网关无有效鉴权，仅依赖可伪造 `Origin`/`Referer` 且关闭 `ssoProtection`
- **严重程度**：CRITICAL ｜ **独立验证置信度**：10/10（VERIFIED）｜ **集群映射**：`F16`
- **位置**：`05_AI_Mentor_Gateway_Vercel/api/chat.js:16-31, 95-106`、`deploy_gateway.py:86-94`
- **利用场景**：攻击者用 `curl`/`Python` 伪造 `Origin: https://suoha888.github.io` 即可绕过 `isAllowedOrigin()`，直接消耗站主付费的 `GEMINI_API_KEY` 与 `AI_GATEWAY_API_KEY`；且 `deploy_gateway.py` 将 `ssoProtection` 设为 `None`（连 Preview 部署也公网裸奔）。
- **修复策略**：将 `ssoProtection` 收紧为仅开放 production（保护 preview）；网关层引入可选 Cloudflare Turnstile / 共享客户端签名校验开关 + 服务端固定提示词校验 + 分布式限流与全站日配额硬熔断，并建议在 Vercel / Gemini 控制台配置硬性月消费上限。

---

### 3.2 HIGH（P1 — 高优先修复）

#### SEC-04：Edge AI 网关信任并透传客户端任意 `system` 提示词（通用免费 AI 代理滥用）
- **严重程度**：HIGH ｜ **独立验证置信度**：9/10（DOWNGRADED from CRIT）｜ **集群映射**：`F17`（关联 `F13`）
- **位置**：`05_AI_Mentor_Gateway_Vercel/api/chat.js:189, 205-209` + 16 个前端子站
- **利用场景**：结合 SEC-03，攻击者可将 `messages[0]` 替换为任意 `system` 指令，将专用 KOL 研报问答代理变成免费通用 LLM API，放大盗刷与上游合规封号风险。
- **修复策略**：在 `api/chat.js` 建立 16 个合法子站 `systemPrompt` 的 SHA-256 哈希白名单（兼顾向后兼容冻结站 `thankucrypto`）并前置不可覆盖的服务端安全护栏 `SERVER_SECURITY_GUARD`，拒绝任何未经认证的自由 `system` 提示词。

#### SEC-05：Edge 单 Isolate 内存限流易被绕过，存在 `x-forwarded-for` 回退伪造与全局 `'unknown'` 桶碰撞
- **严重程度**：HIGH ｜ **独立验证置信度**：9/10（VERIFIED）｜ **集群映射**：`F18`
- **位置**：`05_AI_Mentor_Gateway_Vercel/api/chat.js:33-66`
- **修复策略**：集成分布式限流（Upstash Redis REST API 可选配置）+ 全站硬性日请求上限；生产环境优先且严格信任 `x-vercel-forwarded-for`（移除无界 `x-forwarded-for` 伪造回退）；对 IPv6 归并至 `/64` 子网；为内存兜底 Map 设置容量硬上限。

#### SEC-06：Stage1_2 遗留采集脚本明文硬编码无过期时间（No `exp`）的 `ai.6551.io` 生产 JWT
- **严重程度**：HIGH ｜ **独立验证置信度**：10/10（VERIFIED）｜ **集群映射**：`F03`, `F26`
- **位置**：`04_Pipeline/Stage1_2_推文与长文全量抓取/collect_all_gch_arbitrage.py:10`、`harvest_gch_arbitrage.py:10`
- **说明**：解码 Payload 显示含 `user` 与 `jti=19727dd2-ca88-4a16-bab1-afb4b6e2fd91`，**无 `exp` 声明**（永久有效）。
- **修复策略**：立即在 `ai.6551.io` 后台吊销/轮换该 JWT；源码彻底移除硬编码改为读取环境变量 `API_6551_TOKEN` / `TWITTER_TOKEN`。

#### SEC-07：部署与 25 个流水线脚本跨项目硬编码读取 C 盘 `mcp_config.json` 与无关交易项目 `cb-desk/.env`
- **严重程度**：HIGH ｜ **独立验证置信度**：9/10（VERIFIED）｜ **集群映射**：`F19`, `F05`, `F34`
- **位置**：`05_AI_Mentor_Gateway_Vercel/deploy_gateway.py:9-36`、`Stage5/_check_ai_billing.py:8,24`、`Stage4/build_skill.py:183` 及 20+ 流水线脚本
- **利用场景**：公网免费网关一旦被盗刷，爆炸半径直接冲击无关链上量化项目 `cb-desk` 的同一 `AI_GATEWAY_API_KEY`；且自动化脚本直接读取个人全局 `mcp_config.json` 账号级 `VERCEL_TOKEN`，违背最小权限与凭据隔离。
- **修复策略**：彻底清除跨项目 `.env` 与 `C:\Users\KALOS\.gemini\config\mcp_config.json` 硬编码读取逻辑，统一改由当前进程环境变量注入专属隔离凭据；禁用 `build_skill.py` 向 C 盘全局目录的硬编码写入。

#### SEC-08：现役 v5/v6 脚本在 Windows 下启用 `shell=True` 拼接未校验推文 ID / Handle 导致 OS 命令注入（CWE-78）
- **严重程度**：HIGH ｜ **独立验证置信度**：9/10（VERIFIED）｜ **集群映射**：`F28`
- **位置**：`Stage3/classify_kol_llm_v5.py:1165`、`Stage1_2/harvest_kol_v5.py:224,248,643`、`ws0n_v6_rebuild/incremental_harvest_ws0n.py:179,396`
- **利用场景**：Windows `subprocess.run(list, shell=True)` 将参数交由 `cmd.exe /c` 解析且不转义 `& | ^ %VAR% >`。当外部抓取 JSON 中的 `tid` 或 `--handle` 包含 Shell 元字符时可触发任意命令执行。
- **修复策略**：全面移除 `shell=(os.name == "nt")`，改为 `shutil.which(...)` 解析可执行文件并以 `shell=False` 列表调用；强制正则校验 `handle` (`^[A-Za-z0-9_]{1,15}$`) 与 `tid` (`^\d{15,22}$`)。

#### SEC-09：遗留 `KOL--ziliao` 技能保留 `user-invocable: true` 并指令 Agent 免确认 `git add -A && git push origin main`
- **严重程度**：HIGH ｜ **独立验证置信度**：10/10（VERIFIED）｜ **集群映射**：`F41`
- **位置**：`03_KOL--ziliao_核心Skill与模板库/KOL--ziliao/SKILL.md:4,483`、`SKILL_v1_单站初版备份.md:4,436`（含全局副本 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao\SKILL.md`）
- **修复策略**：将工作区遗留副本设为 `user-invocable: false` 并标注 DEPRECATED，彻底删除 `git add -A` 与自动 `git push origin main` 指令；同时提醒用户移除 C 盘全局旧技能副本。

---

### 3.3 MEDIUM（P2 — 架构与防御纵深加固）

| 编号 | 映射 ID | 置信度 | 漏洞描述与受影响范围 | 修复方案 |
|---|---|---:|---|---|
| **SEC-10** | `F06`, `F48` | 9/10 | **公开数据湖与 RAG 索引再分发第三方明文密钥**：`wallstreet0name` 推文 `2000843101716508867` 所含第三方密钥 `sk-XPj...De37` 被原样镜像至公开库 5 个衍生文件（含 `ai_rag_index.json`）及纯享包，且现有审计门禁仅扫描 HTML 未扫 `data/` | 对 `wallstreet0name` 衍生 JSON/CSV/RAG 文件执行 `[REDACTED_SECRET]` 脱敏（保持 `*_ultra_raw.json` 只读不变）；在清洗/RAG 脚本中加入自动密钥脱敏器，并扩展审计门禁扫描全部文本资产 |
| **SEC-11** | `F49` | 9/10 | **全站 16 子站 RAG 上下文无隔离拼接（间接提示词注入 OWASP LLM01）**：`wallstreet0name/data/ai_rag_index.json` 中已存在实态角色劫持/指令覆盖文本，前端直接以中文方括号拼入 `user` 消息且 `systemPrompt` 缺失边界防御 | 用 `<retrieved_context>...</retrieved_context>` 包裹检索语料并转义闭合标签；在所有非冻结子站与 v5/v6 模板 `systemPrompt` 及网关服务端护栏加入明确的反间接提示词注入指令 |
| **SEC-12** | `F10`, `F29`, `F30`, `F31`, `F40`, `F51` | 9/10 | **前端渲染与静态站生成器多处 XSS / 上下文逃逸汇点**：1) `escHtml()` 漏转义单引号 `'` 导致 `onclick="showModalImage('${escHtml(p)}')"` 逃逸；2) `href="${escHtml(t.tweetUrl)}"` 与 `art['url']` 未做 `https?://` 协议白名单校验；3) `t.roleOrder` 未强转整数直接拼入 `class` 属性；4) `preset_prompts` 漏转义双引号；5) 现役 v5/v6 内联 JSON 漏转义 `<!--`/`<`/`\u2028`/`\u2029`，5 个遗留脚本完全零转义；6) 遗留 `ai_mentor_module.html` `renderSimpleMarkdown()` 双引号逃逸 & 11 个遗留 Stage4 生成器零转义 `innerHTML` | 统一补全 `escHtml` 单引号转义、`safeHttpUrl()` 协议白名单、事件委托 `data-modal-src` 替代内联 `onclick`、`Number(t.roleOrder)` 强转、`safe_json_for_script()` 完整转义，修复全部非冻结子站、v5/v6 生成器、`sync_global_hub_v5.py` 及 03/04 模板脚本 |
| **SEC-13** | `F32` | 9/10 | **图片下载器缺乏 `https://` 精确域名白名单与体积上限（SSRF / `file://` 读取）**：`harvest_kol_v5.py`、`classify_kol_llm_v5.py`、`incremental_harvest_ws0n.py` 使用 `urllib.request.urlopen()` 且仅做 `"pbs.twimg.com" in murl` 子串校验，头像/横幅 URL 零校验 | 封装统一安全下载器：`urlparse` 严格校验 `scheme == "https"` + 精确主机白名单（`pbs.twimg.com`, `abs.twimg.com`）+ DNS 解析阻断私有/环回/链路本地 IP + 逐跳校验重定向 + 15 MB 流式上限 |
| **SEC-14** | `F33` | 10/10 | **v5 流水线 `--slug` 与内部路径未校验边界（CWE-22）**：在 Windows NTFS 下传入 `./thankucrypto` 或 `ThankUCrypto` 可绕过 `FROZEN_SLUGS` 冻结保护，传入 `../` 可引发任意目录读写 | 所有 v5 入口统一加入 `validate_slug()`（正则 `^[a-z0-9][a-z0-9-]{0,40}$` + `.lower()` 校验 `FROZEN_SLUGS`）并对拼接路径强制 `.resolve().is_relative_to(base.resolve())` |
| **SEC-15** | `F20`, `F23` | 9/10 | **Edge 网关上游 `fetch` 无超时/断连取消与 4 路回退放大；`deploy_gateway.py` 生产密钥越权下发至 `preview`/`development` 且漏同步 `GEMINI_API_KEY`** | 增加 `UPSTREAM_TTFB_TIMEOUT_MS = 15000`、`req.signal` 联动中止、同 Provider `401/402/403/429` 熔断；`deploy_gateway.py` 仅向 `production` 注入 `sensitive` 类型密钥并同步 `GEMINI_API_KEY` |
| **SEC-16** | `F35` | 10/10 | **`_probe_atria_new.py` 向动态爬取的未校验外部 URL 自动发送 Bearer Key（CWE-200）** | 停用/中和 `_probe_atria_new.py` 与 `_probe_atria.py` 的外部动态爬取发 Key 逻辑，严格要求仅向硬编码官方 HTTPS 域名发请求 |
| **SEC-17** | `F07` | 9/10 | **公开仓库安全基础设施缺失**：`.gitignore` 首行含 UTF-8 BOM 导致 `.DS_Store` 规则失效且缺失 `.env.*`/`*.pem`/`*.key`/`*_harvest_report.json`；完全缺失 `.github/workflows` Secret Scanning CI、`.gitleaks.toml`、`SECURITY.md` 与 `CODEOWNERS` | 修复 `.gitignore`（去 BOM + 补全规则），新增 `.gitleaks.toml`、`SECURITY.md`、`.github/CODEOWNERS`、`.github/workflows/security-audit.yml` 及 `scripts/security_verify.py` 自动化安全门禁 |
| **SEC-18** | `F42`, `F43`, `F45`, `F46` | 8/10 | **Agent Skill 供应链与审核清单盲区**：`opentwitter/SKILL.md` 将通用 `TWITTER_TOKEN` 发往第三方域 `ai.6551.io`、存在 bash `curl` 单引号注入与 WebSocket URL 明文传 Token；`kol-archive-builder` 缺短链域名白名单、防提示词注入边界及过窄的发布前密钥审计规则 | 重构 `opentwitter/SKILL.md` 与 `package.json`（更名专属 `API_6551_TOKEN`、参数化安全调用、防注入边界、标注 WebSocket 凭据风险）；补齐 `kol-archive-builder/SKILL.md`、`methodology_v2.md` 与 `audit_checklist.md` 及 `audit_kol_v5.py` 全量安全门禁 |

---

### 3.4 LOW & INFO（P3 — 浏览器加固与数据卫生）

- **SEC-19 [LOW, 8–9/10 VERIFIED]**（映射 `F11`, `F12`, `F14`, `F15`, `F21`, `F22`, `F24`, `F25`, `F36`, `F44`）：
  1. 全站 18 页缺失 `<meta http-equiv="Content-Security-Policy">` 与 `<meta name="referrer" content="strict-origin-when-cross-origin">`（修复全部非冻结页面 + v5/v6 生成器；冻结站 `thankucrypto/`、`laoemo/` 记录在案待显式解冻授权）。
  2. `sendAiQuestion()` 将 `sessionStorage` 反序列化的 `cached.ragCount` 未强转整数即拼入 `innerHTML`（改为 `Math.max(0, parseInt(cached.ragCount, 10) || 0)`）。
  3. 总站 `index.html` 16 处 `target="_blank"` 完全缺失 `rel`，16 子站 5,878 处缺少 `noreferrer`；首页 15 处头像回退 `onerror` 缺 `this.onerror=null` 并外链 `abs.twimg.com`。
  4. `api/chat.js` 生产环境无条件放行 `localhost` CORS、未校验 `Content-Type: application/json`、无请求体字节数上限（32 KB）及消息总数上限（6 条）、Referer 回退头不一致；`vercel.json` 与 `api/chat.js` 缺安全响应头（`nosniff`, `DENY`, `no-store`, `HSTS`）；`deploy_gateway.py` 与 `_check_ai_billing.py` 原始打印错误响应体。
  5. `handbook_skeleton.html` 残留废弃第三方域 `api.b.ai` 预连接。
- **SEC-20 [LOW/INFO, 8–9/10 VERIFIED]**（映射 `F37`, `F50`, `F52`, `F53`, `F54`, `F08`）：
  1. 全部 24 个 CSV 导出脚本与 306 份公开 CSV 缺失 CWE-1236 公式中和（含 12 处 `- ` 与 42,054 处 `@` 前缀单元格）→ 在现役 CSV 导出函数增加 `sanitize_csv_cell()`，并对非冻结公开 CSV 做好中和策略评估（注：大规模重写 42,054 处 `@handle` 会影响纯享包可读性，对真正会触发 Excel 公式的 `=`, `+`, `-`, `\t`, `\r` 强制中和，并可按需对 `@` 做严格公式模式检测如 `@SUM(`/`@CMD` 或前置单引号，确保安全与数据可用性兼顾）。
  2. 16 份 `*_ultra_raw.json`（43.45 MB）含第三方邮箱，遵循 `AGENTS.md` 只读红线不修改本地原始备份，在报告中建议后续归档至私有目录。
  3. 未追踪待提交目录 `17zxhold/data/17zxhold_harvest_report.json` 泄露内部采集遥测通道名 → 已在 `.gitignore` 加入 `*_harvest_report.json` 阻断误提交。
  4. `xiaomu` 12 份数据残留无害 `<p>`/`<br>` 碎片 → 在 `classify_kol_llm_v5.py` 文本规范化阶段补齐 HTML 碎片剥离。
  5. 根工作目录 4 个已 gitignore 的旧调试脚本滞留 → 建议移出仓库工作目录。

---

## 四、STRIDE 威胁建模与数据分级（CSO Phases 10–11）

### 4.1 核心组件 STRIDE 威胁矩阵
| 组件 | Spoofing (仿冒) | Tampering (篡改) | Repudiation (抵赖) | Info Disclosure (信息泄露) | DoS / Cost Abuse (拒绝服务/成本放大) | Elevation of Privilege (越权) |
|---|---|---|---|---|---|---|
| **GitHub Pages 前端 (18 HTML)** | 低（无登录态） | 中（静态站 XSS 汇点 + 同源 `sessionStorage` 横向污染） | 低（只读静态页） | 中（第三方密钥镜像于 RAG/数据湖） | 低（GitHub CDN 抗压） | 中（同源 `suoha888.github.io` 跨仓库共享 Origin） |
| **Vercel Edge AI 网关 (`api/chat.js`)** | **极高**（`Origin`/`Referer` 可伪造） | **高**（任意 `system` 提示词劫持） | 高（缺少审计日志与请求 ID） | 中（上游错误元数据、缓存头缺失） | **极高**（付费 API 盗刷 + 单 Isolate 内存限流绕过） | **高**（任意匿名调用付费代理与跨项目密钥） |
| **本地采集与建站流水线 (`04_Pipeline`)** | 中（外部推文/短链源不可信） | **高**（Windows `shell=True` OS 命令注入 + SSRF） | 中（本地日志） | **高**（硬编码 JWT / 30 枚 Atria Key / 跨项目读取 `.env`） | 中（无体积上限图片下载） | **高**（`--slug` 路径穿越绕过冻结目录保护） |
| **Agent Skills 供应链 (`03_` & `.agents/`)** | 高（旧 Skill 遮蔽新 Skill） | **高**（间接提示词注入通过抓取网页/推文进入 Agent） | 中（免确认 `git push`） | **极高**（硬编码 23-Key 与通用 `TWITTER_TOKEN` 碰撞） | 低 | **高**（免确认 `git add -A && git push origin main`） |

### 4.2 数据资产分级（Data Classification）
- **RESTRICTED（绝密 — 泄露即直接资金/账号损失）**：`VERCEL_TOKEN`、`AI_GATEWAY_API_KEY`、`GEMINI_API_KEY`、无 `exp` 的 `ai.6551.io` JWT、30 枚历史 `atr_*` 与 15 枚 `sk-*` 密钥。
- **CONFIDENTIAL（机密 — 泄露影响内部架构与关联项目）**：宿主机 `mcp_config.json`、`cb-desk/.env`、内部采集通道遥测（`*_harvest_report.json`）。
- **INTERNAL（内部）**：本地流水线检查点（`checkpoints/`）、本地只读原始备份（`*_ultra_raw.json`）、本地调试审计脚本。
- **PUBLIC（公开）**：18 个静态研报网页、清洗后的公开数据湖与 `ai_rag_index.json`、公开 README 与文档。

---

## 五、边界与免责声明

1. **只读与冻结红线遵循**：严格遵循 `AGENTS.md` 第 3 条，全部修复过程绝不修改或删除任何 `*_ultra_raw.json` 原始备份，绝不改动冻结模范站 `thankucrypto/` 与 `laoemo/`，且不触碰当前工作树未提交的 `17zxhold/` 与根目录本地未提交草稿。
2. **人工必填闭环项（无法通过代码 PR 自动完成）**：
   - 在供应商后台吊销已泄露的 **45 枚历史密钥（30 枚 Atria + 15 枚 `api.b.ai`）** 及 **1 枚无过期时间的 `ai.6551.io` JWT**；
   - 轮换并隔离原与 `cb-desk` 共享的 `AI_GATEWAY_API_KEY`，重新部署加固后的 `05_AI_Mentor_Gateway_Vercel`；
   - 审批并执行公开仓库 `git filter-repo` 历史清洗与强制推送；
   - 手动删除 C 盘全局旧技能副本 `C:\Users\KALOS\.gemini\config\skills\KOL--ziliao`。
3. **免责声明**：本报告基于自动化多 Agent 集群代码审计与静态/动态验证生成，不能替代具备资质的专业第三方渗透测试机构的全面人工红队评估。


---

## 六、修复实施与自动化验证记录（Remediation & Verification Log）

| 架构层 | 实施修复项 | 自动化验证结果 |
|---|---|---|
| **Layer 1 · 公开前端与数据湖 (`01_Trader-Archives`)** | 全量 14 非冻结子站 + 根总站补齐 `<meta Content-Security-Policy>` 与 `Referrer-Policy`；修复 `escHtml` 单引号转义、`safeHttpUrl()` 协议白名单、`data-modal-src` 事件委托、`parseInt(t.roleOrder, 10)` 与 `Number(cached.ragCount)` 强转、`<script>` 内联 JSON 全量 `<`/`>`/`&`/` `/` ` 转义、`<untrusted_archive_excerpts>` RAG 边界隔离、全量 `rel="noopener noreferrer"`、首页移除 `abs.twimg.com` 外链循环；脱敏 `wallstreet0name` 衍生数据湖与 RAG 中的第三方明文 `sk-` 密钥；中和 `0xsun` 与 `yourquantguy` 6 份公开 CSV 及对应纯享包中的 CWE-1236 非数值 `-` 公式单元 | `scripts/security_verify.py` 全过（561 份公开文件 0 密钥、134 份 CSV 0 公式注入、15 份 HTML JS 语法 0 报错）；Playwright 实测 6 页 HTTP 200、0 console/page error、0 CSP violation、0 横向溢出、Lightbox 事件委托正常 |
| **Layer 2 · Vercel Edge AI 网关 (`05_AI_Mentor_Gateway_Vercel`)** | `api/chat.js` 落地 16 子站 `systemPrompt` SHA-256 白名单 + 不可覆盖 `SERVER_SECURITY_GUARD`、Upstash 分布式限流（2.5s 超时）+ 全站日上限 + IPv6 `/64` 归并、Vercel 生产环境仅信 `x-vercel-forwarded-for`、`POST Content-Type: application/json` 强校验（415）、无 Origin 仅 Referer 场景 CORS 一致性与 `Vary: Origin, Referer`、32 KB 流式载荷上限（413）、15s TTFB 超时与 `req.signal` 断连中止、`401/402/403/429` 同供应商熔断、可选 Cloudflare Turnstile 人机校验钩子及全套安全响应头；`deploy_gateway.py` 彻底移除跨项目 `mcp_config.json`/`cb-desk/.env` 耦合、收紧 `ssoProtection` 保护 Preview、采用只写 `type: "sensitive"` 生产密钥并同步 `GEMINI_API_KEY` 与 `TURNSTILE_SECRET_KEY` | Node.js ESM 10 项对抗性安全单测全部 PASS（含 403 非法 Origin/提示词、415 MIME、413 超大包、200 合法哈希与护栏前置、429 熔断跳 provider、Turnstile 阻断、生产 XFF 伪造防护） |
| **Layer 3 · 6 阶段 Python 流水线 (`04_Pipeline`)** | 新增共享模块 `security_utils.py`（密钥脱敏、安全 JSON、URL/Slug/ID 校验、DNS 公网 IP 解析防 SSRF 私有/环回地址、无 `shell=True` 的 `run_cli_safe`、CWE-1236 `sanitize_csv_row`、`strip_residual_html`）；全量移除 `shell=(os.name=="nt")` 与硬编码无 `exp` JWT；清除 22 个脚本的跨项目 `cb-desk/.env` 与宿主机 `C:\Users\KALOS` 路径；修复 6 个遗留 Stage4 生成器 `innerHTML`/`href="$2"` XSS；脱敏 `ws0n_v6_rebuild/r2_candidates.json` | 全部非 workflow `.py` 脚本 `py_compile` 0 语法错误；`security_utils.py` 全套安全单测 PASS；跨项目 `.env`/`KALOS` 活跃代码命中归零 |
| **Layer 4 · Agent Skills 与模板 (`03_` & `.agents/`)** | 下线遗留 `KOL--ziliao`（设 `user-invocable: false`、清除 23-Key 明文池与免确认 `git add -A && git push` 指令）；修复 `ai_mentor_module.html` 与 `handbook_skeleton.html` 属性逃逸 XSS、移除 `api.b.ai` 预连接；重构 `opentwitter` 为专属 `API_6551_TOKEN` 与参数化安全调用；增强 `kol-archive-builder` 短链白名单、防提示词注入边界与 5 项前端安全回归门禁 | 03_ 与 `.agents/` 0 残留硬编码密钥 |
| **Layer 5 & 6 · Git 仓库安全基建 (`01_Trader-Archives`)** | 修复 `.gitignore` UTF-8 BOM 并补齐 `.env.*`/`*.key`/`*.pem`/`*cookie*`/`*_ultra_raw.json`/`*_harvest_report.json`；新增 `SECURITY.md`、`.gitleaks.toml`、`.github/CODEOWNERS`；将 `.github/workflows/security-audit.yml` 全部 Actions 锁定至官方验证 40 位 Commit SHA，并升级 `scripts/security_verify.py` 门禁 | 冻结标杆站 `thankucrypto/`、`laoemo/` 与全部 `*_ultra_raw.json` 原始备份 0 改动 |
