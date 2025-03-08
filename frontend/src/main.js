import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js';

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App,{
    compilerOptions: {
      isCustomElement: tag => tag === 'nobr'
    },
  });
app.use(ElementPlus);
app.use(router);

app.mount('#app');
