/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
  // darkMode: 'class',
  plugins: [require("daisyui")],
  // daisyui: {
  //   themes: ["light", "dark"],
  // },
  theme: {
      extend: {
          // Remove backticks from inline code
          typography: {
              DEFAULT: {
                  css: {
                      // Fix <code> rendering
                      'code::before': {
                          content: '""'
                      },
                      'code::after': {
                          content: '""'
                      },
                      'code': {
                          "border-radius": "0.375rem",
                          "padding": "0.35em",
                          "color": "var(--tw-prose-pre-code)",
                          "background-color": "var(--tw-prose-pre-bg)",
                          "font-weight": "normal"
                      },
                  }
              }
          },
      },
  },
};
