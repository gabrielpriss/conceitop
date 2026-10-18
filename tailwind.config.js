/* Configuração do Tailwind compilado (antes era o CDN no navegador).
   Gerar o CSS: bash scripts/build-css.sh  (saída versionada em assets/css/tailwind.css) */
module.exports = {
  content: [
    './index.html',
    './404.html',
    './quem-somos/index.html',
    './contato/index.html',
    './blog/**/*.html',
    './servicos/**/*.html',
    './industrial/**/*.html',
    './b2b/**/*.html',
    './trabalhe-conosco/**/*.html',
    './partials/*.html',
    './assets/js/**/*.js',
    './scripts/*.py',
    './scripts/*.mjs',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Cairo', 'sans-serif'],
        serif: ['Tachyon', 'Share Tech', 'sans-serif'],
        display: ['Cosild', 'Michroma', 'sans-serif'],
      },
      colors: {
        prime: { 50: '#fafafa', 100: '#f0f0f0', 200: '#d9d9d9', 300: '#a3a3a3', 400: '#6b6b6b', 500: '#4a4a4a', 600: '#353535', 700: '#2a2a2a', 800: '#1f1f1f', 900: '#161616', 950: '#0d0d0d' },
        gold: { 300: '#fce88a', 400: '#f7cc19', 500: '#e5b800', 600: '#c9a000' },
        accent: { DEFAULT: '#ff4c01', light: '#ff7a3d', pale: '#ffd4b8' },
      },
    },
  },
  plugins: [],
};
