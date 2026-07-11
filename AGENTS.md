# InsuranceTipsPro

## 基础信息
- 域名：insurancetipspro.com
- 主色：#1e40af（深蓝）+ #ea580c（橙 CTA）
- GA ID：G-DQ4ZT8RD2R
- 内容数量：35篇博客文章 + about + contact + privacy
- 部署方式：Hostinger FTP（node deploy-ftp.js）
- CSS：style.css（单文件，含完整编辑级排版）

## 当前进度
- AdSense 状态：准备就绪，可提交审核 [2026-06-19]
- 上次审计完成：2026-06-19（完整12项审计 + 11项修复）
- 通过概率评估：90%+
- 本轮完成事项 [2026-06-19]：
  - 删除 "no ads disguised as advice" 红线文案
  - 创建 privacy.html（AdSense 必需）+ 全站37页添加链接
  - 删除首页3篇重复文章条目 + StructuredData 重复
  - 创建4个SVG占位图 + 修复5篇文章图片404
  - 修复 business-insurance-types meta description HTML标签
  - Hero 统计 21+ → 35+，重建分页（page2，删page3/4）
  - auto-publish.js 补充20个新topic
  - deploy-ftp.js 排除列表追加7个开发文件
  - contact.html 改 Formspree 表单（占位ID待替换）
- 下一步：提交 AdSense 审核

## 专属配置
- FTP：212.85.28.149 / u868313694.insurancetipspro.com / Xxh113324~ / public_html
- auto-publish.js：自动发文系统（Unsplash取图 → Claude CLI生成 → HTML → FTP部署）
- topics-used.json：已用33个 + 新增20个候选 = 还剩约20个可用
- Formspree 表单ID：xyzgobkp（占位，需替换真实ID）

## 关键修复历史
- [2026-06-19] "no ads disguised as advice" → "Honest, unbiased coverage guidance"（AdSense红线）
- [2026-06-19] privacy.html 缺失 → 已创建完整隐私政策页
- [2026-06-19] 首页 medicare/types-of-car 文章重复 → 删除重复条目+StructuredData
- [2026-06-19] 5篇文章 .png 图片404 → 创建SVG + 替换引用
- [2026-06-19] FTP排除列表不完整 → 追加 AGENTS.md/CLAUDE.md/package.json 等

## Amazon Associates 变现页 [2026-06-22]
- **共用 Tracking ID**：`bizpolicyguid-20`（与 BusinessPolicyGuide 同账号，统一管理）
- **新增变现页**：`/articles/best-insurance-books.html` — 8本理财书单（24个真实Amazon链接）
- **OneLink**：已注入双重OneLink脚本（官方JS + 时区检测fallback），支持9国跳转
- **首页插入**：Latest Articles第1位
- **180天3单计时**：从2026-06-22起，需通过此页面链接产生3笔合格销售（与BPG共享180天计数）

## 待办
- [ ] 替换 contact.html Formspree 占位ID为真实ID
- [ ] 提交 AdSense 审核
- [ ] 继续用 auto-publish.js 发文扩充内容量
- [ ] Skimlinks通过后单独申请此站domain（在Skimlinks后台 Settings → Domains → Add）

## 2026-06-20 Codex 复核更新
- 复核 Claude Code 优化后的站点：39 个 HTML 页面通过本地静态检查，无本地资源缺失、无 JSON-LD 解析错误、无 `data-ad-slot` 手动广告位、无 `check-purchase.php` 后端残留。
- AdSense/YMYL 风险收敛：删除或降级 “reviewed by licensed professionals” 等强资质表述，改为教育内容、清晰度和实用准确性定位。
- 新增 `terms.html`，并全站页脚补齐 Privacy / Terms / Contact；`sitemap.xml` 增加 privacy/terms 并去重。
- 统一联系邮箱为 `xiaohuixie3@gmail.com`，修复 `contact@...` 与 `hello@...` 不一致。
- 修复页脚残留的字面量 `` `n``。
- 所有指向 CoverageFixPro 的商业/工具外链统一加 `rel="sponsored nofollow noopener"`。
- 修复 `robots.txt` 中无效的 `/check-purchase.php` 禁止规则。
- 修复 `auto-publish.js`：FTP 部署失败时直接抛错，避免未成功发布的主题被写入 `topics-used.json`。
- 修复 `deploy-ftp.js`：新增远端清理，已从公网删除 `auto-publish.js`、`topics-used.json`、`package*.json`、`AGENTS.md`、`CLAUDE.md` 等私有/构建文件。
- 已部署并通过 Post-Deploy：`https://insurancetipspro.com/`、示例文章、JS 语法、内容新鲜度均通过。
## 2026-06-30 Auto-Publish LLM Fallback
- `auto-publish.js` now uses shared helper `C:\Users\Administrator\pm-worker\llm-json.js`.
- Article generation first tries Claude CLI with stdin ignored; if Claude fails, it falls back to the local OpenAI-compatible/DeepSeek configuration without printing secrets.
- Recovered failed daily publish: `articles/professional-liability-insurance.html`; deployed and post-deploy checks passed.

## 2026-07-09 文章 UI 组件化
- 优化文字密集型每日文章结构，降低纯文本堆叠感。
- `auto-publish.js` 现在会在导语后自动渲染决策卡片、行动/目录面板、工具 CTA 条。
- 已同步修复并部署最新文章：`articles/wedding-insurance-guide.html`。
- 组件类名：`article-insight-grid`、`article-action-panel`、`tool-strip`。
- QA：`node --check auto-publish.js` 通过；部署上传 `style.css` 和文章页；线上 HTML 返回 200，且包含全部组件类名和 `coveragefixpro.com`。

## 2026-07-11 portfolio AdSense preflight
- 2026-07-11 preflight: retained 51 long-form guides, added editorial review/evidence notes, noindexed pagination, and replaced unsupported professional-review/expert language. Auto-publish now runs the portfolio gate before FTP deployment.
- Required release check: `node C:\\Users\\Administrator\\pm-worker\\adsense-release-gate.js insurancetipspro`. Do not submit or deploy after a failed gate.
