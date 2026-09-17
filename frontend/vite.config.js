import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    // 后端 CORS 只放行了 5173，端口被占用时直接报错而不是换端口
    port: 5173,
    strictPort: true,
  },
})
