/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0a0f0a',
          light: '#0f1810',
          dark: '#050805',
        },
        secondary: {
          DEFAULT: '#141f14',
          light: '#1b2e1b',
          dark: '#0d140d',
        },
        accent: {
          green: '#00ff88',
          'green-dark': '#00cc6a',
          'green-light': '#33ffaa',
          red: '#ff3366',
          'red-dark': '#cc2952',
          yellow: '#ffaa00',
          'yellow-dark': '#cc8800',
        },
        text: {
          primary: '#e8f5e9',
          secondary: '#81c784',
          muted: '#4a5f4a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'glow-green': '0 0 20px rgba(0, 255, 136, 0.3)',
        'glow-green-lg': '0 0 40px rgba(0, 255, 136, 0.4)',
        'glow-red': '0 0 20px rgba(255, 51, 102, 0.3)',
        'glow-yellow': '0 0 20px rgba(255, 170, 0, 0.3)',
      },
    }
  },
  plugins: []
};