import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
// [新增] 1. 从 auth.js 文件中导入全局状态
import { authState } from '../auth'; // 请确保路径正确
import LayoutsView from '@/views/LayoutsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      // 标记这个页面需要登录认证
      meta: { requiresAuth: true } 
    },
    {
      // 当用户访问根路径时，重定向到主页
      path: '/',
      redirect: '/home'
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView,
      // 标记这个页面只允许未登录的“访客”访问
      meta: { requiresGuest: true }
    },
    {
      path: '/layouts',
      name: 'layouts',
      component: LayoutsView,
      // 标记这个页面只允许未登录的“访客”访问
      meta: { requiresAuth: true }
    },
    // ... 您其他的路由定义
  ],
})

// --- [核心修改] 全局前置导航守卫 ---
router.beforeEach((to, from, next) => {
  // 守卫现在直接检查我们可靠的全局状态 authState.isLoggedIn
  // 因为 main.js 会确保在路由开始前，这个状态就已经通过 API 验证完毕
  if (to.meta.requiresAuth && !authState.isLoggedIn) {
    // 如果目标页面需要登录，但我们的状态显示为“未登录”，则跳转
    console.log('路由守卫：需要登录，但状态为未登录，跳转到 /auth');
    next('/auth');
  } else if (to.meta.requiresGuest && authState.isLoggedIn) {
    // 如果目标页面是访客专用（如登录页），但我们的状态显示为“已登录”，则跳转
    console.log('路由守卫：状态为已登录，访问访客页面，跳转到 /home');
    next('/home');
  } else {
    // 其他所有情况，正常放行
    next();
  }
});

export default router
