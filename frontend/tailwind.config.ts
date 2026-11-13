import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Segoe UI', 'Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['Cascadia Code', 'Consolas', 'Liberation Mono', 'monospace'],
      },
      colors: {
        canvas: '#f6f8fa',
        ink: '#1b303b',
        muted: '#536670',
        placeholder: '#647680',
        brand: '#087c72',
        'brand-soft': '#e4f3ef',
        line: '#dee5e9',
        field: '#93a5af',
        notice: '#fffaf0',
        'notice-line': '#ebd8a5',
        'notice-ink': '#72521d',
      },
    },
  },
  plugins: [],
} satisfies Config
