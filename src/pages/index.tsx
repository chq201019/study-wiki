import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

type Track = {
  title: string;
  tag: string;
  desc: string;
  meta: string;
  to: string;
  items: string[];
  primary?: boolean;
};

const TRACKS: Track[] = [
  {
    title: '软件编程',
    tag: 'Python / C / C++',
    desc: '把语言本身学透。不教框架怎么调 API，讲的是这门语言为什么这样设计——因为只有懂了原理，遇到没见过的报错才知道往哪查。',
    meta: '适用：想真正会用一门语言',
    to: '/docs/software/',
    items: [
      'Python：语法 → 数据类型 → 进阶 → 并发 → 工程化',
      'C：指针、内存模型、位运算、嵌入式 C、未定义行为',
      'C++：RAII、移动语义、模板、STL、嵌入式 C++',
      '每条线都从原理讲到应用再到进阶',
    ],
    primary: true,
  },
  {
    title: '硬件开发',
    tag: 'ESP / STM / Linux',
    desc: '让代码真正控制物理世界。硬件写错可能烧芯片、变砖，所以格外强调原理：电流走哪、寄存器怎么被改、芯片按什么顺序启动。',
    meta: '适用：做设备、做产品',
    to: '/docs/hardware/',
    items: [
      'ESP 系列：ESP32-S3，自带 WiFi，生态最好',
      'STM 系列：STM32，实时性强，工业主流',
      'Linux 系列：交叉编译、内核驱动、启动全链',
      '四层纵深：硬件 → 外设 → 系统 → 工程化',
    ],
  },
  {
    title: '快速上手',
    tag: '只教怎么用',
    desc: '面向完全零基础。全程米思齐拖积木不写代码，只教接线、拼积木、调通。2~3 天做出能演示能联网的完整小项目。',
    meta: '适用：现在就要出成果',
    to: '/docs/quickstart/',
    items: [
      '先避坑：USB 口、禁用引脚、供电',
      '装驱动让电脑认出板子',
      '装米思齐跑通第一个程序',
      'WiFi 配网 + MQTT 上云',
    ],
  },
  {
    title: 'AI 辅助开发',
    tag: 'Agent 流',
    desc: '用 agent 干活，不是用网页聊天。目标写清楚、验收标准定好，改代码跑编译让 agent 自己转，人只做裁决和上机验证。',
    meta: '适用：提升开发效率',
    to: '/docs/ai-coding/',
    items: [
      '为什么 agent 优于网页端',
      '提示词工程：五类技巧包',
      'agent 开发工作流与 AGENTS.md',
      '识别 AI 幻觉与作弊式编译',
    ],
  },
];

function FeatureCard({track}: {track: Track}) {
  return (
    <div className={clsx('col col--3')}>
      <Link
        to={track.to}
        className={clsx('card', styles.card, track.primary && styles.cardPrimary)}>
        <div className={styles.cardHead}>
          <h3>{track.title}</h3>
          <span className={styles.tag}>{track.tag}</span>
        </div>
        <p className={styles.meta}>{track.meta}</p>
        <p className={styles.desc}>{track.desc}</p>
        <ul className={styles.items}>
          {track.items.map((it) => (
            <li key={it}>{it}</li>
          ))}
        </ul>
        <span className={clsx('button', 'button--lg', styles.btn)}>
          进入{track.title}
        </span>
      </Link>
    </div>
  );
}

function LangCard({name, desc, to}: {name: string; desc: string; to: string}) {
  return (
    <Link to={to} className={clsx('card', styles.miniCard)}>
      <h4>{name}</h4>
      <p>{desc}</p>
    </Link>
  );
}

