import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'


// https://vitepress.dev/reference/site-config
export default withMermaid(  
  defineConfig({
  title: 'Insurance Data Platform',
  description: 'Data Engineering platform documentation',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Architecture', link: '/architecture/overview' },
      { text: 'Data Layers', link: '/layers/overview' },
      { text: 'Framework', link: '/framework/overview' },
      { text: 'Operations', link: '/operations/runbook' },
    ],
    sidebar: [
      {
        text: 'Platform',
        items: [
          { text: 'Overview', link: '/' },
          { text: 'CONTEXT.md (for AI)', link: '/CONTEXT' },
        ]
      },
      {
        text: 'Architecture',
        items: [
          { text: 'L1 / L2 Overview', link: '/architecture/overview' },
        ]
      },
      {
        text: 'Data Layers',
        items: [
          { text: 'Raw → History → Active', link: '/layers/overview' },
        ]
      },
      {
        text: 'Orchestration Framework',
        items: [
          { text: 'Chain / Group Pattern', link: '/framework/overview' },
          { text: 'Audit Tables (aud_*)', link: '/framework/audit-tables' },
        ]
      },
      {
        text: 'Operations',
        items: [
          { text: 'Runbook', link: '/operations/runbook' },
        ]
      },
    ],
    socialLinks: [],
  },
  markdown: {
    theme: 'github-dark',
  }
})
)