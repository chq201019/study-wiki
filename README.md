# chennet 的学习站 · ESP32 / 编程中文教程

一个开源的**中文编程与嵌入式教程站**源码。用 [Docusaurus 3](https://docusaurus.io/) 构建，纯静态、无后端依赖。

> **线上站点**：<https://study.chennet.dpdns.org>
> **内容后台**：<https://study.chennet.dpdns.org/admin/>
> **仓库地址**：<https://github.com/chq201019/study-wiki>

## 这个站讲什么

两条主线，各自独立成篇：

| 主线 | 内容 | 入口 |
| --- | --- | --- |
| **软件编程** | Python · C · C++，从语法到内存模型、并发、工程化 | `docs/software/` |
| **硬件开发** | ESP32（S3 主线）· STM32 · Linux 嵌入式 | `docs/hardware/` |

外加：

- **快速上手**（`docs/quickstart/`）：全程米思齐拖积木，零基础做出能跑的东西，不讲原理
- **赛事实战**（`docs/quickstart/competition/`）：一次性的比赛内容，可整目录删除
- **速查表**（`docs/reference/`）：引脚映射、API 对照、错误码、示例库
- **AI 辅助开发**（`docs/ai-coding/`）：怎么让 agent 真正干活，而不是产出一堆看起来对的代码

## 内容原则

这个站的代码示例尽量**在本机实测**过，输出直接贴原文；凡是无法实测的地方会明确标注依据来源。勘误时优先修「读者照着做会出错」的问题——比如错误的引脚号、编译不过的分区表、说反的机制。

每页统一结构：目标 → 原理 → 接线/配置 → 代码 → 验证 → 常见坑 → 下一步。

## 本地开发

```bash
npm install
npm start        # http://localhost:3000
npm run build    # 产出 build/
npm run serve    # 本地预览生产构建
```

技术栈：Docusaurus 3.10 + TypeScript + 本地搜索（`@easyops-cn/docusaurus-search-local`，不依赖 Algolia）+ mermaid 图。

## 目录结构

```text
docs/
├── software/            Python / C / C++（每条线有「零基础」与「进阶」两档）
├── hardware/
│   ├── esp-basics/      ESP32 零基础
│   ├── stm-basics/      STM32 零基础
│   └── linux/           Linux 进阶（含 linux-basics/）
├── course/              ESP32 完整教程 L0~L7
├── chips/               STM32 深讲 + 其他芯片
├── quickstart/          米思齐快速上手 + 赛事实战
├── reference/           速查表
└── ai-coding/           AI 辅助开发

static/img/diagrams/     示意图（由 scripts/gen_diagrams*.py 生成，可重跑）
scripts/                 示意图生成器 + 内容校验脚本
```

## 部署

### 环境与前置

| 项 | 要求 |
| --- | --- |
| Node.js | **>= 20**（`package.json` 的 `engines` 限定，低版本构建直接失败） |
| 依赖安装 | `npm install`（首次或 `package-lock.json` 变更后） |
| 服务器 | 已装好 nginx + cloudflared + `systemctl` 的 Linux 主机 |

服务器上的目录约定（`/opt/study-wiki/`）：

```text
app/         站点源码，线上就是从它构建的（node_modules 已装好）
www/         构建产物，nginx 指向这里
backups/     后台每次保存前的 mdx 备份
build.log    构建日志
publish.sh   发布脚本：预压缩 + 原子替换 www/ + reload nginx
admin/       内容后台服务（零依赖 Node）
```

### 方式一：内容后台（只改 `docs/**/*.mdx` 时最快）

打开 <https://study.chennet.dpdns.org/admin/> → 输密码 → 点页面 → 改 → **保存并发布**。

后台自动完成：备份旧版到 `backups/` → 构建 → 预压缩 → 原子替换 `www/` → 重载 nginx，约 40 秒。**构建失败不会影响线上**，仍是上一个可用版本。编辑框上方有「选择图片」，上传后自动插入 `![说明](路径)`。

> ⚠️ 后台只接受 `docs/**/*.mdx`。改 `docusaurus.config.ts`、`sidebars.ts`、`src/`、`static/` 必须走方式二。

### 方式二：本地改完推送（改配置 / 侧边栏 / 首页时用）

```powershell
npm run build                          # 先在本地确认构建通过
.\scripts\push.ps1                     # 打包 → 上传 → 服务器构建 → 发布
```

`push.ps1` 打包 `docs/ src/ static/ docusaurus.config.ts sidebars.ts scripts package.json package-lock.json`，上传后在服务器解包构建并发布，执行时会提示输入服务器密码。

手动等价流程（`push.ps1` 不可用时）：

```bash
# 本地
tar -czf content.tar.gz -C . docs src static docusaurus.config.ts sidebars.ts scripts package.json package-lock.json
# 上传后，在服务器执行
tar -xzf content.tar.gz -C /opt/study-wiki/app
cd /opt/study-wiki/app && npm run build && sh /opt/study-wiki/publish.sh build
```

### 回滚

后台每次保存都在 `backups/` 留了旧版，直接覆盖回去再重新发布：

```bash
ls -t /opt/study-wiki/backups/ | head              # 找要回滚的 .bak
cp /opt/study-wiki/backups/<文件名>.bak /opt/study-wiki/app/docs/<原路径>
cd /opt/study-wiki/app && npm run build && sh /opt/study-wiki/publish.sh build
```

### 常见故障

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 发布后页面没变化 | 只改了 `docs/` 之外的文件 | 配置类改动走 `push.ps1`，后台不处理 |
| 构建卡住或内存爆掉 | `.cache/` 原生插件缓存异常 | 删掉 `/opt/study-wiki/.cache/` 后重跑构建 |
| 后台打不开 | `study-admin` 服务挂了 | `systemctl status study-admin` / `journalctl -u study-admin -f` |
| 站点 502 | nginx 或 cloudflared 异常 | `nginx -t && systemctl reload nginx` |

### 部署前自检

本地 `npm run build` 必须通过——**MDX 编译错误会让整站发布失败**，而服务器上的失败只在 `build.log` 里看得到。提交前再跑一遍下面「内容校验」里的脚本。

## 内容校验

提交前跑这几个脚本（本地几秒钟，能拦下绝大多数构建失败）：

```bash
node scripts/check_sidebar.js         # sidebars.ts 语法
python scripts/check_docid.py         # doc id 与文件名一致
python scripts/check_jsx_safe.py      # 正文裸 < 会被当 JSX
python scripts/check_links.py         # 相对链接是否指向真实页面
python scripts/check_mdx_all.py       # admonition ::: 配对
python scripts/check_frontmatter.py   # frontmatter 合法性
```

示意图可重跑生成：

```bash
python scripts/gen_diagrams.py        # 输出到 static/img/diagrams/
```

## 约定

- 每页 frontmatter 必须有 `title` / `sidebar_position` / `description`
- `index.mdx` 不要写 `id:`（会整体替换路径 id，多个 index 会撞车）
- 站内链接指向目录首页写 `../xxx/`，不写 `../xxx/index`
- admonition 用方括号标题语法 `:::tip[标题]`；MDX 不支持 `<!-- -->` 注释
- 一页不超过约 2000 行，超了就拆

## 许可

本仓库**全部内容**（教程文字、图片、脚本、站点代码）统一采用 [MIT License](./LICENSE)。

这意味着你可以自由地：**使用、复制、修改、合并、发布、分发、再许可、销售** —— 包括商业用途，
无需通知作者、无需分成。唯一要求是保留版权声明与许可声明。

> 本项目此前对教程内容使用 CC BY-NC-SA 4.0（禁止商业使用）。
> 自本次提交起统一改为 MIT，**此前的非商业限制不再适用于后续版本**。

