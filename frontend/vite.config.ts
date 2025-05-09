import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

// https://vite.dev/config/
export default defineConfig({
    base: process.env.VITE_BASE_PATH,
    plugins: [react()],
    server: {
        port: 8080,
        proxy: { "/api": "http://localhost:8081" },
    },
})
