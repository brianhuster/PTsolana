/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./view/**/*.{html,templ}"],
  theme: {
    extend: {
      colors: {
        'primary': "#2e3bc7",
        'secondary': "#22e3cc",
        'foreground': "0b0c0c",
        'base': {
          100: "#ffffff",
          200: "#d7d9df",
          300: "#D1D5DB",
        }
      },
    },
  },
  plugins: [],
}

