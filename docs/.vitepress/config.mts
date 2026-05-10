import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'


// https://vitepress.dev/reference/site-config
export default withMermaid(
  defineConfig({
  base: '/data-platform-lab/',   
  title: "Data Platform Lab",
  description: "AI Native Data Engineering and Platform Engineering Lab",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
  { text: 'Home', link: '/' },
  { text: 'Architecture', link: '/architecture/' },
  { text: 'Pipelines', link: '/pipelines/' },
  { text: 'CI/CD', link: '/cicd/' },
  { text: 'Observability', link: '/observability/' },
  { text: 'Labs', link: '/labs/' }
    ],
sidebar: [
  {
    text: 'Architecture',
    items: [
      { text: 'Overview', link: '/architecture/' }
    ]
  },
  {
    text: 'Pipelines',
    items: [
      { text: 'Overview', link: '/pipelines/' }
    ]
  },
  {
    text: 'CI/CD',
    items: [
      { text: 'Overview', link: '/cicd/' }
    ]
  },
  {
    text: 'Observability',
    items: [
      { text: 'Overview', link: '/observability/' }
    ]
  },
  {
    text: 'Labs',
    items: [
      { text: 'Overview', link: '/labs/' }
    ]
  }
],

    socialLinks: [
      
    ]
  }
}))
