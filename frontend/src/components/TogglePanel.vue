<template>
  <div class="card">
    <div class="card-header bg-info text-white">
      <h5 class="mb-0">
        <i class="bi bi-toggle-on"></i> Follower Pool Toggle
      </h5>
    </div>
    <div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <div>
          <p class="mb-1">
            <strong>Current Status:</strong>
            <span :class="statusClass">{{ statusText }}</span>
          </p>
          <small class="text-muted">
            Toggle to switch between primary database and follower pool for read queries
          </small>
        </div>
        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            :checked="enabled"
            @change="handleToggle"
            :disabled="loading"
            style="width: 3rem; height: 1.5rem;"
          >
        </div>
      </div>
      <div v-if="message" class="alert alert-info mt-3 mb-0" role="alert">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'TogglePanel',
  data() {
    return {
      enabled: false,
      loading: false,
      message: ''
    }
  },
  computed: {
    statusText() {
      return this.enabled ? 'Follower Pool Enabled' : 'Primary Database'
    },
    statusClass() {
      return this.enabled ? 'badge bg-success ms-2' : 'badge bg-secondary ms-2'
    }
  },
  async mounted() {
    await this.loadStatus()
  },
  methods: {
    async loadStatus() {
      try {
        const data = await api.getFollowerStatus()
        this.enabled = data.follower_pool_enabled
      } catch (error) {
        console.error('Failed to load follower status:', error)
      }
    },
    async handleToggle(event) {
      this.loading = true
      const newValue = event.target.checked
      
      try {
        const data = await api.toggleFollowerPool(newValue)
        this.enabled = data.follower_pool_enabled
        this.message = data.message
        this.$emit('toggle-changed', this.enabled)
        
        // Clear message after 3 seconds
        setTimeout(() => {
          this.message = ''
        }, 3000)
      } catch (error) {
        console.error('Failed to toggle follower pool:', error)
        // Show the actual error message from the backend if available
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to toggle follower pool. Please try again.'
        this.message = errorMessage
        // Revert checkbox
        event.target.checked = !newValue
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

