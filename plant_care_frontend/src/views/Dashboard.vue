<!-- plant_care_frontend/src/views/Dashboard.vue -->
<template>
  <div class="dashboard">
    <h1 class="mb-4">植物养护仪表板</h1>
    
    <!-- Stats Cards -->
    <div class="row row-cols-1 md:row-cols-2 lg:row-cols-5 gap-4 mb-6">
      <div class="card bg-primary text-white">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title">我的植物</h5>
              <p class="card-text display-4">{{ dashboard.total_plants }}</p>
            </div>
            <i class="bi bi-leaf text-3xl"></i>
          </div>
        </div>
      </div>
      
      <div class="card bg-success text-white">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title">健康植物</h5>
              <p class="card-text display-4">{{ dashboard.healthy_plants }}</p>
            </div>
            <i class="bi bi-heart text-3xl"></i>
          </div>
        </div>
      </div>
      
      <div class="card bg-warning text-white">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title">需关注</h5>
              <p class="card-text display-4">{{ dashboard.warning_plants }}</p>
            </div>
            <i class="bi bi-exclamation-triangle text-3xl"></i>
          </div>
        </div>
      </div>
      
      <div class="card bg-info text-white">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title">今日任务</h5>
              <p class="card-text display-4">{{ dashboard.today_tasks }}</p>
            </div>
            <i class="bi bi-calendar-check text-3xl"></i>
          </div>
        </div>
      </div>
      
      <div class="card bg-secondary text-white">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="card-title">本周任务</h5>
              <p class="card-text display-4">{{ dashboard.upcoming_tasks }}</p>
            </div>
            <i class="bi bi-calendar-week text-3xl"></i>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Activities -->
    <div class="row row-cols-1 lg:row-cols-2 gap-6">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">最近养护记录</h5>
        </div>
        <div class="card-body">
          <div v-if="dashboard.recent_records && dashboard.recent_records.length > 0">
            <div v-for="record in dashboard.recent_records" :key="record.id" class="mb-3">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ record.my_plant_name }}</strong>
                  <span class="text-muted ms-2">{{ record.record_type_display }}</span>
                </div>
                <small class="text-muted">{{ formatDate(record.record_time) }}</small>
              </div>
              <p class="text-sm text-muted">{{ record.description }}</p>
            </div>
          </div>
          <div v-else class="text-center text-muted">
            暂无养护记录
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">快速操作</h5>
        </div>
        <div class="card-body">
          <div class="d-grid gap-3">
            <router-link to="/my-plants/add" class="btn btn-success">
              <i class="bi bi-plus-circle me-2"></i>添加新植物
            </router-link>
            <router-link to="/care-records" class="btn btn-primary">
              <i class="bi bi-journal-plus me-2"></i>记录养护操作
            </router-link>
            <router-link to="/growth-photos" class="btn btn-info">
              <i class="bi bi-camera me-2"></i>上传成长照片
            </router-link>
            <router-link to="/plants" class="btn btn-secondary">
              <i class="bi bi-search me-2"></i>浏览植物库
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { onMounted } from 'vue'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters(['dashboard'])
  },
  methods: {
    ...mapActions(['fetchDashboard']),
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    }
  },
  mounted() {
    this.fetchDashboard()
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
</style>