/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Based on activism.wtf and We The Free branding
        'navy': {
          900: '#0A0E27',
          800: '#151933',
          700: '#1E2440',
          600: '#272F4D',
        },
        'magenta': {
          500: '#FF1B8D',
          600: '#E6187E',
          700: '#CC156F',
          400: '#FF4DA6',
        },
        'accent': {
          blue: '#4A90E2',
          green: '#4CAF50',
          yellow: '#FFC107',
          red: '#F44336',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Space Grotesk', 'Inter', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
