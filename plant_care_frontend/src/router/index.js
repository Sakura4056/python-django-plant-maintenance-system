// plant_care_frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/plants',
    name: 'Plants',
    component: () => import('../views/plants/PlantList.vue')
  },
  {
    path: '/plants/:id',
    name: 'PlantDetail',
    component: () => import('../views/plants/PlantDetail.vue')
  },
  {
    path: '/my-plants',
    name: 'MyPlants',
    component: () => import('../views/care/MyPlantList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-plants/add',
    name: 'AddPlant',
    component: () => import('../views/care/AddPlant.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-plants/:id',
    name: 'MyPlantDetail',
    component: () => import('../views/care/MyPlantDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/care-plans',
    name: 'CarePlans',
    component: () => import('../views/care/CarePlanList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/care-records',
    name: 'CareRecords',
    component: () => import('../views/care/CareRecordList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/growth-photos',
    name: 'GrowthPhotos',
    component: () => import('../views/growth/GrowthPhotoList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/user/Profile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router