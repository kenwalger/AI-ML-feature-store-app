<template>
  <div class="card">
    <div class="card-header bg-dark text-white">
      <h5 class="mb-0">
        <i class="bi bi-graph-up"></i> Performance Metrics
      </h5>
    </div>
    <div class="card-body">
      <div class="row mb-3">
        <div class="col-md-3">
          <div class="card bg-light">
            <div class="card-body text-center">
              <h6 class="text-muted">Total Features</h6>
              <h3>{{ stats.total_features || 0 }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-light">
            <div class="card-body text-center">
              <h6 class="text-muted">Avg Query Latency</h6>
              <h3>{{ avgLatency }}ms</h3>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-light">
            <div class="card-body text-center">
              <h6 class="text-muted">Follower Pool</h6>
              <h3>
                <span :class="followerEnabled ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ followerEnabled ? 'Enabled' : 'Disabled' }}
                </span>
              </h3>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-light">
            <div class="card-body text-center">
              <h6 class="text-muted">Recent Searches</h6>
              <h3>{{ recentSearches.length }}</h3>
            </div>
          </div>
        </div>
      </div>

      <div v-if="recentSearches.length > 0" class="mt-4">
        <h6>Query Latency Over Time</h6>
        <ChartComponent :data="chartData" />
      </div>

      <div v-else class="text-center text-muted py-4">
        <p>No search queries yet. Perform a search to see metrics.</p>
      </div>
    </div>
  </div>
</template>

<script>
import ChartComponent from './ChartComponent.vue'
import api from '../services/api'

export default {
  name: 'MetricsPanel',
  components: {
    ChartComponent
  },
  props: {
    recentSearches: {
      type: Array,
      default: () => []
    },
    followerEnabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      stats: {},
      loading: false,
      refreshInterval: null
    }
  },
  computed: {
    avgLatency() {
      if (this.recentSearches.length === 0) return '0'
      const sum = this.recentSearches.reduce((acc, s) => acc + s.queryTime, 0)
      return (sum / this.recentSearches.length).toFixed(1)
    },
    chartData() {
      const labels = this.recentSearches
        .slice()
        .reverse()
        .map((_, i) => `Query ${i + 1}`)
      
      const primaryData = this.recentSearches
        .slice()
        .reverse()
        .map(s => s.database === 'primary' ? s.queryTime : null)
      
      const followerData = this.recentSearches
        .slice()
        .reverse()
        .map(s => s.database === 'follower' ? s.queryTime : null)

      return {
        labels,
        datasets: [
          {
            label: 'Primary DB',
            data: primaryData,
            borderColor: 'rgb(108, 117, 125)',
            backgroundColor: 'rgba(108, 117, 125, 0.2)',
            tension: 0.1
          },
          {
            label: 'Follower Pool',
            data: followerData,
            borderColor: 'rgb(13, 110, 253)',
            backgroundColor: 'rgba(13, 110, 253, 0.2)',
            tension: 0.1
          }
        ]
      }
    }
  },
  async mounted() {
    await this.loadStats()
    // Refresh stats every 5 seconds
    this.refreshInterval = setInterval(this.loadStats, 5000)
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    async loadStats() {
      try {
        this.stats = await api.getStats()
      } catch (error) {
        console.error('Failed to load stats:', error)
      }
    }
  }
}
</script>

