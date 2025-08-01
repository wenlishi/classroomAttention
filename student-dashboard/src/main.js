import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

// [新增] 1. 导入我们的初始化函数
import { initializeAuth } from './auth'

// [新增] 2. 创建一个异步函数来启动应用
async function startApp() {
  // [核心修改] 3. 首先执行并等待身份验证完成
  await initializeAuth();

  // 4. 验证完成后，再创建和挂载Vue应用
  const app = createApp(App)
  app.use(router)
  app.use(ElementPlus)

  app.use(createPinia())

  app.mount('#app')
}

// 5. 调用启动函数
startApp();

