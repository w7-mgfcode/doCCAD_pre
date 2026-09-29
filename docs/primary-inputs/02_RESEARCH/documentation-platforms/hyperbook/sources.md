# Sources — Hyperbook analysis (all accessed 2026-08-12)

## Repository (primary evidence base)

Cloned https://github.com/openpatch/hyperbook to /tmp/hyperbook (shallow, then history fetched with --filter=blob:none for contributor stats; HEAD dated 2026-08-11).

| Path | What it evidenced |
|---|---|
| README.md | Project purpose (interactive workbooks), package inventory, maintainer (Mike Barkmin / OpenPatch), Matrix community, no @hyperbook/toolkit package exists |
| LICENSE.md | MIT license, copyright Mike Barkmin 2021 |
| package.json, pnpm-workspace.yaml | pnpm monorepo, changesets release flow, website EN/DE diff script, no Next.js in current stack |
| packages/hyperbook/{index.ts,build.ts,dev.ts,incremental.ts,archive.ts} | CLI surface (new/dev/build), full static build to .hyperbook/out, lunr search index generation (build.ts:36-97), llms.txt generation (build.ts:283-412, 969-971), dev-only IncrementalBuilder with dependency tracking, WebSocket live reload (dev.ts:267-353), Node>=18 engines |
| packages/hyperbook/tests/incremental.test.ts | Incremental builder test coverage |
| packages/markdown/src/process.ts | Full remark/rehype pipeline; 40 directive plugins registered; shiki highlighting; KaTeX; allowDangerousHtml default false |
| packages/markdown/src/remarkDirective*.ts (40 files) | Verified element list: tabs, protect, mermaid, plantuml, excalidraw, geogebra, h5p, pyide, sqlide, webide, onlineide, multievent, textinput, learningmap, scratchblock, struktog, struktolab, blockflow, kirimoto, openscad, typst, abc-music, jsxgraph, alert, collapsible, slideshow, tiles, bookmarks, pagelist, term, qr, download, archive, embed, video, audio, youtube, unpack; no literal multiple-choice directive |
| packages/markdown/src/remarkDirectiveMermaid.ts | Dual mermaid syntax (fenced + directive), base64 payload, client-side render |
| packages/markdown/src/remarkDirectiveProtect.ts | protect = client-side gating; base64 password in data-toast; content in hidden div |
| packages/markdown/src/rehypeHtmlStructure.ts (lines ~200-280) | Emitted head metadata; verified defects: og:title uses value attr, keywords.join(""), html lang fallback "es", no canonical/sitemap/og:image |
| packages/markdown/src/i18n.ts + locales | UI i18n: only en.json and de.json bundles; English fallback |
| packages/markdown/assets/ | Per-directive JS/CSS assets incl. mermaid.min.js, lunr-adjacent search UI, store.js |
| packages/types/src/index.ts | hyperbook.json schema (search, llms, importExport, colors, fonts, scripts/styles, basePath, repo, cloud, elements config); Language union de|en|fr|es|it|pt|nl (no hu); frontmatter types incl. permaid, hide, virtual sections; HyperlibraryJson multi-book model |
| packages/fs/src/vfile.ts | Folder model (book/glossary/public/snippets/archives); .md.yml/.md.json data files requiring template; .md.hbs pages; dependency tracking for inlined snippets/templates; warning-only error handling (lines ~840-900) |
| packages/fs/src/handlebars.ts | ~20 Handlebars helpers (times, concat, case transforms, truncate, dateformat, rbase64, rfile...) |
| packages/create/package.json | create-hyperbook scaffolder |
| packages/web-component-excalidraw/package.json | React 19 web component packaged via r2wc — pattern for custom components via scripts |
| platforms/vscode/package.json | hyperbook-studio VS Code extension 0.54.0: activation, schema validation, snippets, preview |
| platforms/cloud/{README.md,Dockerfile,docker-compose.yml} | Optional self-hosted Express student-data backend, Docker/GHCR distribution — out of scope for target system |
| .github/workflows/changeset-version.yml | CI: changesets publish to npm, VS Code Marketplace + OpenVSX, GHCR cloud image; permissions surface |
| renovate.json | Automated dependency updates |
| website/hyperlibrary.json, website/en/**, website/de/** | Real EN/DE bilingual library config; docs corpus incl. elements/, hosting/{ghpages,glpages,vercel,custom}.md, advanced/ template demos |
| scripts/diffFolders.mjs (via package.json website:diff) | Translation drift detection pattern |
| git log/shortlog (full history) | First commit 2022-03-08; ~1010 human commits, 910+55 by maintainer, 2 external contributors x 1 commit; 220 commits in last 6 months |

## Web (secondary)

| URL | What it evidenced |
|---|---|
| https://github.com/openpatch/hyperbook (via web fetch) | Stars 74, forks 14, watchers 2, open issues 5, 1924 commits (2026-08-12) |
| https://github.com/openpatch/hyperbook/issues | 5 open issues, titles/dates incl. #350 OpenGraph Images (2022), #349 page/section password |
| https://registry.npmjs.org/hyperbook | Latest 0.104.0 published 2026-08-11T21:10Z; release timestamps showing 11 releases 2026-07-25..08-11 |
| https://hyperbook.openpatch.org/ | Official docs site (same content as website/ in repo; used for orientation) |
| https://github.com/openpatch/hyperbook-anywhere | Deployment starter template (search result; existence verified) |

Notes: GitHub REST API was blocked in this session; stars/forks/issues were observed via rendered pages and are marked [OBSERVED]. All code claims are [VERIFIED-REPO] from the local clone.
