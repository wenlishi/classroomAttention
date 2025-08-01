<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>欢迎登录 - 课堂专注度分析系统</span>
        </div>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" @click="onLogin">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const onLogin = () => {
  // 这里未来会写真正的登录逻辑，比如调用 API
  // 现在我们只是简单地跳转到主控台
  console.log('登录信息:', form)
  router.push('/')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.login-card {
  width: 400px;
}
</style>
