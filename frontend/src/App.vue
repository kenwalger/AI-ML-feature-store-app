<template>
  <div class="container-fluid">
    <nav class="navbar navbar-dark bg-primary mb-4">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">
          <i class="bi bi-database"></i> AI/ML Feature Store - Heroku NGPG Demo
        </span>
      </div>
    </nav>

    <div class="container">
      <div class="row">
        <!-- Toggle Panel -->
        <div class="col-12 mb-4">
          <TogglePanel @toggle-changed="handleToggleChanged" />
        </div>

        <!-- Main Content -->
        <div class="col-lg-6 mb-4">
          <IngestionPanel @ingestion-complete="handleIngestionComplete" />
        </div>

        <div class="col-lg-6 mb-4">
          <SearchPanel @search-complete="handleSearchComplete" />
        </div>

        <!-- Metrics Panel -->
        <div class="col-12 mb-4">
          <MetricsPanel 
            :recent-searches="recentSearches"
            :follower-enabled="followerEnabled"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TogglePanel from './components/TogglePanel.vue'
import IngestionPanel from './components/IngestionPanel.vue'
import SearchPanel from './components/SearchPanel.vue'
import MetricsPanel from './components/MetricsPanel.vue'

export default {
  name: 'App',
  components: {
    TogglePanel,
    IngestionPanel,
    SearchPanel,
    MetricsPanel
  },
  data() {
    return {
      followerEnabled: false,
      recentSearches: []
    }
  },
  methods: {
    handleToggleChanged(enabled) {
      this.followerEnabled = enabled
    },
    handleIngestionComplete() {
      // Refresh stats if needed
    },
    handleSearchComplete(searchData) {
      this.recentSearches.unshift(searchData)
      if (this.recentSearches.length > 10) {
        this.recentSearches.pop()
      }
    }
  }
}
</script>

<style>
body {
  background-color: #f8f9fa;
}
</style>

