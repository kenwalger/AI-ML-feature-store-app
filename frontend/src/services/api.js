import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Ingestion
  async ingestFeature(feature) {
    const response = await api.post('/api/ingest', feature)
    return response.data
  },

  async ingestFeaturesBatch(features) {
    const response = await api.post('/api/ingest/batch', features)
    return response.data
  },

  // Search
  async searchFeatures(query, limit = 10, threshold = 0.0) {
    const response = await api.get('/api/search', {
      params: { query, limit, threshold }
    })
    return response.data
  },

  async searchFeaturesPost(searchQuery) {
    const response = await api.post('/api/search', searchQuery)
    return response.data
  },

  // Features
  async getFeature(id) {
    const response = await api.get(`/api/features/${id}`)
    return response.data
  },

  // Stats
  async getStats() {
    const response = await api.get('/api/stats')
    return response.data
  },

  // Toggle
  async getFollowerStatus() {
    const response = await api.get('/api/toggle/follower')
    return response.data
  },

  async toggleFollowerPool(enabled) {
    const response = await api.post('/api/toggle/follower', null, {
      params: { enabled }
    })
    return response.data
  }
}

