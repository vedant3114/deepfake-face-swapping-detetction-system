<template>
  <div class="explainability-container">
    <!-- Tab Navigation -->
    <div class="tabs-header">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tabs-content">
      <!-- 1. Prediction Summary Tab -->
      <div v-show="activeTab === 'summary'" class="tab-pane">
        <div class="prediction-card">
          <div :class="['prediction-badge', prediction.label.toLowerCase()]">
            {{ prediction.label }}
          </div>
          <div class="prediction-details">
            <div class="detail-row">
              <span class="label">Confidence Score:</span>
              <span class="value">{{ (prediction.score * 100).toFixed(2) }}%</span>
            </div>
            <div class="detail-row">
              <span class="label">Risk Level:</span>
              <span :class="['risk-badge', getRiskLevel(prediction.score)]">
                {{ getRiskLevel(prediction.score) }}
              </span>
            </div>
            <div class="detail-row">
              <span class="label">Analysis Type:</span>
              <span class="value">Multi-Modal (Audio + Video)</span>
            </div>
          </div>
        </div>

        <!-- Global Consistency Scores -->
        <div class="consistency-summary">
          <h3>📊 Global Consistency Scores</h3>
          <div class="consistency-grid">
            <div class="consistency-item audio">
              <i class="fas fa-volume-up"></i>
              <div class="consistency-info">
                <span class="name">Audio Consistency</span>
                <div class="bar-container">
                  <div class="bar" :style="{ width: consistency.audio * 100 + '%' }"></div>
                </div>
                <span class="score">{{ (consistency.audio * 100).toFixed(1) }}%</span>
              </div>
            </div>

            <div class="consistency-item video">
              <i class="fas fa-video"></i>
              <div class="consistency-info">
                <span class="name">Video Consistency</span>
                <div class="bar-container">
                  <div class="bar" :style="{ width: consistency.video * 100 + '%' }"></div>
                </div>
                <span class="score">{{ (consistency.video * 100).toFixed(1) }}%</span>
              </div>
            </div>

            <div class="consistency-item cross">
              <i class="fas fa-link"></i>
              <div class="consistency-info">
                <span class="name">Cross-Modal Consistency</span>
                <div class="bar-container">
                  <div class="bar" :style="{ width: consistency.cross_modal * 100 + '%' }"></div>
                </div>
                <span class="score">{{ (consistency.cross_modal * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Temporal Analysis Tab -->
      <div v-show="activeTab === 'temporal'" class="tab-pane">
        <div class="temporal-container">
          <h3>⏱️ Temporal Consistency Analysis</h3>
          <p class="description">
            Detects inconsistencies across video frames. Lower values indicate potential manipulation.
          </p>

          <!-- Audio Temporal -->
          <div class="temporal-section">
            <div class="section-header">
              <h4>🔊 Audio Temporal Consistency</h4>
              <span class="anomaly-count" v-if="anomalies.audio > 0">
                {{ anomalies.audio }} anomalies detected
              </span>
            </div>
            <canvas ref="audioChart" class="temporal-chart"></canvas>
            <p class="chart-desc">
              Red zones indicate frame-to-frame inconsistencies in audio patterns
            </p>
          </div>

          <!-- Video Temporal -->
          <div class="temporal-section">
            <div class="section-header">
              <h4>🎬 Video Temporal Consistency</h4>
              <span class="anomaly-count" v-if="anomalies.video > 0">
                {{ anomalies.video }} anomalies detected
              </span>
            </div>
            <canvas ref="videoChart" class="temporal-chart"></canvas>
            <p class="chart-desc">
              Red zones indicate frame-to-frame inconsistencies in visual patterns
            </p>
          </div>
        </div>
      </div>

      <!-- 3. Anomaly Detection Tab -->
      <div v-show="activeTab === 'anomalies'" class="tab-pane">
        <div class="anomaly-container">
          <h3>🔍 Anomaly Detection Report</h3>
          
          <div class="severity-indicator" :class="severity.toLowerCase()">
            <i :class="severityIcon"></i>
            <div class="severity-info">
              <span class="label">Overall Severity:</span>
              <span class="value">{{ severity }}</span>
            </div>
          </div>

          <div class="anomaly-stats">
            <div class="stat-card audio">
              <h4>Audio Anomalies</h4>
              <div class="count">{{ anomalies.audio }}</div>
              <p v-if="anomalies.audio === 0">✓ No inconsistencies found</p>
              <p v-else>Detected at {{ anomalies.audio_indices.length > 0 ? 'multiple frames' : '' }}</p>
            </div>

            <div class="stat-card video">
              <h4>Video Anomalies</h4>
              <div class="count">{{ anomalies.video }}</div>
              <p v-if="anomalies.video === 0">✓ No inconsistencies found</p>
              <p v-else>Detected at {{ anomalies.video_indices.length > 0 ? 'multiple frames' : '' }}</p>
            </div>

            <div class="stat-card combined">
              <h4>Total Issues</h4>
              <div class="count">{{ anomalies.audio + anomalies.video }}</div>
              <p>Across temporal sequence</p>
            </div>
          </div>

          <!-- Anomaly Indices -->
          <div v-if="anomalies.audio_indices.length > 0 || anomalies.video_indices.length > 0" class="anomaly-details">
            <div v-if="anomalies.audio_indices.length > 0" class="anomaly-list audio">
              <h4>🔊 Audio Anomaly Frames</h4>
              <div class="frame-list">
                <span v-for="idx in anomalies.audio_indices" :key="'a-' + idx" class="frame-badge">
                  Frame {{ idx }}
                </span>
              </div>
            </div>

            <div v-if="anomalies.video_indices.length > 0" class="anomaly-list video">
              <h4>🎬 Video Anomaly Frames</h4>
              <div class="frame-list">
                <span v-for="idx in anomalies.video_indices" :key="'v-' + idx" class="frame-badge">
                  Frame {{ idx }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. Technical Details Tab -->
      <div v-show="activeTab === 'technical'" class="tab-pane">
        <div class="technical-container">
          <h3>⚙️ Technical Analysis</h3>

          <div class="technical-section">
            <h4>Model Architecture</h4>
            <ul class="tech-list">
              <li><strong>Audio Extractor:</strong> Transformer-based temporal modeling with mel-spectrogram features</li>
              <li><strong>Video Extractor:</strong> ResNet18 backbone + Spatial Attention + Transformer encoder</li>
              <li><strong>Fusion Network:</strong> Cross-modal attention between audio and video modalities</li>
              <li><strong>Hidden Dimensions:</strong> 128 (optimized for small datasets)</li>
              <li><strong>Sequence Length:</strong> 32 frames/segments</li>
            </ul>
          </div>

          <div class="technical-section">
            <h4>Detection Features</h4>
            <ul class="tech-list">
              <li><strong>Audio Features:</strong> Mel-spectrogram (64 mels, 1024 FFT)</li>
              <li><strong>Video Features:</strong> 112x112 RGB frames with ImageNet normalization</li>
              <li><strong>Temporal Analysis:</strong> Frame-to-frame consistency scoring</li>
              <li><strong>Consistency Modules:</strong> Detects temporal inconsistencies in manipulated content</li>
            </ul>
          </div>

          <div class="technical-section">
            <h4>Regularization Techniques</h4>
            <ul class="tech-list">
              <li>Dropout Rate: 50% (reduces overfitting)</li>
              <li>Label Smoothing: 10% (improves generalization)</li>
              <li>Weight Decay: 0.01 (L2 regularization)</li>
              <li>Dynamic Class Balancing: Weights loss by class frequency</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'DeepfakeExplainability',
  props: {
    result: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      activeTab: 'summary',
      tabs: [
        { id: 'summary', label: 'Summary', icon: 'fas fa-chart-pie' },
        { id: 'temporal', label: 'Temporal Analysis', icon: 'fas fa-chart-line' },
        { id: 'anomalies', label: 'Anomalies', icon: 'fas fa-exclamation-circle' },
        { id: 'technical', label: 'Technical', icon: 'fas fa-cogs' }
      ],
      prediction: {
        label: 'LOADING',
        score: 0
      },
      consistency: {
        audio: 0,
        video: 0,
        cross_modal: 0
      },
      anomalies: {
        audio: 0,
        video: 0,
        audio_indices: [],
        video_indices: []
      },
      audioChart: null,
      videoChart: null
    };
  },
  computed: {
    severity() {
      const totalAnomalies = this.anomalies.audio + this.anomalies.video;
      if (totalAnomalies > 10) return 'HIGH';
      if (totalAnomalies > 3) return 'MEDIUM';
      return 'LOW';
    },
    severityIcon() {
      if (this.severity === 'HIGH') return 'fas fa-exclamation-triangle';
      if (this.severity === 'MEDIUM') return 'fas fa-exclamation-circle';
      return 'fas fa-check-circle';
    }
  },
  methods: {
    getRiskLevel(score) {
      if (score > 0.7) return 'HIGH';
      if (score > 0.4) return 'MEDIUM';
      return 'LOW';
    },
    initializeCharts() {
      this.$nextTick(() => {
        if (this.result.explainability) {
          this.drawTemporalCharts();
        }
      });
    },
    drawTemporalCharts() {
      const audioData = this.result.explainability.audio_temporal_consistency || [];
      const videoData = this.result.explainability.video_temporal_consistency || [];

      // Audio Chart
      if (this.$refs.audioChart && audioData.length > 0) {
        if (this.audioChart) this.audioChart.destroy();
        this.audioChart = new Chart(this.$refs.audioChart, {
          type: 'line',
          data: {
            labels: audioData.map((_, i) => `Frame ${i}`),
            datasets: [{
              label: 'Audio Consistency',
              data: audioData,
              borderColor: '#FF6B6B',
              backgroundColor: 'rgba(255, 107, 107, 0.1)',
              tension: 0.4,
              fill: true,
              pointRadius: 2,
              pointBackgroundColor: audioData.map(v => v < 0.3 ? '#FF0000' : '#FF6B6B')
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: true },
              title: { display: false }
            },
            scales: {
              y: { min: 0, max: 1 }
            }
          }
        });
      }

      // Video Chart
      if (this.$refs.videoChart && videoData.length > 0) {
        if (this.videoChart) this.videoChart.destroy();
        this.videoChart = new Chart(this.$refs.videoChart, {
          type: 'line',
          data: {
            labels: videoData.map((_, i) => `Frame ${i}`),
            datasets: [{
              label: 'Video Consistency',
              data: videoData,
              borderColor: '#4ECDC4',
              backgroundColor: 'rgba(78, 205, 196, 0.1)',
              tension: 0.4,
              fill: true,
              pointRadius: 2,
              pointBackgroundColor: videoData.map(v => v < 0.3 ? '#FF0000' : '#4ECDC4')
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: true },
              title: { display: false }
            },
            scales: {
              y: { min: 0, max: 1 }
            }
          }
        });
      }
    },
    loadExplainabilityData() {
      if (!this.result || !this.result.prediction) return;

      // Basic prediction
      this.prediction = {
        label: this.result.prediction.label,
        score: this.result.prediction.score
      };

      // Consistency scores
      if (this.result.explainability?.global_consistency) {
        this.consistency = {
          audio: this.result.explainability.global_consistency.audio,
          video: this.result.explainability.global_consistency.video,
          cross_modal: this.result.explainability.global_consistency.cross_modal
        };
      }

      // Anomalies
      if (this.result.explainability?.anomalies_detected) {
        const anom = this.result.explainability.anomalies_detected;
        this.anomalies = {
          audio: anom.audio_inconsistencies || 0,
          video: anom.video_inconsistencies || 0,
          audio_indices: anom.audio_anomaly_indices || [],
          video_indices: anom.video_anomaly_indices || []
        };
      }

      // Draw charts
      this.initializeCharts();
    }
  },
  watch: {
    result: {
      handler() {
        this.loadExplainabilityData();
      },
      deep: true
    }
  },
  mounted() {
    this.loadExplainabilityData();
  }
};
</script>

<style scoped>
.explainability-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 24px;
  color: #333;
}

/* Tabs */
.tabs-header {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 12px;
}

.tab-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  border-radius: 6px 6px 0 0;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.tab-btn.active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border-bottom: 2px solid white;
}

