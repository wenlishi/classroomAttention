// 文件路径: src/composables/useToast.js

import { reactive, readonly } from 'vue';

// 1. 创建一个响应式的、私有的状态对象
const state = reactive({
  visible: false,
  message: '',
  type: 'success', // 'success' 或 'error'
  timeoutId: null,
});

// 2. 创建一个 showToast 函数来控制状态
function showToast(message, type = 'success', duration = 2500) {
  // 如果当前有通知正在显示，先清除它
  if (state.timeoutId) {
    clearTimeout(state.timeoutId);
  }

  state.message = message;
  state.type = type;
  state.visible = true;

  // 设置定时器，在指定时间后自动隐藏
  state.timeoutId = setTimeout(() => {
    state.visible = false;
  }, duration);
}

// 3. 导出一个 useToast "组合式函数"
export function useToast() {
  return {
    // 只暴露状态的只读版本，防止外部组件意外修改
    toastState: readonly(state),
    // 暴露控制函数
    showToast,
  };
}
