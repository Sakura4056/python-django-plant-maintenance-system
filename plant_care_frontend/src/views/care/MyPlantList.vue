<!-- plant_care_frontend/src/views/care/MyPlantList.vue -->
<template>
  <div class="my-plants">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>我的植物</h1>
      <router-link to="/my-plants/add" class="btn btn-primary">
        <i class="bi bi-plus-circle me-2"></i>添加植物
      </router-link>
    </div>
    
    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row row-cols-1 md:row-cols-3 gap-3">
          <div>
            <label class="form-label">植物状态</label>
            <select v-model="filters.status" class="form-select" @change="fetchMyPlants">
              <option value="">全部状态</option>
              <option value="healthy">健康</option>
              <option value="warning">需关注</option>
              <option value="unhealthy">不健康</option>
              <option value="dormant">休眠期</option>
            </select>
          </div>
          <div>
            <label class="form-label">植物位置</label>
            <input v-model="filters.location" type="text" class="form-control" placeholder="搜索位置">
          </div>
          <div>
            <label class="form-label">搜索</label>
            <div class="input-group">
              <input v-model="filters.search" type="text" class="form-control" placeholder="搜索植物名称">
              <button class="btn btn-outline-secondary" type="button" @click="fetchMyPlants">
                <i class="bi bi-search"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Plant Grid -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="myPlants.length === 0" class="text-center py-5">
      <div class="alert alert-info" role="alert">
        <i class="bi bi-info-circle me-2"></i>
        您还没有添加任何植物，点击"添加植物"开始您的植物养护之旅！
      </div>
    </div>
    
    <div v-else class="row row-cols-1 md:row-cols-2 lg:row-cols-3 xl:row-cols-4 gap-4">
      <div v-for="plant in myPlants" :key="plant.id" class="card h-100">
        <div class="position-relative">
          <img :src="plant.plant.image || 'https://via.placeholder.com/300x200?text=No+Image'" 
               class="card-img-top" alt="Plant Image" style="height: 200px; object-fit: cover;">
          <span :class="getStatusBadgeClass(plant.status)" class="position-absolute top-2 right-2">
            {{ getStatusText(plant.status) }}
          </span>
        </div>
        <div class="card-body">
          <h5 class="card-title">{{ plant.nickname }}</h5>
          <p class="card-text text-muted">{{ plant.plant_name }}</p>
          <div class="text-sm">
            <div class="mb-1">
              <i class="bi bi-geo-alt me-1"></i>
              {{ plant.location || '未设置位置' }}
            </div>
            <div class="mb-1">
              <i class="bi bi-calendar-plus me-1"></i>
              {{ formatDate(plant.purchase_date) || '未设置购买日期' }}
            </div>
          </div>
        </div>
        <div class="card-footer bg-transparent">
          <div class="d-grid gap-2">
            <router-link :to="'/my-plants/' + plant.id" class="btn btn-outline-primary btn-sm">
              查看详情
            </router-link>
            <button @click="generateCarePlan(plant.id)" class="btn btn-outline-success btn-sm">
              生成养护计划
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { onMounted, reactive } from 'vue'

export default {
  name: 'MyPlantList',
  setup() {
    const filters = reactive({
      status: '',
      location: '',
      search: ''
    })
    
    return {
      filters
    }
  },
  computed: {
    ...mapGetters('myPlants', ['allMyPlants', 'isLoading']),
    myPlants() {
      return this.allMyPlants || []
    }
  },
  methods: {
    ...mapActions('myPlants', ['fetchMyPlants', 'generateCarePlan']),
    
    getStatusBadgeClass(status) {
      const classes = {
        'healthy': 'badge bg-success',
        'warning': 'badge bg-warning',
        'unhealthy': 'badge bg-danger',
        'dormant': 'badge bg-secondary'
      }
      return classes[status] || 'badge bg-light text-dark'
    },
    
    getStatusText(status) {
      const texts = {
        'healthy': '健康',
        'warning': '需关注',
        'unhealthy': '不健康',
        'dormant': '休眠期'
      }
      return texts[status] || status
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
  },
  mounted() {
    this.fetchMyPlants()
  }
}
</script>

<style scoped>
.my-plants {
  padding: 20px 0;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.card-img-top {
  transition: transform 0.3s ease;
}

.card:hover .card-img-top {
  transform: scale(1.05);
}
</style>