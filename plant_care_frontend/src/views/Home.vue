<!-- plant_care_frontend/src/views/Home.vue -->
<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero bg-gradient-to-r from-green-400 to-blue-500 text-white py-16">
      <div class="container text-center">
        <h1 class="display-4 mb-4">智能植物养护管理系统</h1>
        <p class="lead mb-6">让植物养护变得简单、科学、有趣</p>
        <div class="d-flex justify-content-center gap-4">
          <router-link to="/register" class="btn btn-light btn-lg">
            开始使用
          </router-link>
          <router-link to="/plants" class="btn btn-outline-light btn-lg">
            浏览植物库
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-12">
      <div class="container">
        <h2 class="text-center mb-10">系统功能</h2>
        <div class="row row-cols-1 md:row-cols-2 lg:row-cols-4 gap-6">
          <div class="card h-100">
            <div class="card-body text-center">
              <div class="mb-4">
                <i class="bi bi-search text-4xl text-green-500"></i>
              </div>
              <h5 class="card-title">植物信息库</h5>
              <p class="card-text">收录常见植物的详细信息，包括生长习性、养护要点等</p>
            </div>
          </div>
          
          <div class="card h-100">
            <div class="card-body text-center">
              <div class="mb-4">
                <i class="bi bi-calendar-check text-4xl text-blue-500"></i>
              </div>
              <h5 class="card-title">智能养护计划</h5>
              <p class="card-text">根据植物特性自动生成个性化养护计划和提醒</p>
            </div>
          </div>
          
          <div class="card h-100">
            <div class="card-body text-center">
              <div class="mb-4">
                <i class="bi bi-journal-text text-4xl text-purple-500"></i>
              </div>
              <h5 class="card-title">养护记录</h5>
              <p class="card-text">详细记录每次养护操作，跟踪植物生长历程</p>
            </div>
          </div>
          
          <div class="card h-100">
            <div class="card-body text-center">
              <div class="mb-4">
                <i class="bi bi-camera text-4xl text-orange-500"></i>
              </div>
              <h5 class="card-title">成长相册</h5>
              <p class="card-text">上传植物照片，记录成长变化，生成成长时间轴</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-12 bg-light">
      <div class="container">
        <h2 class="text-center mb-10">使用流程</h2>
        <div class="row row-cols-1 md:row-cols-3 gap-8">
          <div class="text-center">
            <div class="bg-primary text-white rounded-circle w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">1</div>
            <h3 class="mb-3">添加植物</h3>
            <p>从植物库中选择您的植物，或添加新的植物信息</p>
          </div>
          
          <div class="text-center">
            <div class="bg-primary text-white rounded-circle w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">2</div>
            <h3 class="mb-3">制定计划</h3>
            <p>系统自动生成养护计划，包括浇水、施肥等提醒</p>
          </div>
          
          <div class="text-center">
            <div class="bg-primary text-white rounded-circle w-16 h-16 flex items-center justify-center mx-auto mb-4 text-2xl font-bold">3</div>
            <h3 class="mb-3">记录成长</h3>
            <p>记录养护操作，上传照片，跟踪植物成长历程</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  mounted() {
    // Auto-scroll to top when component is mounted
    window.scrollTo(0, 0)
  }
}
</script>

<style scoped>
.hero {
  background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1512314889357-e157c22f938d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
</style>