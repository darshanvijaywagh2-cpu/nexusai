/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0a',
        foreground: '#ededed',
        card: '#171717',
        'card-foreground': '#ededed',
        primary: '#6366f1',
        'primary-foreground': '#ffffff',
        secondary: '#27272a',
        'secondary-foreground': '#ededed',
        muted: '#27272a',
        'muted-foreground': '#a1a1aa',
        accent: '#27272a',
        'accent-foreground': '#ededed',
        destructive: '#7f1d1d',
        border: '#27272a',
        input: '#27272a',
        ring: '#6366f1',
      },
    },
  },
  plugins: [],
}
