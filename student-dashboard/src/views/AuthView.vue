<template>
  <!-- [已移除] Toast 通知的 HTML 已经移动到 ToastNotification.vue 组件中 -->
  <div class="auth-container">
    <div class="auth-wrapper">
      <!-- Left Panel -->
      <div class="left-panel">
        <img
          src="@/assets/student-illustration.png"
          alt="Classroom Image"
          class="left-panel-img"
        />
        <!-- Overlay -->
        <div class="left-panel-overlay">
          <div class="overlay-content">
            <h2 class="overlay-title">教室智能布局系统</h2>
            <p class="overlay-subtitle">精准、高效、智能地管理您的教室资源。</p>
          </div>
        </div>
      </div>

      <!-- Right Panel -->
      <div class="right-panel">
        <!-- Login Form -->
        <div v-if="isLoginView" class="form-container">
          <h1 class="form-title">欢迎回来</h1>
          <p class="form-subtitle">请登录您的账户</p>

          <form @submit.prevent="handleLogin">
            <div v-if="loginError" class="error-message">
              {{ loginError }}
            </div>
            <div class="input-group">
              <label for="login-username" class="input-label">用户名</label>
              <input
                v-model="loginData.username"
                type="text"
                id="login-username"
                placeholder="请输入您的用户名"
                class="input-field"
                required
              />
            </div>
            <div class="input-group relative">
              <label for="login-password" class="input-label">密码</label>
              <input
                v-model="loginData.password"
                :type="loginPasswordVisible ? 'text' : 'password'"
                id="login-password"
                placeholder="请输入您的密码"
                class="input-field"
                required
              />
              <button type="button" class="password-toggle-btn" @click="loginPasswordVisible = !loginPasswordVisible">
                <svg v-if="!loginPasswordVisible" xmlns="http://www.w3.org/2000/svg" class="eye-icon" viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z" /><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.022 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" /></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="eye-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.97 9.97 0 01-1.563 3.029m0 0l-2.175 2.175m-5.358-5.358l-3.29-3.29" /></svg>
              </button>
            </div>
            <div class="form-actions">
              <a href="#" class="forgot-password-link">忘记密码?</a>
            </div>
            <button type="submit" class="submit-btn" :disabled="isLoading">
              {{ isLoading ? '正在登录...' : '登 录' }}
            </button>
          </form>
          <p class="switch-form-text">
            还没有账户? <a href="#" @click.prevent="isLoginView = false" class="switch-form-link">立即注册</a>
          </p>
        </div>

        <!-- Register Form -->
        <div v-else class="form-container">
          <h1 class="form-title">创建您的账户</h1>
          <p class="form-subtitle">只需几步，即可开始使用</p>

          <form @submit.prevent="handleRegister">
            <div v-if="registerError" class="error-message">
              {{ registerError }}
            </div>
            <div class="input-group">
              <label for="register-username" class="input-label">用户名</label>
              <input
                v-model="registerData.username"
                type="text"
                id="register-username"
                placeholder="设置您的用户名"
                class="input-field"
                required
              />
            </div>
            <div class="input-group">
              <label for="register-email" class="input-label">邮箱地址</label>
              <input
                v-model="registerData.email"
                type="email"
                id="register-email"
                placeholder="请输入您的邮箱"
                class="input-field"
                required
              />
            </div>
            <div class="input-group relative">
              <label for="register-password" class="input-label">设置密码</label>
              <input
                v-model="registerData.password"
                :type="registerPasswordVisible ? 'text' : 'password'"
                id="register-password"
                placeholder="请输入您的密码"
                class="input-field"
                required
              />
              <button type="button" class="password-toggle-btn" @click="registerPasswordVisible = !registerPasswordVisible">
                <svg v-if="!registerPasswordVisible" xmlns="http://www.w3.org/2000/svg" class="eye-icon" viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z" /><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.022 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" /></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="eye-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.97 9.97 0 01-1.563 3.029m0 0l-2.175 2.175m-5.358-5.358l-3.29-3.29" /></svg>
              </button>
            </div>
            <div class="input-group">
              <label for="confirm-password" class="input-label">确认密码</label>
              <input
                v-model="registerData.confirmPassword"
                type="password"
                id="confirm-password"
                placeholder="请再次输入您的密码"
                class="input-field"
                required
              />
            </div>
            <button type="submit" class="submit-btn" :disabled="isRegistering">
              {{ isRegistering ? '正在注册...' : '注 册' }}
            </button>
          </form>
          <p class="switch-form-text">
            已经有账户了? <a href="#" @click.prevent="isLoginView = true" class="switch-form-link">返回登录</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { authState } from '../auth'; 
// [核心修改] 1. 导入我们创建的 useToast 组合式函数
import { useToast } from '../composables/useToast';

// --- State Management ---
const isLoginView = ref(true);
const isLoading = ref(false);
const loginError = ref('');
const isRegistering = ref(false);
const registerError = ref('');

const router = useRouter();
// [核心修改] 2. 获取 showToast 函数
const { showToast } = useToast();

