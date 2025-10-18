<!-- plant_care_frontend/src/views/auth/Register.vue -->
<template>
  <div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
      <div class="card mt-5">
        <div class="card-header bg-primary text-white text-center">
          <h4 class="mb-0">用户注册</h4>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleRegister">
            <!-- Error Alert -->
            <div v-if="error" class="alert alert-danger" role="alert">
              <div v-if="typeof error === 'object'">
                <div v-for="(errors, field) in error" :key="field">
                  <strong>{{ field }}:</strong>
                  <ul class="mb-0">
                    <li v-for="err in errors" :key="err">{{ err }}</li>
                  </ul>
                </div>
              </div>
              <div v-else>{{ error }}</div>
            </div>
            
            <div class="row mb-3">
              <!-- Username Field -->
              <div class="col-md-6">
                <label for="username" class="form-label">用户名</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="username" 
                  v-model="form.username" 
                  required
                  placeholder="请输入用户名"
                >
              </div>
              
              <!-- Email Field -->
              <div class="col-md-6">
                <label for="email" class="form-label">邮箱</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="form.email" 
                  required
                  placeholder="请输入邮箱"
                >
              </div>
            </div>
            
            <div class="row mb-3">
              <!-- Password Field -->
              <div class="col-md-6">
                <label for="password" class="form-label">密码</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="form.password" 
                  required
                  placeholder="请输入密码"
                >
              </div>
              
              <!-- Password Confirmation Field -->
              <div class="col-md-6">
                <label for="password2" class="form-label">确认密码</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password2" 
                  v-model="form.password2" 
                  required
                  placeholder="请再次输入密码"
                >
              </div>
            </div>
            
            <div class="row mb-3">
              <!-- First Name Field -->
              <div class="col-md-6">
                <label for="first_name" class="form-label">姓名</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="first_name" 
                  v-model="form.first_name" 
                  placeholder="请输入姓名"
                >
              </div>
              
              <!-- Phone Field -->
              <div class="col-md-6">
                <label for="phone" class="form-label">手机号</label>
                <input 
                  type="tel" 
                  class="form-control" 
                  id="phone" 
                  v-model="form.phone" 
                  placeholder="请输入手机号"
                >
              </div>
            </div>
            
            <!-- Submit Button -->
            <button 
              type="submit" 
              class="btn btn-primary w-100"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              注册
            </button>
          </form>
          
          <!-- Login Link -->
          <div class="text-center mt-3">
            <span>已有账号？</span>
            <router-link to="/login" class="text-primary">立即登录</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        password2: '',
        first_name: '',
        phone: ''
      }
    }
  },
  computed: {
    ...mapGetters(['isLoading', 'error'])
  },
  methods: {
    ...mapActions(['register']),
    
    async handleRegister() {
      try {
        await this.register(this.form)
        this.$router.push('/login')
        this.$toast.success('注册成功！请登录')
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