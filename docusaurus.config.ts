import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'chennet 的学习站',
  tagline: '软件与硬件双主线：Python / C / C++ · ESP / STM / Linux',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://study.chennet.dpdns.org',
  baseUrl: '/',

  organizationName: 'chennet',
  projectName: 'study-wiki',

  onBrokenLinks: 'throw',
  onDuplicateRoutes: 'throw',

  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans'],
  },

  markdown: {
    mermaid: true,
  },

  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        indexDocs: true,
        indexBlog: false,
        indexPages: true,
        docsRouteBasePath: ['docs'],
        // 搜索索引构建后由 scripts/postbuild.js 复制到 /assets/search-index.js，
        // nginx 再把 /search-index.json 302 重定向过去。
        // 原因：Cloudflare 免费版的默认缓存扩展名列表里没有 .json，
        // 用 .js 承载才能命中边缘缓存。
        highlightSearchTermsOnTargetPage: true,
        searchResultLimits: 10,
        searchBarShortcut: true,
        searchBarShortcutHint: true,
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
          showLastUpdateTime: false,
        },
        blog: false,
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'chennet 的学习站',
      hideOnScroll: true,
      logo: {
        alt: 'chennet 的学习站',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'dropdown',
          label: '软件编程',
          position: 'left',
          items: [
            {type: 'doc', docId: 'software/index', label: '软件总览'},
            {type: 'docSidebar', sidebarId: 'pythonSidebar', label: 'Python'},
            {type: 'docSidebar', sidebarId: 'cSidebar', label: 'C 语言'},
            {type: 'docSidebar', sidebarId: 'cppSidebar', label: 'C++'},
          ],
        },
        {
          type: 'dropdown',
          label: '硬件开发',
          position: 'left',
          items: [
            {type: 'doc', docId: 'hardware/index', label: '硬件总览'},
            {type: 'docSidebar', sidebarId: 'espSidebar', label: 'ESP32'},
            {type: 'docSidebar', sidebarId: 'stmSidebar', label: 'STM32'},
            {type: 'docSidebar', sidebarId: 'linuxSidebar', label: 'Linux'},
            {type: 'docSidebar', sidebarId: 'othersSidebar', label: '其他芯片'},
          ],
        },
        {
          type: 'docSidebar',
          sidebarId: 'aiSidebar',
          position: 'left',
          label: 'AI 辅助开发',
        },
        {
          type: 'docSidebar',
          sidebarId: 'referenceSidebar',
          position: 'left',
          label: '速查表',
        },
        {to: '/docs/reference/examples', label: '参考示例', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '软件编程',
          items: [
            {label: 'Python', to: '/docs/software/python/'},
            {label: 'C 语言', to: '/docs/software/c/'},
            {label: 'C++', to: '/docs/software/cpp/'},
          ],
        },
        {
          title: '硬件开发',
          items: [
            {label: 'ESP 系列', to: '/docs/hardware/esp/'},
            {label: 'STM 系列', to: '/docs/hardware/stm/'},
            {label: 'Linux 系列', to: '/docs/hardware/linux/'},
          ],
        },
        {
          title: '快速上手',
          items: [
            {label: '开始前避坑', to: '/docs/quickstart/board'},
            {label: '装驱动认出板子', to: '/docs/quickstart/driver-setup'},
            {label: '装米思齐跑通第一个', to: '/docs/quickstart/mixly-setup'},
            {label: '串口与调试', to: '/docs/quickstart/debug'},
          ],
        },
        {
          title: '其他专栏',
          items: [
            {label: '其他芯片', to: '/docs/chips/'},
            {label: 'AI 辅助开发', to: '/docs/ai-coding/'},
          ],
        },
        {
          title: '资源',
          items: [
            {label: '参考示例库', to: '/docs/reference/examples'},
            {label: '错误码速查', to: '/docs/reference/error-codes'},
            {label: '引脚映射', to: '/docs/reference/pinout'},
          ],
        },
        {
          title: '联系',
          items: [
            {label: '邮箱 chq201019@163.com', href: 'mailto:chq201019@163.com'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} study.chennet.dpdns.org · Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'c', 'cpp', 'ini', 'makefile', 'cmake', 'python', 'json'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;