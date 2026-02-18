/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        gaming: { primary: '#00ff88', secondary: '#a855f7', bg: '#0a0e17', card: '#111827' },
        business: { primary: '#f59e0b', secondary: '#1e3a5f', bg: '#0f172a', card: '#1e293b' },
        developer: { primary: '#06b6d4', secondary: '#8b5cf6', bg: '#0c0a09', card: '#1c1917' },
      },
      animation: {
        'pulse-slow': 'pulse 3s infinite',
        'bounce-slow': 'bounce 2s infinite',
        'flip': 'flip 0.6s ease-in-out',
      },
      keyframes: {
        flip: {
          '0%': { transform: 'rotateY(0deg)' },
          '100%': { transform: 'rotateY(180deg)' },
        }
      }
    },
  },
  plugins: [],
}