// --- Login Form State ---
const loginData = reactive({ username: '', password: '' });
const loginPasswordVisible = ref(false);

// --- Register Form State ---
const registerData = reactive({ username: '', email: '', password: '', confirmPassword: '' });
const registerPasswordVisible = ref(false);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

// --- Form Submission Handlers ---
const handleLogin = async () => {
  isLoading.value = true;
  loginError.value = '';

  const formData = new URLSearchParams();
  formData.append('username', loginData.username);
  formData.append('password', loginData.password);

  try {
    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || '登录失败，请检查您的凭据。');
    }

    // [核心修改] 3. 使用新的全局 showToast 函数
    showToast('登录成功!');
    
    authState.isLoggedIn = true;

    setTimeout(() => {
      router.push('/home');
    }, 1000); 

  } catch (error) {
    loginError.value = error.message;
    // [核心修改] 4. 在出错时显示错误类型的 Toast
    showToast(error.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const handleRegister = async () => {
  if (registerData.password !== registerData.confirmPassword) {
    const msg = '两次输入的密码不匹配！';
    registerError.value = msg;
    showToast(msg, 'error'); // 显示错误通知
    return;
  }

  isRegistering.value = true;
  registerError.value = '';

  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: registerData.username,
        email: registerData.email,
        password: registerData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || '注册失败，请稍后重试。');
    }

    showToast('注册成功！现在可以用新账户登录了。');
    
    isLoginView.value = true;
    loginData.username = registerData.username;
    loginData.password = '';

  } catch (error) {
    registerError.value = error.message;
    showToast(error.message, 'error'); // 显示错误通知
  } finally {
    isRegistering.value = false;
  }
};
</script>

<style scoped>
/* [已移除] Toast 通知的 CSS 已经移动到 ToastNotification.vue */

/* General Styles */
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f1f5f9; /* slate-100 */
  font-family: 'Inter', system-ui, sans-serif;
}

.auth-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  margin: 1.5rem;
  background-color: white;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border-radius: 1rem;
  width: 90%;
  max-width: 1024px;
}

@media (min-width: 768px) {
  .auth-wrapper {
    flex-direction: row;
  }
}

.error-message {
  background-color: #fee2e2; /* red-100 */
  color: #b91c1c; /* red-700 */
  padding: 0.75rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  text-align: center;
}

/* Left Panel */
.left-panel {
  position: relative;
}
@media (min-width: 768px) {
  .left-panel {
    width: 50%;
  }
}

.left-panel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}
@media (min-width: 768px) {
  .left-panel-img {
    display: block;
    border-top-right-radius: 0;
    border-bottom-left-radius: 1rem;
  }
}
@media (max-width: 767px) {
    .left-panel {
        display: none;
    }
}

.left-panel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(30, 58, 138, 0.5); /* blue-900 with 50% opacity */
  border-top-left-radius: 1rem;
}
@media (min-width: 768px) {
  .left-panel-overlay {
    display: block;
    border-bottom-left-radius: 1rem;
  }
}

.overlay-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  padding: 2rem;
  text-align: center;
}

.overlay-title {
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.overlay-subtitle {
  font-size: 1.125rem;
}

/* Right Panel */
.right-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem;
}
@media (min-width: 768px) {
  .right-panel {
    width: 50%;
    padding: 3.5rem;
  }
}

.form-container {
  width: 100%;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b; /* slate-800 */
  margin-bottom: 0.75rem;
}

.form-subtitle {
  color: #64748b; /* slate-500 */
  margin-bottom: 2rem;
}

.input-group {
  margin-bottom: 1.25rem; 
}
.input-group.relative {
  position: relative;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569; /* slate-600 */
  margin-bottom: 0.5rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #cbd5e1; /* slate-300 */
  border-radius: 0.375rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease-in-out;
  height: 44px;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6; /* blue-500 */
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.password-toggle-btn {
    position: absolute;
    bottom: 0;
    right: 0;
    height: 44px;
    display: flex;
    align-items: center;
    padding: 0 1rem;
    color: #64748b; /* slate-500 */
    background: transparent;
    border: none;
    cursor: pointer;
}

.eye-icon {
    height: 1.25rem;
    width: 1.25rem;
}


.form-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.forgot-password-link {
  font-size: 0.875rem;
  color: #2563eb; /* blue-600 */
  text-decoration: none;
}
.forgot-password-link:hover {
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  background-color: #2563eb; /* blue-600 */
  color: white;
  padding: 0.75rem;
  border-radius: 0.375rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}
.submit-btn:hover {
  background-color: #1d4ed8; /* blue-700 */
}
.submit-btn:disabled {
  background-color: #94a3b8; /* slate-400 */
  cursor: not-allowed;
}

.switch-form-text {
  text-align: center;
  font-size: 0.875rem;
  color: #64748b; /* slate-500 */
  margin-top: 2rem;
}

.switch-form-link {
  font-weight: 500;
  color: #2563eb; /* blue-600 */
  text-decoration: none;
}
.switch-form-link:hover {
  text-decoration: underline;
}
</style>
