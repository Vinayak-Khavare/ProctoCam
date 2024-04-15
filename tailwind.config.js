/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    // screens: {
    //   "2xl": { max: "1535px" },
    //   // => @media (max-width: 1535px) { ... }
    //
    //   negxl: { max: "1279px" },
    //   // => @media (max-width: 1279px) { ... }
    //
    //   neglg: { max: "1023px" },
    //   // => @media (max-width: 1023px) { ... }
    //
    //   negmd: { max: "767px" },
    //   // => @media (max-width: 767px) { ... }
    //
    //   negsm: { max: "639px" },
    //   // => @media (max-width: 639px) { ... }
    // },
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["garden", "sunset"],
  },
};
