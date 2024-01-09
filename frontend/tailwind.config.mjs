/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	plugins: [require("daisyui")],
	// https://daisyui.com/docs/colors/
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["cupcake"],
					'accent': '#f3f4f6',
					'secondary': '#e5e7eb',
					// primary: "teal",
        },
      },
			{
        dark: {
          ...require("daisyui/src/theming/themes")["dark"],
					'accent': '#374151',
					'secondary': '#4b5563',
        },
      },
    ],
  },
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
	// theme: {
	// 	extend: {},
	// },
	// plugins: [],
}
