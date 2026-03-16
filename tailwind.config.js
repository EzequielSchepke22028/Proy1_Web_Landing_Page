/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'mercadolibre-yellow': '#FFF159',
        'mercadolibre-blue': '#3483FA',
        'mercadolibre-gray': '#EBEBEB',
      },
    },
  },
  plugins: [],
}