<!-- plant_care_frontend/src/components/layout/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <!-- Logo -->
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-leaf me-2"></i>
        植物养护系统
      </router-link>
      
      <!-- Toggle Button -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/" exact>首页</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/plants">植物库</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/my-plants">我的植物</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/care-plans">养护计划</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/care-records">养护记录</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/growth-photos">成长相册</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/dashboard">仪表板</router-link>
          </li>
        </ul>
        
        <!-- User Menu -->
        <div class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
              <i class="bi bi-person-circle me-1"></i>
              {{ currentUser?.username || '用户' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <li>
                <router-link class="dropdown-item" to="/profile">
                  <i class="bi bi-person me-2"></i>个人资料
                </router-link>
              </li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                  <i class="bi bi-box-arrow-right me-2"></i>退出登录
                </a>
              </li>
            </ul>
          </li>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { onMounted } from 'vue'

export default {
  name: 'Navbar',
  computed: {
    ...mapGetters(['currentUser'])
  },
  methods: {
    ...mapActions(['logout', 'getUserProfile']),
    
    async handleLogout() {
      await this.logout()
      this.$router.push('/login')
      this.$toast.success('已成功退出登录')
    }
  },
  mounted() {
    // Fetch user profile if not already loaded
    if (this.$store.getters.isAuthenticated && !this.currentUser) {
      this.getUserProfile()
    }
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.25rem;
}

.nav-link {
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #e8f5e9 !important;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.dropdown-item {
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}
</style>