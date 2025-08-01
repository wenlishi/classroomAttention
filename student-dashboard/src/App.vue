<script setup>
import { RouterView } from 'vue-router'
import ToastNotification from './components/ToastNotification.vue';
</script>

<template>
  <!-- 
    这里是整个应用的根节点。
    Vue Router会根据当前URL，将匹配到的组件渲染到 <RouterView /> 中。
    它本身不应该包含任何具体页面的内容。
  -->
  <ToastNotification />
  <RouterView />
</template>

<style>
  /* 
    建议删除所有 scoped 样式，或者保留一些你想全局应用的样式。
    例如，重置 body 的 margin 和 padding。
  */
  body {
    margin: 0;
    padding: 0;
  }
</style>
