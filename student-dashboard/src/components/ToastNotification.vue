<template>
  <!-- 当 toastState.visible 为 true 时，显示通知 -->
  <div v-if="toastState.visible" :class="['toast-notification', toastState.type]">
    <span class="toast-icon">{{ toastState.type === 'success' ? '✅' : '❌' }}</span>
    <p>{{ toastState.message }}</p>
  </div>
</template>

<script setup>
// 导入并使用我们的组合式函数来获取状态
import { useToast } from '../composables/useToast';

const { toastState } = useToast();
</script>

<style scoped>
.toast-notification {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 9999;
  animation: slide-in-out 2.8s cubic-bezier(0.68, -0.55, 0.27, 1.55) forwards;
}

/* 根据不同的类型（success/error）显示不同的背景色 */
.toast-notification.success {
  background-color: #2c3e50; /* 深蓝灰色 */
}

.toast-notification.error {
  background-color: #c0392b; /* 红色 */
}

.toast-icon {
  font-size: 1.25rem;
}

@keyframes slide-in-out {
  0% {
    transform: translate(-50%, -100px);
    opacity: 0;
  }
  15%, 85% {
    transform: translate(-50%, 0);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -100px);
    opacity: 0;
  }
}
</style>
