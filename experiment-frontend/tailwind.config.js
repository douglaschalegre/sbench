/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        display: ['Newsreader', 'Georgia', 'serif'],
      },
      colors: {
        canvas: '#f3f0e8', ink: '#17201b', forest: '#174b3a', moss: '#738f62',
        line: '#d8d4c8', paper: '#fbfaf6', amber: '#d97734',
      },
      boxShadow: { card: '0 18px 45px rgba(23,32,27,.08)' },
    },
  },
  plugins: [],
}
