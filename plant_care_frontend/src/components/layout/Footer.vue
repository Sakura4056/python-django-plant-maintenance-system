<!-- plant_care_frontend/src/components/layout/Footer.vue -->
<template>
  <footer class="bg-dark text-white py-6">
    <div class="container">
      <div class="row row-cols-1 md:row-cols-3 gap-4">
        <div>
          <h5 class="mb-3">植物养护管理系统</h5>
          <p class="text-muted">
            让植物养护变得简单、科学、有趣。帮助植物爱好者更好地管理和养护植物。
          </p>
        </div>
        <div>
          <h5 class="mb-3">快速链接</h5>
          <ul class="list-unstyled">
            <li><router-link to="/about" class="text-muted">关于我们</router-link></li>
            <li><router-link to="/plants" class="text-muted">植物库</router-link></li>
            <li><router-link to="/dashboard" class="text-muted">用户仪表板</router-link></li>
          </ul>
        </div>
        <div>
          <h5 class="mb-3">联系我们</h5>
          <ul class="list-unstyled text-muted">
            <li><i class="bi bi-envelope me-2"></i>contact@plantcare.com</li>
            <li><i class="bi bi-phone me-2"></i>+86 123 4567 8910</li>
            <li><i class="bi bi-geo-alt me-2"></i>北京市朝阳区科技园</li>
          </ul>
        </div>
      </div>
      <hr class="border-secondary">
      <div class="text-center text-muted">
        <p>&copy; 2024 植物养护管理系统. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
footer {
  margin-top: auto;
}

h5 {
  color: #ffffff;
}

a {
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: #4CAF50 !important;
}
</style>