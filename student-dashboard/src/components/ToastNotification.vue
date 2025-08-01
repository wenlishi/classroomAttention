<template>
  <!-- 当 toastState.visible 为 true 时，显示通知 -->
  <div v-if="toastState.visible" :class="['toast-notification', toastState.type]">
    <span class="toast-icon">{{ toastState.type === 'success' ? '✅' : '❌' }}</span>
    <p>{{ toastState.message }}</p>
  </div>
</template>

<script setup>
// 导入并使用我们的组合式函数来获取状态
// 请确保您的项目路径是正确的
import { useToast } from '../composables/useToast';

const { toastState } = useToast();
</script>

<style scoped>
/* 通知组件的基础样式
*/
.toast-notification {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  /* 使用更柔和的阴影效果 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 9999;
  /* 应用进入和离开的动画 */
  animation: slide-in-out 2.8s cubic-bezier(0.68, -0.55, 0.27, 1.55) forwards;
}

/* 成功状态的样式 (浅绿色)
*/
.toast-notification.success {
  background-color: #d4edda; /* 浅绿色背景 */
  color: #155724; /* 深绿色文字，保证可读性 */
}

/* 错误状态的样式 (浅粉色)
*/
.toast-notification.error {
  background-color: #f8d7da; /* 浅粉色背景 */
  color: #721c24; /* 深红色文字，保证可读性 */
}

.toast-icon {
  font-size: 1.25rem;
}

/* 定义滑入和滑出的动画效果
*/
@keyframes slide-in-out {
  0% {
    transform: translate(-50%, -100px);
    opacity: 0;
  }
  /* 动画的 15% 到 85% 阶段，通知会停留在屏幕上 */
  15%, 85% {
    transform: translate(-50%, 20px); /* 让通知稍微向下移动一点，视觉效果更好 */
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -100px);
    opacity: 0;
  }
}
</style>
