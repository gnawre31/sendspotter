/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/pages/**/*.{js,jsx,ts,tsx}",
    "./src/sections/**/*.{js,jsx,ts,tsx}",
    "./src/components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["graphik"],
        serif: ["graphik"],
        mono: ["graphik"],
        display: ["graphik"],
        body: ["graphik"],
      },
    },
  },
  plugins: [],
};
