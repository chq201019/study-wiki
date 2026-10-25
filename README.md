# chennet 的学习站 · ESP32 / 编程中文教程

一个开源的**中文编程与嵌入式教程站**源码。用 [Docusaurus 3](https://docusaurus.io/) 构建，纯静态、无后端依赖。

线上站点：<https://study.chennet.dpdns.org>

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

本仓库采用**双许可**，按内容类型区分：

| 范围 | 许可 | 全文 |
| --- | --- | --- |
| 教程内容：`docs/`、`static/img/`、`PROJECT.md` | **CC BY-NC-SA 4.0**（署名—非商业—相同方式共享） | [LICENSE-CONTENT-CC-BY-NC-SA-4.0.md](./LICENSE-CONTENT-CC-BY-NC-SA-4.0.md) |
| 代码：`scripts/`、`src/`、配置文件 | **MIT** | [LICENSE](./LICENSE) |

简而言之：

- 转载/改编教程请**署名 + 注明是否修改 + 用同样许可**分发，且**不能用于商业目的**
- 脚本和站点代码随便用，保留版权声明即可

商业使用请联系作者单独授权。
