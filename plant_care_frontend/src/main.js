// plant_care_frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import { BootstrapVue3 } from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

// Create Vue app
const app = createApp(App)

// Configure Axios
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Request interceptor for adding auth token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Response interceptor for token refresh
axios.interceptors.response.use(response => {
  return response
}, async error => {
  const originalRequest = error.config
  
  // If error is 401 and not already retrying
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true
    
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      const response = await axios.post('/token/refresh/', {
        refresh: refreshToken
      })
      
      const { access } = response.data
      localStorage.setItem('access_token', access)
      
      // Retry original request with new token
      originalRequest.headers.Authorization = `Bearer ${access}`
      return axios(originalRequest)
    } catch (refreshError) {
      // Refresh token failed, redirect to login
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/login')
      return Promise.reject(refreshError)
    }
  }
  
  return Promise.reject(error)
})

// Make axios available globally
app.config.globalProperties.$axios = axios

// Use plugins
app.use(store)
app.use(router)
app.use(BootstrapVue3)

// Mount app
app.mount('#app')