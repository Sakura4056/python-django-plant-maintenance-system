<!-- plant_care_frontend/src/views/auth/Login.vue -->
<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card mt-5">
        <div class="card-header bg-primary text-white text-center">
          <h4 class="mb-0">登录系统</h4>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleLogin">
            <!-- Error Alert -->
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <!-- Username Field -->
            <div class="mb-3">
              <label for="username" class="form-label">用户名</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="username" 
                required
                placeholder="请输入用户名"
              >
            </div>
            
            <!-- Password Field -->
            <div class="mb-3">
              <label for="password" class="form-label">密码</label>
              <input 
                type="password" 
                class="form-control" 
                id="password" 
                v-model="password" 
                required
                placeholder="请输入密码"
              >
            </div>
            
            <!-- Submit Button -->
            <button 
              type="submit" 
              class="btn btn-primary w-100"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              登录
            </button>
          </form>
          
          <!-- Register Link -->
          <div class="text-center mt-3">
            <span>还没有账号？</span>
            <router-link to="/register" class="text-primary">立即注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  computed: {
    ...mapGetters(['isLoading', 'error'])
  },
  methods: {
    ...mapActions(['login']),
    
    async handleLogin() {
      try {
        await this.login({ username: this.username, password: this.password })
        this.$router.push('/dashboard')
        this.$toast.success('登录成功！')
      } catch (error) {
        // Error is already handled by Vuex
      }
    }
  },
  mounted() {
    // Redirect if already authenticated
    if (this.$store.getters.isAuthenticated) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
}
</style>