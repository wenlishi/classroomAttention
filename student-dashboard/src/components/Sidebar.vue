<template>
  <!-- 这是独立的侧边栏组件 -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <span class="logo-icon">🎓</span>
      <h1 class="sidebar-title">智慧课堂</h1>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/home" class="nav-item">
        <span class="nav-icon">📊</span>
        <span>实时仪表盘</span>
      </router-link>
      <router-link to="/layouts" class="nav-item">
        <span class="nav-icon">🏫</span>
        <span>教室布局</span>
      </router-link>
      <router-link to="/alerts" class="nav-item">
        <span class="nav-icon">🔔</span>
        <span>告警中心</span>
      </router-link>
      <router-link to="/settings" class="nav-item">
        <span class="nav-icon">⚙️</span>
        <span>系统设置</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
// 这个组件目前没有自己的逻辑，所以 script 部分很简单
</script>

<style scoped>
/* 侧边栏 */
.sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  /* 添加一个 flex-shrink: 0 来防止侧边栏在 flex 布局中被压缩 */
  flex-shrink: 0;
}

.sidebar-header {
  display: flex;
  align-items: center;
  margin-bottom: 2.5rem;
}

.logo-icon {
  font-size: 2rem;
  margin-right: 0.75rem;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #343a40;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  text-decoration: none;
  color: #495057;
  font-weight: 500;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-item:hover {
  background-color: #f1f3f5;
}

/* 使用 Vue Router 的 active class 来实现高亮 */
.nav-item.router-link-exact-active {
  background-color: #4c6ef5;
  color: white;
}

.nav-icon {
  margin-right: 1rem;
  font-size: 1.2rem;
}
</style>