export default function Home(): React.ReactElement {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="软件与硬件双主线学习站：Python / C / C++，ESP / STM / Linux">
      <header className={clsx('hero hero--primary', styles.hero)}>
        <div className="container">
          <div className={styles.heroInner}>
            <p className={styles.kicker}>软件编程 · 硬件开发</p>
            <h1 className={styles.title}>chennet 的学习站</h1>
            <p className={styles.subtitle}>
              一条路学软件：<Link to="/docs/software/python/">Python</Link>、
              <Link to="/docs/software/c/">C</Link>、
              <Link to="/docs/software/cpp/">C++</Link>；
              一条路学硬件：<Link to="/docs/hardware/esp/">ESP</Link>、
              <Link to="/docs/hardware/stm/">STM</Link>、
              <Link to="/docs/hardware/linux/">Linux</Link>。
              每条主线都从原理讲到应用再到进阶，代码示例尽量实测。
            </p>
            <div className={styles.buttons}>
              <Link className="button button--primary button--lg" to="/docs/software/">
                学软件编程
              </Link>
              <Link className="button button--secondary button--lg" to="/docs/hardware/">
                学硬件开发
              </Link>
            </div>
            <p className={styles.spec}>
              原理 → 可运行代码 + 真实输出 → 验证 → 常见坑 → 自检清单
            </p>
          </div>
        </div>
      </header>

      <main className="container margin-vert--lg">
        <div className="row">
          {TRACKS.map((t) => (
            <FeatureCard key={t.title} track={t} />
          ))}
        </div>
      </main>

      <section className={styles.strip}>
        <div className="container">
          <h3 className={styles.stripTitle}>六条主线，按你的方向挑</h3>
          <div className="row margin-bottom--lg">
            <div className="col col--6">
              <p className={styles.stripLabel}>软件编程</p>
              <div className="row">
                <div className="col col--4">
                  <LangCard
                    name="Python"
                    desc="上手最快，写工具、跑数据、做 AI"
                    to="/docs/software/python/"
                  />
                </div>
                <div className="col col--4">
                  <LangCard
                    name="C"
                    desc="嵌入式地基，指针与内存的真相"
                    to="/docs/software/c/"
                  />
                </div>
                <div className="col col--4">
                  <LangCard
                    name="C++"
                    desc="在 C 之上做零开销抽象"
                    to="/docs/software/cpp/"
                  />
                </div>
              </div>
            </div>
            <div className="col col--6">
              <p className={styles.stripLabel}>硬件开发</p>
              <div className="row">
                <div className="col col--4">
                  <LangCard
                    name="ESP 系列"
                    desc="ESP32-S3，自带 WiFi，入门首选"
                    to="/docs/hardware/esp/"
                  />
                </div>
                <div className="col col--4">
                  <LangCard
                    name="STM 系列"
                    desc="STM32，实时性强，工业主流"
                    to="/docs/hardware/stm/"
                  />
                </div>
                <div className="col col--4">
                  <LangCard
                    name="Linux 系列"
                    desc="交叉编译、内核驱动、启动全链"
                    to="/docs/hardware/linux/"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.strip}>
        <div className="container">
          <div className="row">
            <div className={clsx('col col--4')}>
              <h3>为什么代码要贴真实输出</h3>
              <p>
                教程最常见的错误不是讲错概念，而是给了一段跑不起来或者早就过时的代码。
                本站示例尽量在本机实测，输出直接贴原文，你能对照着确认自己走对了。
              </p>
            </div>
            <div className={clsx('col col--4')}>
              <h3>为什么不直接上框架</h3>
              <p>
                会调 API 不等于会用。时序错了就是调不通，内存越界了就是莫名其妙重启——
                这些必须靠原理解决。每页都从「为什么是这样设计的」讲起。
              </p>
            </div>
            <div className={clsx('col col--4')}>
              <h3>零基础该从哪进</h3>
              <p>
                想三天出成果：走<Link to="/docs/quickstart/">快速上手</Link>。
                想真学会：先<Link to="/docs/software/python/">Python</Link>建立编程直觉，
                或直接从<Link to="/docs/software/c/">C</Link>开始打地基。
              </p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}
