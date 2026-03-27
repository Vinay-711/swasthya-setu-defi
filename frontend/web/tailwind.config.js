/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#2563eb", dark: "#1d4ed8", light: "#eff6ff" },
        accent: { DEFAULT: "#7c3aed", dark: "#6d28d9", light: "#f5f3ff" },
        success: { DEFAULT: "#16a34a", light: "#f0fdf4" },
        warning: { DEFAULT: "#d97706", light: "#fffbeb" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
      },
    },
  },
  plugins: [],
};
