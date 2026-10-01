import type {Config} from '@docusaurus/types';

// DOCCAD Prototype Site Configuration (AD-2, AD-3, AD-12, AD-13).
const config: Config = {
  title: 'DOCCAD — AI-Augmented Documentation System',
  tagline: 'docs-as-code, static-first, AI-in-CI — prototype',
  url: 'https://w7-mgfcode.github.io',
  baseUrl: '/doCCAD_pre/',
  favicon: undefined,
  trailingSlash: false,

  // AD-10: broken internal links are a merge-blocking failure.
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'hu'],
    localeConfigs: {
      en: {
        label: 'English',
      },
      hu: {
        label: 'Magyar (Hungarian)',
      },
    },
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
      onBrokenMarkdownImages: 'throw',
    },
  },

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        // CANONICAL plane (AD-3): human-owned, route /docs.
        id: 'source',
        path: 'docs/source',
        routeBasePath: 'docs',
        sidebarPath: './sidebars-source.ts',
        editUrl: undefined,
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        // GENERATED plane (AD-3): bot-authored via PR only, route /views.
        id: 'generated',
        path: 'docs/generated',
        routeBasePath: 'views',
        sidebarPath: './sidebars-generated.ts',
        editUrl: undefined,
      },
    ],
    '@docusaurus/plugin-content-pages',
  ],

  themes: [
    [
      '@docusaurus/theme-classic',
      {
        customCss: './src/css/custom.css',
      },
    ],
    // AD-2 / content_architecture §7: Mermaid-as-code for all diagrams.
    '@docusaurus/theme-mermaid',
    // AD-13: Build-time local search index
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en', 'hu'],
        indexDocs: true,
        indexPages: true,
        docsRouteBasePath: ['docs', 'views'],
        docsDir: ['docs/source', 'docs/generated'],
        docsPluginIdForPreferredVersion: 'source',
      },
    ],
  ],

  themeConfig: {
    mermaid: {
      options: {
        securityLevel: 'strict',
      },
    },
    navbar: {
      title: 'DOCCAD',
      items: [
        {to: '/docs/overview', label: 'Docs (Canonical)', position: 'left'},
        {to: '/views/recruiter/project-overview', label: 'Recruiter View', position: 'left'},
        {to: '/explorer', label: 'Knowledge Explorer', position: 'left'},
        {to: '/workbench', label: 'Question Workbench', position: 'left'},
        {to: '/inspector', label: 'Drift Inspector', position: 'left'},
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {label: 'Canonical Docs', to: '/docs/overview'},
            {label: 'Architecture Spine', to: '/docs/architecture/system-overview'},
            {label: 'ADRs', to: '/docs/decisions/adr-001-github-source-of-truth'},
          ],
        },
        {
          title: 'Governed Views',
          items: [
            {label: 'Recruiter Briefing', to: '/views/recruiter/project-overview'},
            {label: 'Interview Guides', to: '/views/interview/architecture-system-overview'},
            {label: 'Question Answers', to: '/views/questions/q-001-canonical-separation'},
          ],
        },
        {
          title: 'Workbenches',
          items: [
            {label: 'Knowledge Explorer', to: '/explorer'},
            {label: 'Question Workbench', to: '/workbench'},
            {label: 'Drift Inspector', to: '/inspector'},
          ],
        },
      ],
      copyright:
        'DOCCAD Prototype — Canonical content under /docs is human-owned; derived views under /views are AI-generated through governed PR workflows.',
    },
  },
};

export default config;
