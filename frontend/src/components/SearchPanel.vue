<template>
  <div class="card">
    <div class="card-header bg-warning text-dark">
      <h5 class="mb-0">
        <i class="bi bi-search"></i> Vector Similarity Search
      </h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label for="searchQuery" class="form-label">Search Query</label>
        <input
          type="text"
          class="form-control"
          id="searchQuery"
          v-model="query"
          placeholder="Enter search query..."
          @keyup.enter="search"
          :disabled="loading"
        >
      </div>

      <div class="mb-3">
        <label for="searchLimit" class="form-label">Results Limit</label>
        <input
          type="number"
          class="form-control"
          id="searchLimit"
          v-model.number="limit"
          min="1"
          max="100"
          :disabled="loading"
        >
      </div>

      <button
        class="btn btn-warning w-100"
        @click="search"
        :disabled="loading || !query.trim()"
      >
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        <i v-else class="bi bi-search me-2"></i>
        {{ loading ? 'Searching...' : 'Search' }}
      </button>

      <div v-if="searchResult" class="mt-3">
        <div class="alert alert-info" role="alert">
          <strong>Query Time:</strong> {{ searchResult.query_time_ms }}ms
          <br>
          <strong>Database:</strong> {{ searchResult.database_used }}
          <br>
          <strong>Results:</strong> {{ searchResult.results.length }}
        </div>

        <div v-if="searchResult.results.length > 0" class="mt-3">
          <h6>Results:</h6>
          <div class="list-group">
            <div
              v-for="(result, index) in searchResult.results"
              :key="index"
              class="list-group-item"
            >
              <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">{{ result.feature.name }}</h6>
                <small class="badge bg-primary">{{ (result.similarity_score * 100).toFixed(1) }}%</small>
              </div>
              <p class="mb-1 text-muted">{{ result.feature.description }}</p>
              <small v-if="result.feature.category" class="badge bg-secondary me-1">
                {{ result.feature.category }}
              </small>
              <small v-if="result.feature.price" class="text-muted">
                ${{ result.feature.price.toFixed(2) }}
              </small>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="mt-3">
        <div class="alert alert-danger" role="alert">
          <strong>Error:</strong> {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'SearchPanel',
  data() {
    return {
      query: '',
      limit: 10,
      loading: false,
      searchResult: null,
      error: null
    }
  },
  methods: {
    async search() {
      if (!this.query.trim()) return

      this.loading = true
      this.searchResult = null
      this.error = null

      try {
        const result = await api.searchFeatures(this.query, this.limit)
        this.searchResult = result
        
        // Emit search complete event with data for metrics
        this.$emit('search-complete', {
          query: this.query,
          queryTime: result.query_time_ms,
          database: result.database_used,
          resultCount: result.results.length,
          timestamp: Date.now()
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Search failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

