import type {Config} from '@docusaurus/types';

// GitHub-Native AI Documentation System — PoC site config.
// Implements AD-2 (Docusaurus publishing foundation), AD-3 (two content planes as
// two docs-plugin instances), AD-12 (filesystem i18n, EN canonical, HU fallback).
const config: Config = {
  title: 'GitHub-Native AI Documentation System',
  tagline: 'docs-as-code, static-first, AI-in-CI — proof of concept',
  url: 'https://example.github.io',
  baseUrl: '/',
  favicon: undefined,

  // AD-10: broken internal links are a merge-blocking failure.
  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'hu'],
  },

  markdown: {
    mermaid: true,
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
  ],

  themeConfig: {
    navbar: {
      title: 'AI Docs PoC',
      items: [
        {to: '/docs/overview', label: 'Docs (canonical)', position: 'left'},
        {
          to: '/views/recruiter/project-overview',
          label: 'Views (generated)',
          position: 'left',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright:
        'PoC — canonical content under /docs is human-owned; everything under /views is AI-generated and merged only through reviewed PRs.',
    },
  },
};

export default config;
