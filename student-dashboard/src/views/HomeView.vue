<template>
  <div class="home-container">
    <!-- [核心修改] 使用我们新创建的 Sidebar 组件 -->
    <Sidebar />

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 主内容区头部 -->
      <header class="main-header">
        <div>
          <h2 class="header-title">C101 教室 - 实时仪表盘</h2>
          <p class="header-subtitle">上午 10:24, 周二, 7月26日</p>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-label">平均专注度</span>
            <span class="stat-value green">85%</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">需关注人数</span>
            <span class="stat-value orange">2</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总人数</span>
            <span class="stat-value">50</span>
          </div>
        </div>
      </header>

      <!-- 仪表盘网格布局 -->
      <div class="dashboard-grid">
        <!-- 实时监控卡片 -->
        <div class="card large-card">
          <h3 class="card-title">■ 实时监控</h3>
          <div class="monitoring-placeholder">
            <p>实时视频监控区域</p>
          </div>
        </div>

        <!-- 专注度热力图卡片 -->
        <div class="card">
          <h3 class="card-title">💧 专注度热力图</h3>
          <div class="heatmap-placeholder">
            <div class="blur-circle green-blur"></div>
            <div class="blur-circle yellow-blur"></div>
            <div class="blur-circle red-blur"></div>
          </div>
        </div>
      </div>

      <!-- 学生详情卡片 -->
      <div class="card student-details-card">
        <h3 class="card-title">👥 学生专注度详情</h3>
        <table class="student-table">
          <thead>
            <tr>
              <th>学生</th>
              <th>状态/预计</th>
              <th>专注度</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="student-info">
                  <img src="https://i.pravatar.cc/40?u=a042581f4e29026704d" alt="avatar" class="avatar">
                  <span>王强</span>
                </div>
              </td>
              <td>正常听讲，与PPT互动</td>
              <td class="green">高</td>
              <td><a href="#" class="action-link">查看</a></td>
            </tr>
            <tr>
              <td>
                <div class="student-info">
                  <img src="https://i.pravatar.cc/40?u=a042581f4e29026705d" alt="avatar" class="avatar">
                  <span>李静</span>
                </div>
              </td>
              <td class="orange">频繁低头，疑似走神</td>
              <td class="orange">中</td>
              <td><a href="#" class="action-link">查看</a></td>
            </tr>
            <tr>
              <td>
                <div class="student-info">
                  <img src="https://i.pravatar.cc/40?u=a042581f4e29026706d" alt="avatar" class="avatar">
                  <span>赵磊</span>
                </div>
              </td>
              <td>与邻座同学交谈</td>
              <td class="red">低</td>
              <td><a href="#" class="action-link">查看</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
// [核心修改] 1. 导入新创建的 Sidebar 组件
// 请确保路径正确，例如 '../components/Sidebar.vue'
import Sidebar from '../components/Sidebar.vue';

// 这是一个用于布局演示的静态组件。
// 您可以根据需要在此处添加响应式数据和方法。
</script>

<style scoped>
/* 主布局 */
.home-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Inter', system-ui, sans-serif;
}

/* [已移除] 所有 sidebar 相关的样式都已移动到 Sidebar.vue 文件中 */

/* 主内容区 */
.main-content {
  flex: 1;
  padding: 2rem 2.5rem;
  overflow-y: auto;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.header-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #212529;
}

.header-subtitle {
  color: #868e96;
  margin-top: 0.25rem;
}

.header-stats {
  display: flex;
  gap: 2rem;
  background-color: #ffffff;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  color: #868e96;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #343a40;
}

.stat-value.green { color: #28a745; }
.stat-value.orange { color: #fd7e14; }

/* 仪表盘网格 */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.card {
  background-color: #ffffff;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #343a40;
  margin-bottom: 1rem;
}

.large-card {
  height: 350px;
}

.monitoring-placeholder {
  width: 100%;
  height: calc(100% - 40px);
  background-color: #f1f3f5;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #adb5bd;
}

.heatmap-placeholder {
  position: relative;
  width: 100%;
  height: calc(100% - 40px);
  border-radius: 0.5rem;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.blur-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
}

.green-blur {
  width: 150px;
  height: 150px;
  background-color: rgba(40, 167, 69, 0.4);
  top: 10%;
  left: 15%;
}
.yellow-blur {
  width: 120px;
  height: 120px;
  background-color: rgba(255, 193, 7, 0.4);
  bottom: 15%;
  right: 20%;
}
.red-blur {
  width: 100px;
  height: 100px;
  background-color: rgba(220, 53, 69, 0.3);
  bottom: 30%;
  left: 30%;
}

/* 学生详情 */
.student-table {
  width: 100%;
  border-collapse: collapse;
}

.student-table th, .student-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f1f3f5;
}

.student-table th {
  color: #868e96;
  font-weight: 500;
  font-size: 0.875rem;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.action-link {
  color: #4c6ef5;
  text-decoration: none;
  font-weight: 500;
}
.action-link:hover {
  text-decoration: underline;
}

.green { color: #28a745; }
.orange { color: #fd7e14; }
.red { color: #dc3545; }

</style>
