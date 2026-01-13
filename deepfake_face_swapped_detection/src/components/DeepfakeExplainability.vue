<template>
  <div class="explainability-container cyber-explainability">
    <!-- Cyber Header -->
    <div class="cyber-header">
      <div class="cyber-title">
        <i class="fas fa-shield-alt"></i>
        <span>DEEPFAKE ANALYSIS REPORT</span>
      </div>
      <div class="status-indicators">
        <div class="status-dot" :class="getStatusClass()"></div>
        <span class="status-text">{{ getStatusText() }}</span>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs-header cyber-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-btn cyber-tab', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tabs-content cyber-content">
      <!-- 1. Prediction Summary Tab -->
      <div v-show="activeTab === 'summary'" class="tab-pane">
        <div class="prediction-card cyber-card">
          <div class="prediction-header">
            <h3>📊 PREDICTION SUMMARY</h3>
            <div :class="['prediction-badge cyber-badge', prediction.label.toLowerCase()]">
              {{ prediction.label }}
            </div>
          </div>

          <div class="prediction-details">
            <div class="detail-row">
              <span class="label">CONFIDENCE SCORE:</span>
              <span class="value">{{ (prediction.score * 100).toFixed(2) }}%</span>
            </div>
            <div class="detail-row">
              <span class="label">RISK LEVEL:</span>
              <span :class="['risk-badge cyber-risk', getRiskLevel(prediction.score)]">
                {{ getRiskLevel(prediction.score) }}
              </span>
            </div>
            <div class="detail-row">
              <span class="label">ANALYSIS TYPE:</span>
              <span class="value">MULTI-MODAL (AUDIO + VIDEO)</span>
            </div>
          </div>
        </div>

        <!-- Global Consistency Scores -->
        <div class="consistency-summary cyber-section">
          <h3>📊 GLOBAL CONSISTENCY SCORES</h3>
          <div class="consistency-grid">
            <div class="consistency-item audio cyber-item">
              <div class="item-header">
                <i class="fas fa-volume-up"></i>
                <span class="name">AUDIO CONSISTENCY</span>
              </div>
              <div class="bar-container cyber-bar">
                <div class="bar" :style="{ width: consistency.audio * 100 + '%' }"></div>
              </div>
              <span class="score">{{ (consistency.audio * 100).toFixed(1) }}%</span>
            </div>

            <div class="consistency-item video cyber-item">
              <div class="item-header">
                <i class="fas fa-video"></i>
                <span class="name">VIDEO CONSISTENCY</span>
              </div>
              <div class="bar-container cyber-bar">
                <div class="bar" :style="{ width: consistency.video * 100 + '%' }"></div>
              </div>
              <span class="score">{{ (consistency.video * 100).toFixed(1) }}%</span>
            </div>

            <div class="consistency-item cross cyber-item">
              <div class="item-header">
                <i class="fas fa-link"></i>
                <span class="name">CROSS-MODAL CONSISTENCY</span>
              </div>
              <div class="bar-container cyber-bar">
                <div class="bar" :style="{ width: consistency.cross_modal * 100 + '%' }"></div>
              </div>
              <span class="score">{{ (consistency.cross_modal * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Temporal Analysis Tab -->
      <div v-show="activeTab === 'temporal'" class="tab-pane">
        <div class="temporal-container cyber-section">
          <h3>⏱️ TEMPORAL CONSISTENCY ANALYSIS</h3>
          <p class="description">
            DETECTS INCONSISTENCIES ACROSS VIDEO FRAMES. LOWER VALUES INDICATE POTENTIAL MANIPULATION.
          </p>

          <!-- Audio Temporal -->
          <div class="temporal-section cyber-subsection">
            <div class="section-header">
              <h4>🔊 AUDIO TEMPORAL CONSISTENCY</h4>
              <span class="anomaly-count" v-if="anomalies.audio > 0">
                {{ anomalies.audio }} ANOMALIES DETECTED
              </span>
            </div>
            <canvas ref="audioChart" class="temporal-chart cyber-chart"></canvas>
            <p class="chart-desc">
              RED ZONES INDICATE FRAME-TO-FRAME INCONSISTENCIES IN AUDIO PATTERNS
            </p>
          </div>

          <!-- Video Temporal -->
          <div class="temporal-section cyber-subsection">
            <div class="section-header">
              <h4>🎬 VIDEO TEMPORAL CONSISTENCY</h4>
              <span class="anomaly-count" v-if="anomalies.video > 0">
                {{ anomalies.video }} ANOMALIES DETECTED
              </span>
            </div>
            <canvas ref="videoChart" class="temporal-chart cyber-chart"></canvas>
            <p class="chart-desc">
              RED ZONES INDICATE FRAME-TO-FRAME INCONSISTENCIES IN VISUAL PATTERNS
            </p>
          </div>
        </div>
      </div>

      <!-- 3. Anomaly Detection Tab -->
      <div v-show="activeTab === 'anomalies'" class="tab-pane">
        <div class="anomaly-container cyber-section">
          <h3>🔍 ANOMALY DETECTION REPORT</h3>

          <div class="severity-indicator cyber-severity" :class="severity.toLowerCase()">
            <i :class="severityIcon"></i>
            <div class="severity-info">
              <span class="label">OVERALL SEVERITY:</span>
              <span class="value">{{ severity }}</span>
            </div>
          </div>

          <div class="anomaly-stats">
            <div class="stat-card audio cyber-stat">
              <div class="stat-header">
                <i class="fas fa-volume-up"></i>
                <h4>AUDIO ANOMALIES</h4>
              </div>
              <div class="count">{{ anomalies.audio }}</div>
              <p v-if="anomalies.audio === 0">✓ NO INCONSISTENCIES FOUND</p>
              <p v-else>DETECTED AT {{ anomalies.audio_indices.length > 0 ? 'MULTIPLE FRAMES' : '' }}</p>
            </div>

            <div class="stat-card video cyber-stat">
              <div class="stat-header">
                <i class="fas fa-video"></i>
                <h4>VIDEO ANOMALIES</h4>
              </div>
              <div class="count">{{ anomalies.video }}</div>
              <p v-if="anomalies.video === 0">✓ NO INCONSISTENCIES FOUND</p>
              <p v-else>DETECTED AT {{ anomalies.video_indices.length > 0 ? 'MULTIPLE FRAMES' : '' }}</p>
            </div>

            <div class="stat-card combined cyber-stat">
              <div class="stat-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h4>TOTAL ISSUES</h4>
              </div>
              <div class="count">{{ anomalies.audio + anomalies.video }}</div>
              <p>ACROSS TEMPORAL SEQUENCE</p>
            </div>
          </div>

          <!-- Anomaly Indices -->
          <div v-if="anomalies.audio_indices.length > 0 || anomalies.video_indices.length > 0" class="anomaly-details">
            <div v-if="anomalies.audio_indices.length > 0" class="anomaly-list audio cyber-anomaly-list">
              <div class="list-header">
                <i class="fas fa-volume-up"></i>
                <h4>🔊 AUDIO ANOMALY FRAMES</h4>
              </div>
              <div class="frame-list">
                <span v-for="idx in anomalies.audio_indices" :key="'a-' + idx" class="frame-badge cyber-badge">
                  FRAME {{ idx }}
                </span>
              </div>
            </div>

            <div v-if="anomalies.video_indices.length > 0" class="anomaly-list video cyber-anomaly-list">
              <div class="list-header">
                <i class="fas fa-video"></i>
                <h4>🎬 VIDEO ANOMALY FRAMES</h4>
              </div>
              <div class="frame-list">
                <span v-for="idx in anomalies.video_indices" :key="'v-' + idx" class="frame-badge cyber-badge">
                  FRAME {{ idx }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. Technical Details Tab -->
      <div v-show="activeTab === 'technical'" class="tab-pane">
        <div class="technical-container cyber-section">
          <h3>⚙️ TECHNICAL ANALYSIS</h3>

          <div class="technical-section cyber-subsection">
            <div class="section-header">
              <i class="fas fa-microchip"></i>
              <h4>MODEL ARCHITECTURE</h4>
            </div>
            <ul class="tech-list cyber-list">
              <li><strong>AUDIO EXTRACTOR:</strong> TRANSFORMER-BASED TEMPORAL MODELING WITH MEL-SPECTROGRAM FEATURES</li>
              <li><strong>VIDEO EXTRACTOR:</strong> RESNET18 BACKBONE + SPATIAL ATTENTION + TRANSFORMER ENCODER</li>
              <li><strong>FUSION NETWORK:</strong> CROSS-MODAL ATTENTION BETWEEN AUDIO AND VIDEO MODALITIES</li>
              <li><strong>HIDDEN DIMENSIONS:</strong> 128 (OPTIMIZED FOR SMALL DATASETS)</li>
              <li><strong>SEQUENCE LENGTH:</strong> 32 FRAMES/SEGMENTS</li>
            </ul>
          </div>

          <div class="technical-section cyber-subsection">
            <div class="section-header">
              <i class="fas fa-cogs"></i>
              <h4>DETECTION FEATURES</h4>
            </div>
            <ul class="tech-list cyber-list">
              <li><strong>AUDIO FEATURES:</strong> MEL-SPECTROGRAM (64 MELS, 1024 FFT)</li>
              <li><strong>VIDEO FEATURES:</strong> 112X112 RGB FRAMES WITH IMAGENET NORMALIZATION</li>
              <li><strong>TEMPORAL ANALYSIS:</strong> FRAME-TO-FRAME CONSISTENCY SCORING</li>
              <li><strong>CONSISTENCY MODULES:</strong> DETECTS TEMPORAL INCONSISTENCIES IN MANIPULATED CONTENT</li>
            </ul>
          </div>

          <div class="technical-section cyber-subsection">
            <div class="section-header">
              <i class="fas fa-shield-alt"></i>
              <h4>REGULARIZATION TECHNIQUES</h4>
            </div>
            <ul class="tech-list cyber-list">
              <li>DROPOUT RATE: 50% (REDUCES OVERFITTING)</li>
              <li>LABEL SMOOTHING: 10% (IMPROVES GENERALIZATION)</li>
              <li>WEIGHT DECAY: 0.01 (L2 REGULARIZATION)</li>
              <li>DYNAMIC CLASS BALANCING: WEIGHTS LOSS BY CLASS FREQUENCY</li>
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
        { id: 'summary', label: 'SUMMARY', icon: 'fas fa-chart-pie' },
        { id: 'temporal', label: 'TEMPORAL ANALYSIS', icon: 'fas fa-chart-line' },
        { id: 'anomalies', label: 'ANOMALIES', icon: 'fas fa-exclamation-circle' },
        { id: 'technical', label: 'TECHNICAL', icon: 'fas fa-cogs' }
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
    getStatusClass() {
      if (this.prediction.label === 'DEEPFAKE') return 'status-dot deepfake';
      if (this.prediction.label === 'AUTHENTIC') return 'status-dot authentic';
      return 'status-dot loading';
    },
    getStatusText() {
      if (this.prediction.label === 'DEEPFAKE') return 'DEEPFAKE DETECTED';
      if (this.prediction.label === 'AUTHENTIC') return 'AUTHENTIC CONTENT';
      return 'ANALYZING...';
    },
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
/* Cyber Theme Base Styles */
.cyber-explainability {
  background: rgba(10, 14, 42, 0.8);
  border-radius: 12px;
  padding: 0;
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.2);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

/* Cyber Header */
.cyber-header {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
  padding: 16px 24px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cyber-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  font-weight: bold;
}

.cyber-title i {
  color: #00ffff;
  font-size: 20px;
}

.status-indicators {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-dot.deepfake {
  background: #FF6B6B;
}

.status-dot.authentic {
  background: #51CF66;
}

.status-dot.loading {
  background: #FFD93D;
}

.status-text {
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-dot.deepfake + .status-text {
  color: #FF6B6B;
}

.status-dot.authentic + .status-text {
  color: #51CF66;
}

.status-dot.loading + .status-text {
  color: #FFD93D;
}

/* Tabs */
.tabs-header {
  display: flex;
  gap: 0;
  margin: 0;
  padding: 0 24px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(0, 255, 255, 0.05);
}

.tab-btn {
  background: transparent;
  border: none;
  color: rgba(0, 255, 255, 0.6);
  padding: 12px 20px;
  cursor: pointer;
  font-size: 12px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  text-transform: uppercase;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.tab-btn:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.tab-btn.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.2);
  border-bottom: 2px solid #00ffff;
}

.tab-btn i {
  margin-right: 8px;
}

.tabs-content {
  padding: 24px;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

/* Prediction Card */
.prediction-card {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.prediction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
}

.prediction-header h3 {
  margin: 0;
  color: #00ffff;
  font-size: 16px;
}

.prediction-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
}

.prediction-badge.deepfake {
  background: rgba(255, 107, 107, 0.2);
  color: #FF6B6B;
  border: 1px solid #FF6B6B;
}

.prediction-badge.authentic {
  background: rgba(81, 207, 102, 0.2);
  color: #51CF66;
  border: 1px solid #51CF66;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.detail-row .label {
  color: rgba(0, 255, 255, 0.7);
}

.detail-row .value {
  color: #00ffff;
  font-weight: bold;
}

.risk-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
}

.risk-badge.high {
  background: rgba(255, 107, 107, 0.2);
  color: #FF6B6B;
  border: 1px solid #FF6B6B;
}

.risk-badge.medium {
  background: rgba(255, 217, 61, 0.2);
  color: #FFD93D;
  border: 1px solid #FFD93D;
}

.risk-badge.low {
  background: rgba(81, 207, 102, 0.2);
  color: #51CF66;
  border: 1px solid #51CF66;
}

/* Consistency Summary */
.consistency-summary h3 {
  color: #00ffff;
  margin-bottom: 16px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.consistency-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.consistency-item {
  padding: 16px;
  border-radius: 8px;
  background: rgba(10, 14, 42, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.item-header i {
  font-size: 18px;
  color: #00ffff;
}

.item-header .name {
  font-size: 12px;
  color: rgba(0, 255, 255, 0.8);
  font-weight: 600;
  text-transform: uppercase;
}

.bar-container {
  height: 6px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.consistency-item.audio .bar {
  background: linear-gradient(90deg, #FF6B6B, #FF8E8E);
}

.consistency-item.video .bar {
  background: linear-gradient(90deg, #4ECDC4, #67DCD2);
}

.consistency-item.cross .bar {
  background: linear-gradient(90deg, #FFD93D, #FFE66D);
}

.consistency-info .score {
  font-size: 14px;
  font-weight: bold;
  color: #00ffff;
}

/* Temporal Analysis */
.temporal-container h3 {
  color: #00ffff;
  margin-bottom: 8px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.description {
  color: rgba(0, 255, 255, 0.7);
  font-size: 12px;
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
  color: #00ffff;
  margin: 0;
  font-size: 13px;
  text-transform: uppercase;
}

.anomaly-count {
  background: rgba(255, 107, 107, 0.2);
  color: #FF6B6B;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: bold;
  border: 1px solid #FF6B6B;
}

.temporal-chart {
  max-height: 300px;
  margin-bottom: 8px;
  background: rgba(10, 14, 42, 0.5);
  border-radius: 8px;
  padding: 12px;
}

.chart-desc {
  font-size: 11px;
  color: rgba(0, 255, 255, 0.5);
  margin: 0;
  text-transform: uppercase;
}

/* Anomaly Detection */
.anomaly-container h3 {
  color: #00ffff;
  margin-bottom: 20px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.severity-indicator {
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  font-weight: bold;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.severity-indicator.high {
  background: rgba(255, 107, 107, 0.1);
  color: #FF6B6B;
  border-color: #FF6B6B;
}

.severity-indicator.medium {
  background: rgba(255, 217, 61, 0.1);
  color: #FFD93D;
  border-color: #FFD93D;
}

.severity-indicator.low {
  background: rgba(81, 207, 102, 0.1);
  color: #51CF66;
  border-color: #51CF66;
}

.severity-indicator i {
  font-size: 20px;
}

.severity-info {
  display: flex;
  gap: 8px;
  align-items: center;
}

.severity-info .label {
  font-size: 12px;
  opacity: 0.8;
}

.severity-info .value {
  font-size: 14px;
  text-transform: uppercase;
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
  background: rgba(10, 14, 42, 0.5);
  text-align: center;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 12px;
}

.stat-header i {
  color: #00ffff;
  font-size: 16px;
}

.stat-card h4 {
  margin: 0;
  color: rgba(0, 255, 255, 0.8);
  font-size: 11px;
  text-transform: uppercase;
}

.stat-card .count {
  font-size: 28px;
  font-weight: bold;
  color: #00ffff;
  margin-bottom: 8px;
}

.stat-card p {
  margin: 0;
  font-size: 11px;
  color: rgba(0, 255, 255, 0.5);
  text-transform: uppercase;
}

.stat-card.audio {
  border-left: 4px solid #FF6B6B;
}

.stat-card.video {
  border-left: 4px solid #4ECDC4;
}

.stat-card.combined {
  border-left: 4px solid #FFD93D;
}

.anomaly-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.anomaly-list {
  padding: 16px;
  border-radius: 8px;
  background: rgba(10, 14, 42, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.list-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.list-header i {
  color: #00ffff;
  font-size: 16px;
}

.anomaly-list h4 {
  margin: 0;
  color: #00ffff;
  font-size: 12px;
  text-transform: uppercase;
}

.frame-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.frame-badge {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  color: #00ffff;
  text-transform: uppercase;
}

/* Technical Details */
.technical-container h3 {
  color: #00ffff;
  margin-bottom: 20px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.technical-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.section-header i {
  color: #00ffff;
  font-size: 16px;
}

.section-header h4 {
  margin: 0;
  color: #00ffff;
  font-size: 12px;
  text-transform: uppercase;
}

.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-list li {
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  font-size: 12px;
  color: rgba(0, 255, 255, 0.8);
}

.tech-list li:last-child {
  border-bottom: none;
}

.tech-list strong {
  color: #00ffff;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

/* Responsive */
@media (max-width: 768px) {
  .cyber-explainability {
    padding: 0;
  }

  .tabs-header {
    flex-wrap: wrap;
  }

  .tab-btn {
    font-size: 11px;
    padding: 10px 16px;
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