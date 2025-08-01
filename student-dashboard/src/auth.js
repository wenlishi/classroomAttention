// 文件路径: src/auth.js

import { reactive } from 'vue';

export const authState = reactive({
  // [新增] 添加一个状态来跟踪初始化检查是否完成
  isInitialized: false,
  isLoggedIn: false,
});

// 从环境变量读取 API 基础 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * 此函数用于在应用首次加载或页面刷新时，
 * 通过调用后端接口来验证用户的登录状态。
 */
export async function initializeAuth() {
  // 防止重复初始化
  if (authState.isInitialized) {
    return;
  }

  try {
    // [核心修改] 不再读取 document.cookie，而是发起一个API请求
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // credentials: 'include' 确保浏览器会自动发送 HttpOnly cookie
      credentials: 'include',
    });

    if (response.ok) {
      // 如果请求成功 (状态码 2xx)，说明 cookie 有效，用户已登录
      const user = await response.json();
      console.log('认证成功，当前用户:', user.username);
      authState.isLoggedIn = true;
    } else {
      // 如果请求失败 (例如 401 Unauthorized)，说明用户未登录
      console.log('认证失败，用户未登录。');
      authState.isLoggedIn = false;
    }
  } catch (error) {
    // 网络错误等情况，也视为未登录
    console.error('初始化认证状态时发生网络错误:', error);
    authState.isLoggedIn = false;
  } finally {
    // 标记初始化已完成，这样路由守卫就可以开始工作了
    authState.isInitialized = true;
  }
}
