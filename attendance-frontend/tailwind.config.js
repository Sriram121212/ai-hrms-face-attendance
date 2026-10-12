/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#14202E",
          light: "#1E2E40",
          muted: "#5B6B7A",
        },
        canvas: "#F1F4F3",
        surface: "#FFFFFF",
        signal: {
          DEFAULT: "#1F8A57",
          soft: "#E4F3EB",
        },
        amber: {
          DEFAULT: "#C98A2E",
          soft: "#FBF0DE",
        },
        clay: {
          DEFAULT: "#B23A3A",
          soft: "#F9E7E7",
        },
        line: "#DDE3E1",
      },
      fontFamily: {
        serif: ["IBM Plex Serif", "Georgia", "serif"],
        sans: ["IBM Plex Sans", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      borderRadius: {
        card: "10px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(20, 32, 46, 0.06), 0 1px 8px rgba(20, 32, 46, 0.04)",
      },
      keyframes: {
        "pulse-dot": {
          "0%, 100%": { opacity: 1, transform: "scale(1)" },
          "50%": { opacity: 0.5, transform: "scale(1.3)" },
        },
      },
      animation: {
        "pulse-dot": "pulse-dot 1.6s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
