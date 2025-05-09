import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import store from './store'

// 忽略 ResizeObserver 警告
const debounce = (fn, delay) => {
  let timeoutId
  return (...args) => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }
    timeoutId = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

const handleResizeObserverError = debounce(() => {
  const resizeObserverError = 'ResizeObserver loop completed with undelivered notifications.'
  const originalConsoleError = console.error
  console.error = (...args) => {
    if (args[0] === resizeObserverError) {
      return
    }
    originalConsoleError.apply(console, args)
  }
}, 100)

window.addEventListener('error', (event) => {
  if (event.message === 'ResizeObserver loop completed with undelivered notifications.') {
    event.stopImmediatePropagation()
    handleResizeObserverError()
  }
})

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.use(store)
app.mount('#app') 