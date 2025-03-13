import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js';

import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'

const app = createApp(App,{
    compilerOptions: {
      isCustomElement: tag => tag === 'nobr'
    },
  });
app.use(ElementPlus);
app.use(router);
app.use(ElementPlus, {
  locale: zhCn,  // 组件语言设为中文
})

app.mount('#app');
