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
        canvas: '#f5f7f7',
        ink: '#1b303b',
        muted: '#4f626c',
        placeholder: '#657781',
        brand: '#087c72',
        'brand-deep': '#06655d',
        'brand-soft': '#e6f3f0',
        'brand-line': '#b9dcd5',
        line: '#dee5e9',
        field: '#8fa2ac',
        notice: '#fffaf0',
        'notice-line': '#e8d4a3',
        'notice-ink': '#6d4d1b',
        danger: '#8a3d33',
        'danger-line': '#e4c9c4',
        'danger-soft': '#fcf4f2',
      },
      boxShadow: {
        panel: '0 1px 2px rgba(27, 48, 59, 0.04)',
      },
    },
  },
  plugins: [],
} satisfies Config
