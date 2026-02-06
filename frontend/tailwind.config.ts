import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                },
                mole: {
                    dark: '#1a1a2e',
                    darker: '#0f0f1a',
                    accent: '#e94560',
                    gold: '#ffd700',
                    success: '#00ff88',
                }
            },
            animation: {
                'typewriter': 'typewriter 2s steps(40) forwards',
                'blink': 'blink 1s infinite',
                'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
                'slide-up': 'slide-up 0.5s ease-out',
                'fade-in': 'fade-in 0.3s ease-out',
            },
            keyframes: {
                typewriter: {
                    'from': { width: '0' },
                    'to': { width: '100%' }
                },
                blink: {
                    '0%, 50%': { opacity: '1' },
                    '51%, 100%': { opacity: '0' }
                },
                'pulse-glow': {
                    '0%, 100%': { boxShadow: '0 0 5px rgba(233, 69, 96, 0.5)' },
                    '50%': { boxShadow: '0 0 20px rgba(233, 69, 96, 0.8)' }
                },
                'slide-up': {
                    'from': { transform: 'translateY(20px)', opacity: '0' },
                    'to': { transform: 'translateY(0)', opacity: '1' }
                },
                'fade-in': {
                    'from': { opacity: '0' },
                    'to': { opacity: '1' }
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
};

export default config;
