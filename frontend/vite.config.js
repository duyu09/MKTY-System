import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

console.log();
console.log(String.raw`██\      ██\     ██\   ██\  ████████\ ██\     ██\ `);
console.log(String.raw`███\    ███ |    ██ | ██  | \__██  __|\██\   ██  |`);
console.log(String.raw`████\  ████ |    ██ |██  /     ██ |    \██\ ██  / `);
console.log(String.raw`██\██\██ ██ |    █████  /      ██ |     \████  /  `);
console.log(String.raw`██ \███  ██ |    ██  ██<       ██ |      \██  /   `);
console.log(String.raw`██ |\█  /██ |    ██ |\██\      ██ |       ██ |    `);
console.log(String.raw`██ | \_/ ██ |██\ ██ | \██\ ██\ ██ |██\    ██ |██\ `);
console.log(String.raw`\__|     \__|\__|\__|  \__|\__|\__|\__|   \__|\__|`);
console.log();
console.log("──────────────────────────────────────────────────");
console.log("* 明康慧医(MKTY)智慧医疗系统 前端服务 *");
console.log("--------------------------------------------------");
console.log("* Minh Khoe Tue Y Smart Healthcare System Frontend Module");
console.log("* Author: DuYu <202103180009@stu.qlu.edu.cn>, Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)");
console.log("* Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)");
console.log("* Version: 1.0.0");
console.log("──────────────────────────────────────────────────");
console.log();

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: 'localhost', // 监听所有地址
    port: 8092, // 指定启动端口
    open: true // 启动后自动打开浏览器
  },
  // logger: {
  //   level: 'error', // 默认只输出错误日志
  //   customLogger: {
  //     info() {}, // 忽略 info 日志
  //     warn() {}, // 忽略 warn 日志
  //     error(msg) {
  //       console.error(msg); // 只输出 error 日志
  //     },
  //   },
  // },
  // logLevel: 'error' // 只输出错误日志
})
