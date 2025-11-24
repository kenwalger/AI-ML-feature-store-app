<template>
  <div class="card">
    <div class="card-header bg-success text-white">
      <h5 class="mb-0">
        <i class="bi bi-upload"></i> Feature Ingestion
      </h5>
    </div>
    <div class="card-body">
      <div class="mb-3">
        <label for="batchSize" class="form-label">Batch Size</label>
        <input
          type="number"
          class="form-control"
          id="batchSize"
          v-model.number="batchSize"
          min="1"
          max="100"
          :disabled="loading"
        >
        <small class="form-text text-muted">Number of features to generate and ingest</small>
      </div>
      
      <button
        class="btn btn-primary w-100"
        @click="ingestBatch"
        :disabled="loading"
      >
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        <i v-else class="bi bi-cloud-upload me-2"></i>
        {{ loading ? 'Ingesting...' : 'Ingest Batch' }}
      </button>

      <div v-if="result" class="mt-3">
        <div class="alert alert-success" role="alert">
          <strong>Success!</strong> Ingested {{ result.count }} features in {{ result.time }}ms
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
  name: 'IngestionPanel',
  data() {
    return {
      batchSize: 10,
      loading: false,
      result: null,
      error: null
    }
  },
  methods: {
    async ingestBatch() {
      this.loading = true
      this.result = null
      this.error = null

      try {
        // Generate mock features (this would normally come from the backend)
        // For now, we'll create a simple batch request
        const startTime = Date.now()
        
        // Call backend to generate and ingest
        // Note: In a real implementation, you might want a dedicated endpoint
        // that generates and ingests in one call
        const features = this.generateMockFeatures(this.batchSize)
        const response = await api.ingestFeaturesBatch(features)
        
        const elapsed = Date.now() - startTime
        
        this.result = {
          count: response.length,
          time: elapsed
        }
        
        this.$emit('ingestion-complete')
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to ingest features'
      } finally {
        this.loading = false
      }
    },
    generateMockFeatures(count) {
      // Simple mock feature generator for demo
      const categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports']
      const features = []
      
      for (let i = 0; i < count; i++) {
        const category = categories[Math.floor(Math.random() * categories.length)]
        features.push({
          name: `Product ${i + 1}`,
          description: `A great ${category.toLowerCase()} product`,
          category: category,
          price: Math.round((Math.random() * 100 + 10) * 100) / 100
        })
      }
      
      return features
    }
  }
}
</script>

