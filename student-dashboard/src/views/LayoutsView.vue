<template>
  <div class="layout-page-container">
    <!-- 1. 在这里复用您创建的侧边栏组件 -->
    <Sidebar />

    <!-- 2. 这是教室布局页面的主内容区域 -->
    <main class="main-content">
      <header class="page-header">
        <h2>教室布局</h2>
        <p>在这里管理和查看所有教室的座位安排和布局。</p>
      </header>
      
      <!-- 3. 内容占位符，您可以在这里添加具体的功能 -->
      <div class="content-placeholder">
        <div class="placeholder-text">
          <p>教室布局内容区域</p>
          <span>未来可以在这里添加具体的布局图、列表、筛选器等功能。</span>
        </div>

        <!-- 示例卡片，展示如何列出教室 -->
        <div class="layout-card">
          <div class="card-info">
            <h3>高三（1）班</h3>
            <span>座位数: 50 / 50</span>
          </div>
          <button class="btn-primary">查看详情</button>
        </div>
        <div class="layout-card">
          <div class="card-info">
            <h3>高二（3）班</h3>
            <span>座位数: 48 / 50</span>
          </div>
          <button class="btn-secondary">编辑布局</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// 导入侧边栏组件
// 请确保路径相对于当前文件是正确的，这里假设 Sidebar.vue 在 '../components/' 目录下
import Sidebar from '../components/Sidebar.vue'; 
</script>

<style scoped>
/* 整个页面的容器，使用 flex 布局让侧边栏和主内容并排显示 */
.layout-page-container {
  display: flex;
  height: 100vh; /* 让页面撑满整个视口高度 */
  background-color: #f8f9fa; /* 设置一个浅灰色背景 */
}

/* 主内容区域 */
.main-content {
  flex-grow: 1; /* 让主内容区域占据剩余的所有空间 */
  padding: 2.5rem;
  overflow-y: auto; /* 如果内容超出一页，允许垂直滚动 */
}

.page-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #343a40;
}

.page-header p {
  color: #6c757d;
  font-size: 1rem;
  margin-top: 0.25rem;
}

.content-placeholder {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.placeholder-text {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
  border: 2px dashed #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.layout-card {
  border: 1px solid #e9ecef;
  background-color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow 0.2s ease;
}

.layout-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.card-info h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #495057;
}
.card-info span {
  font-size: 0.9rem;
  color: #6c757d;
}

/* 按钮样式 */
button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary {
  background-color: #4c6ef5;
  color: white;
}
.btn-primary:hover {
  background-color: #3b5bdb;
}

.btn-secondary {
  background-color: #f1f3f5;
  color: #495057;
  border: 1px solid #dee2e6;
}
.btn-secondary:hover {
  background-color: #e9ecef;
}

</style>
