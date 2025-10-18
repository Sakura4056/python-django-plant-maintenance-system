// plant_care_frontend/src/store/index.js
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isLoading: false,
    error: null
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    currentUser: state => state.user,
    isLoading: state => state.isLoading,
    error: state => state.error
  },
  mutations: {
    SET_AUTH(state, { user, accessToken, refreshToken }) {
      state.user = user
      state.accessToken = accessToken
      state.refreshToken = refreshToken
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.accessToken = null
      state.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await axios.post('/token/', { username, password })
        const { access, refresh, user } = response.data
        
        commit('SET_AUTH', { user, accessToken: access, refreshToken: refresh })
        return user
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || 'Login failed')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await axios.post('/users/register/', userData)
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data || 'Registration failed')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async logout({ commit }) {
      commit('CLEAR_AUTH')
    },
    
    async getUserProfile({ commit }) {
      commit('SET_LOADING', true)
      
      try {
        const response = await axios.get('/users/profile/')
        commit('SET_AUTH', {
          user: response.data,
          accessToken: this.state.accessToken,
          refreshToken: this.state.refreshToken
        })
        return response.data
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateProfile({ commit }, profileData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      
      try {
        const response = await axios.patch('/users/profile/', profileData)
        commit('SET_AUTH', {
          user: response.data,
          accessToken: this.state.accessToken,
          refreshToken: this.state.refreshToken
        })
        return response.data
      } catch (error) {
        commit('SET_ERROR', error.response?.data || 'Update failed')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  modules: {
    plants: {
      namespaced: true,
      state: {
        plants: [],
        currentPlant: null,
        categories: []
      },
      getters: {
        allPlants: state => state.plants,
        currentPlant: state => state.currentPlant,
        allCategories: state => state.categories
      },
      mutations: {
        SET_PLANTS(state, plants) {
          state.plants = plants
        },
        SET_CURRENT_PLANT(state, plant) {
          state.currentPlant = plant
        },
        SET_CATEGORIES(state, categories) {
          state.categories = categories
        }
      },
      actions: {
        async fetchPlants({ commit }, params = {}) {
          const response = await axios.get('/plants/', { params })
          commit('SET_PLANTS', response.data.results)
          return response.data
        },
        
        async fetchPlantDetail({ commit }, id) {
          const response = await axios.get(`/plants/${id}/`)
          commit('SET_CURRENT_PLANT', response.data)
          return response.data
        },
        
        async fetchCategories({ commit }) {
          const response = await axios.get('/plants/categories/')
          commit('SET_CATEGORIES', response.data)
          return response.data
        }
      }
    },
    
    myPlants: {
      namespaced: true,
      state: {
        myPlants: [],
        currentMyPlant: null
      },
      getters: {
        allMyPlants: state => state.myPlants,
        currentMyPlant: state => state.currentMyPlant
      },
      mutations: {
        SET_MY_PLANTS(state, plants) {
          state.myPlants = plants
        },
        SET_CURRENT_MY_PLANT(state, plant) {
          state.currentMyPlant = plant
        },
        ADD_MY_PLANT(state, plant) {
          state.myPlants.push(plant)
        },
        UPDATE_MY_PLANT(state, updatedPlant) {
          const index = state.myPlants.findIndex(p => p.id === updatedPlant.id)
          if (index !== -1) {
            state.myPlants[index] = updatedPlant
          }
        },
        DELETE_MY_PLANT(state, plantId) {
          state.myPlants = state.myPlants.filter(p => p.id !== plantId)
        }
      },
      actions: {
        async fetchMyPlants({ commit }, params = {}) {
          const response = await axios.get('/care/my-plants/', { params })
          commit('SET_MY_PLANTS', response.data.results)
          return response.data
        },
        
        async fetchMyPlantDetail({ commit }, id) {
          const response = await axios.get(`/care/my-plants/${id}/`)
          commit('SET_CURRENT_MY_PLANT', response.data)
          return response.data
        },
        
        async addMyPlant({ commit }, plantData) {
          const response = await axios.post('/care/my-plants/', plantData)
          commit('ADD_MY_PLANT', response.data)
          return response.data
        },
        
        async updateMyPlant({ commit }, { id, plantData }) {
          const response = await axios.patch(`/care/my-plants/${id}/`, plantData)
          commit('UPDATE_MY_PLANT', response.data)
          return response.data
        },
        
        async deleteMyPlant({ commit }, id) {
          await axios.delete(`/care/my-plants/${id}/`)
          commit('DELETE_MY_PLANT', id)
        },
        
        async generateCarePlan({ commit }, plantId) {
          const response = await axios.post(`/care/my-plants/${plantId}/generate_care_plan/`)
          return response.data
        }
      }
    },
    
    care: {
      namespaced: true,
      state: {
        carePlans: [],
        careRecords: [],
        careReminders: [],
        dashboard: {}
      },
      getters: {
        allCarePlans: state => state.carePlans,
        allCareRecords: state => state.careRecords,
        allCareReminders: state => state.careReminders,
        dashboardData: state => state.dashboard
      },
      mutations: {
        SET_CARE_PLANS(state, plans) {
          state.carePlans = plans
        },
        SET_CARE_RECORDS(state, records) {
          state.careRecords = records
        },
        SET_CARE_REMINDERS(state, reminders) {
          state.careReminders = reminders
        },
        SET_DASHBOARD(state, data) {
          state.dashboard = data
        }
      },
      actions: {
        async fetchCarePlans({ commit }, params = {}) {
          const response = await axios.get('/care/care-plans/', { params })
          commit('SET_CARE_PLANS', response.data.results)
          return response.data
        },
        
        async fetchCareRecords({ commit }, params = {}) {
          const response = await axios.get('/care/care-records/', { params })
          commit('SET_CARE_RECORDS', response.data.results)
          return response.data
        },
        
        async fetchCareReminders({ commit }, params = {}) {
          const response = await axios.get('/care/care-reminders/', { params })
          commit('SET_CARE_REMINDERS', response.data.results)
          return response.data
        },
        
        async addCareRecord({ commit }, recordData) {
          const response = await axios.post('/care/care-records/', recordData)
          return response.data
        },
        
        async fetchDashboard({ commit }) {
          const response = await axios.get('/care/dashboard/statistics/')
          commit('SET_DASHBOARD', response.data)
          return response.data
        }
      }
    },
    
    growth: {
      namespaced: true,
      state: {
        growthPhotos: [],
        growthMeasurements: [],
        growthAnalyses: [],
        timeline: [],
        statistics: {}
      },
      getters: {
        allGrowthPhotos: state => state.growthPhotos,
        allGrowthMeasurements: state => state.growthMeasurements,
        allGrowthAnalyses: state => state.growthAnalyses,
        timelineData: state => state.timeline,
        growthStatistics: state => state.statistics
      },
      mutations: {
        SET_GROWTH_PHOTOS(state, photos) {
          state.growthPhotos = photos
        },
        SET_GROWTH_MEASUREMENTS(state, measurements) {
          state.growthMeasurements = measurements
        },
        SET_GROWTH_ANALYSES(state, analyses) {
          state.growthAnalyses = analyses
        },
        SET_TIMELINE(state, data) {
          state.timeline = data
        },
        SET_STATISTICS(state, data) {
          state.statistics = data
        }
      },
      actions: {
        async fetchGrowthPhotos({ commit }, params = {}) {
          const response = await axios.get('/growth/photos/', { params })
          commit('SET_GROWTH_PHOTOS', response.data.results)
          return response.data
        },
        
        async addGrowthPhoto({ commit }, photoData) {
          const formData = new FormData()
          for (const key in photoData) {
            formData.append(key, photoData[key])
          }
          
          const response = await axios.post('/growth/photos/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          return response.data
        },
        
        async fetchGrowthMeasurements({ commit }, params = {}) {
          const response = await axios.get('/growth/measurements/', { params })
          commit('SET_GROWTH_MEASUREMENTS', response.data.results)
          return response.data
        },
        
        async addGrowthMeasurement({ commit }, measurementData) {
          const response = await axios.post('/growth/measurements/', measurementData)
          return response.data
        },
        
        async fetchGrowthAnalyses({ commit }, params = {}) {
          const response = await axios.get('/growth/analyses/', { params })
          commit('SET_GROWTH_ANALYSES', response.data.results)
          return response.data
        },
        
        async fetchTimeline({ commit }, plantId) {
          const response = await axios.get('/growth/dashboard/timeline/', {
            params: { plant_id: plantId }
          })
          commit('SET_TIMELINE', response.data)
          return response.data
        },
        
        async fetchGrowthStatistics({ commit }, plantId) {
          const response = await axios.get('/growth/dashboard/statistics/', {
            params: { plant_id: plantId }
          })
          commit('SET_STATISTICS', response.data)
          return response.data
        }
      }
    }
  }
})