.tab-btn i {
  margin-right: 6px;
}

.tabs-content {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.tab-pane {
  padding: 24px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Prediction Card */
.prediction-card {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.prediction-badge {
  font-size: 32px;
  font-weight: bold;
  padding: 16px 24px;
  border-radius: 8px;
  min-width: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.prediction-badge.deepfake {
  background: #FF6B6B;
}

.prediction-badge.authentic {
  background: #51CF66;
}

.prediction-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.detail-row .label {
  opacity: 0.8;
}

.detail-row .value {
  font-weight: bold;
}

.risk-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.risk-badge.high {
  background: #FFE0E0;
  color: #D32F2F;
}

.risk-badge.medium {
  background: #FFF3E0;
  color: #F57C00;
}

.risk-badge.low {
  background: #E8F5E9;
  color: #388E3C;
}

/* Consistency Summary */
.consistency-summary {
  margin-top: 24px;
}

.consistency-summary h3 {
  color: #333;
  margin-bottom: 16px;
  font-size: 16px;
}

.consistency-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.consistency-item {
  padding: 16px;
  border-radius: 8px;
  background: #F5F5F5;
  display: flex;
  align-items: center;
  gap: 12px;
}

.consistency-item i {
  font-size: 24px;
}

.consistency-item.audio i { color: #FF6B6B; }
.consistency-item.video i { color: #4ECDC4; }
.consistency-item.cross i { color: #FFD93D; }

.consistency-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.consistency-info .name {
  font-size: 12px;
  color: #666;
  font-weight: 600;
}

.bar-container {
  height: 6px;
  background: #DDD;
  border-radius: 3px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.consistency-info .score {
  font-size: 13px;
  font-weight: bold;
  color: #333;
}

/* Temporal Analysis */
.temporal-container h3 {
  color: #333;
  margin-bottom: 8px;
}

.description {
  color: #666;
  font-size: 14px;
  margin-bottom: 24px;
}

.temporal-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h4 {
  color: #333;
  margin: 0;
}

.anomaly-count {
  background: #FFE0E0;
  color: #D32F2F;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.temporal-chart {
  max-height: 300px;
  margin-bottom: 8px;
}

.chart-desc {
  font-size: 12px;
  color: #999;
  margin: 0;
}

/* Anomaly Detection */
.anomaly-container h3 {
  color: #333;
  margin-bottom: 20px;
}

.severity-indicator {
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  font-weight: bold;
}

.severity-indicator.high {
  background: #FFE0E0;
  color: #D32F2F;
}

.severity-indicator.medium {
  background: #FFF3E0;
  color: #F57C00;
}

.severity-indicator.low {
  background: #E8F5E9;
  color: #388E3C;
}

.severity-indicator i {
  font-size: 20px;
}

.severity-info {
  display: flex;
  gap: 8px;
}

.anomaly-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 16px;
  border-radius: 8px;
  background: #F5F5F5;
  text-align: center;
}

.stat-card h4 {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 12px;
}

.stat-card .count {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.stat-card p {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.stat-card.audio { border-left: 4px solid #FF6B6B; }
.stat-card.video { border-left: 4px solid #4ECDC4; }
.stat-card.combined { border-left: 4px solid #FFD93D; }

.anomaly-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.anomaly-list {
  padding: 16px;
  border-radius: 8px;
  background: #F5F5F5;
}

.anomaly-list h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
}

.frame-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.frame-badge {
  background: white;
  border: 1px solid #DDD;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

/* Technical Details */
.technical-container h3 {
  color: #333;
  margin-bottom: 20px;
}

.technical-section {
  margin-bottom: 24px;
}

.technical-section h4 {
  color: #667eea;
  margin-bottom: 12px;
  font-size: 14px;
}

.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-list li {
  padding: 8px 0;
  border-bottom: 1px solid #EEE;
  font-size: 13px;
  color: #666;
}

.tech-list li:last-child {
  border-bottom: none;
}

.tech-list strong {
  color: #333;
}

@media (max-width: 768px) {
  .explainability-container {
    padding: 16px;
  }

  .tabs-header {
    flex-wrap: wrap;
  }

  .tab-btn {
    font-size: 12px;
    padding: 6px 12px;
  }

  .tab-pane {
    padding: 16px;
  }

  .prediction-card {
    flex-direction: column;
  }

  .consistency-grid {
    grid-template-columns: 1fr;
  }
}
</style>
