<template>
  <div
    class="relative flex h-auto min-h-screen w-full flex-col dark group/design-root overflow-x-hidden cyber-theme"
    style='font-family: "Orbitron", "Space Grotesk", "Noto Sans", sans-serif;'
  >
    <!-- Cyber Background Overlay -->
    <div class="fixed inset-0 z-0 cyber-bg">
      <div class="absolute inset-0 bg-gradient-to-br from-[#0a0e2a] via-[#1a103d] to-[#0a0e2a]"></div>
      <div class="absolute inset-0 cyber-grid"></div>
      <div class="absolute inset-0 cyber-scanlines"></div>
    </div>

    <!-- Uniform wrapper: centers all content with consistent width/padding -->
    <div class="w-full flex justify-center relative z-10">
      <div class="w-full max-w-[1200px] px-4 sm:px-6 flex flex-col flex-1 py-3 sm:py-5">
        <!-- Cyber Header -->
        <div class="flex justify-between items-center mb-6 cyber-border-bottom">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-[#00ffff] rounded-full flex items-center justify-center">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 7L12 12L22 7" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 22V12" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h1 class="text-[#00ffff] text-lg font-bold tracking-wider">DeepDrishti</h1>
          </div>
          <div class="flex gap-2">
            <div class="w-3 h-3 bg-red-500 rounded-full cyber-pulse"></div>
            <div class="w-3 h-3 bg-yellow-500 rounded-full cyber-pulse" style="animation-delay: 0.2s"></div>
            <div class="w-3 h-3 bg-green-500 rounded-full cyber-pulse" style="animation-delay: 0.4s"></div>
          </div>
        </div>
       <!-- Cyber Header -->
<div class="flex justify-between items-center mb-6 cyber-border-bottom">
  <!-- header content -->
</div>

        <div>
          <div class="sm:p-4">
            <div
              class="flex min-h-[200px] sm:min-h-[280px] md:min-h-[320px] lg:min-h-[400px] xl:min-h-[480px] flex-col gap-4 sm:gap-6 md:gap-8 sm:rounded-xl items-center justify-center p-3 sm:p-4 md:p-6 cyber-card"
            >
              <div class="text-center">
                <h1
                  class="text-[#00ffff] text-xl sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl font-black leading-tight tracking-[-0.033em] sm:text-5xl px-2 sm:px-4 cyber-text-glow"
                >
                  DEEPFAKE DETECTOR
                </h1>
                <p class="text-[#8dcece] mt-2 text-sm sm:text-base">
                  VERIFY AUTHENTICITY IN SECONDS
                </p>
              </div>
              <button
                @click="scrollToDetection"
                class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 md:h-12 px-3 sm:px-4 md:px-5 bg-[#00ffff] text-[#0f2424] text-xs sm:text-sm md:text-base font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button"
              >
                <span class="truncate">▶ START ANALYSIS</span>
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3 mb-4">
          <div class="w-6 h-6 bg-[#00ffff] rounded-full flex items-center justify-center">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="text-[#00ffff] text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em]">
            DETECTION TOOL
          </h2>
        </div>

        <!-- Detection Mode Tabs -->
        <div class="flex gap-2 sm:gap-4 py-2 border-b border-[#2e6b6b] cyber-tabs">
          <button
            @click="detectionMode = 'upload'"
            :class="['px-3 sm:px-4 py-2 text-sm font-medium rounded-t-lg transition-all duration-200 cyber-tab', detectionMode === 'upload' ? 'active' : '']"
          >
            📁 UPLOAD VIDEO
          </button>
          <button
            @click="detectionMode = 'url'"
            :class="['px-3 sm:px-4 py-2 text-sm font-medium rounded-t-lg transition-all duration-200 cyber-tab', detectionMode === 'url' ? 'active' : '']"
          >
            🔗 VIDEO URL
          </button>
        </div>

        <div class="flex flex-col p-3 sm:p-4">
          <!-- Upload Mode -->
          <div v-show="detectionMode === 'upload'">
            <div v-if="!fileUploaded"
              class="flex flex-col items-center gap-4 sm:gap-6 rounded-xl border-2 border-dashed border-[#2e6b6b] px-4 sm:px-6 py-6 sm:py-14 transition-all duration-300 hover:border-[#00ffff] cyber-upload-zone"
              @dragover.prevent
              @drop.prevent="handleFileDrop"
              @click="triggerFileInput"
            >
              <div class="flex max-w-[320px] sm:max-w-[480px] flex-col items-center gap-2">
                <div class="w-16 h-16 bg-[#00ffff] bg-opacity-20 rounded-full flex items-center justify-center border border-[#00ffff]">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M17 8L12 3L7 8" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 3V15" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p class="text-white text-base sm:text-lg font-bold leading-tight max-w-[320px] sm:max-w-[480px] text-center px-2">
                  {{ draggedOver ? 'RELEASE TO DROP YOUR VIDEO' : 'DRAG AND DROP A VIDEO HERE' }}
                </p>
                <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal max-w-[320px] sm:max-w-[480px] text-center px-2">
                  OR CLICK TO UPLOAD
                </p>
              </div>
              <button
                class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#204b4b] text-white text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
              >
                <span class="truncate">▶ UPLOAD VIDEO</span>
              </button>
              <input
                type="file"
                ref="fileInput"
                accept="video/mp4,video/avi,video/mov"
                @change="handleFileUpload"
                class="hidden"
              />
            </div>

            <div v-else class="flex flex-col items-center gap-4 rounded-xl border-2 border-[#00ffff] px-4 py-6 cyber-file-selected">
              <div class="w-full max-w-[480px] flex items-center gap-4">
                <div class="text-white text-sm font-medium truncate max-w-[200px]">
                  {{ file?.name }}
                </div>
                <div class="flex gap-2">
                  <button
                    @click="resetUpload"
                    class="flex min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                  >
                    <span class="truncate">✕ REMOVE</span>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="fileUploaded && !analysisComplete" class="flex flex-col gap-2 sm:gap-3 mt-4 cyber-analysis-status">
              <div class="flex gap-4 sm:gap-6 justify-between items-center">
                <p class="text-white text-sm sm:text-base font-medium leading-normal">
                  {{ isAnalyzing ? 'ANALYZING...' : 'READY TO ANALYZE' }}
                </p>
                <p class="text-[#00ffff] text-xs sm:text-sm font-medium leading-normal">
                  {{ isAnalyzing ? progress + '%' : 'CLICK ANALYZE TO START' }}
                </p>
              </div>
              <div class="rounded bg-[#2e6b6b] h-3 sm:h-2 cyber-progress-container">
                <div
                  class="h-full rounded bg-[#00ffff] transition-all duration-500 ease-out cyber-progress-bar"
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
              <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal">
                {{ isAnalyzing ? 'THIS MAY TAKE A FEW SECONDS' : 'ANALYSIS WILL START WHEN YOU CLICK THE BUTTON' }}
              </p>
            </div>

            <div v-if="fileUploaded && !analysisComplete" class="flex px-0 py-2 sm:py-3 justify-center mt-4">
              <button
                @click="startAnalysis"
                :disabled="isAnalyzing"
                class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#00ffff] text-[#0f2424] text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 disabled:opacity-70 disabled:cursor-not-allowed cyber-button"
              >
                <span class="truncate">
                  {{ isAnalyzing ? 'ANALYZING...' : '▶ ANALYZE' }}
                </span>
              </button>
            </div>

            <div v-if="analysisComplete && !showExplainability" class="p-3 sm:p-4 mt-4">
              <div
                class="bg-cover bg-center flex flex-col items-stretch justify-end rounded-xl pt-[100px] sm:pt-[120px] md:pt-[132px] cyber-result-card"
                :style="`background-image: linear-gradient(0deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0) 100%), url('${analysisImageUrl}');`"
              >
                <div
                  class="flex w-full items-end justify-between gap-2 sm:gap-4 p-3 sm:p-4 rounded-lg cyber-result-overlay"
                  :class="analysisResult === 'AUTHENTIC' ? 'bg-green-500/20' : 'bg-red-500/20'"
                >
                  <div class="flex-1">
                    <p
                      class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight"
                      :class="analysisResult === 'AUTHENTIC' ? 'text-green-400' : 'text-red-400'"
                    >
                      {{ analysisResult }}
                    </p>
                    <p class="text-[#070808] text-sm mt-1">
                      CONFIDENCE: {{ videoConfidence }}%
                    </p>
                  </div>
                  <button
                    @click="resetAnalysis"
                    class="flex min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                  >
                    <span class="truncate">↻ NEW ANALYSIS</span>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="analysisComplete && showExplainability" class="mt-6">
              <DeepfakeExplainability :result="explainabilityResult" />
              <div class="flex mt-6 justify-center gap-2 flex-col sm:flex-row">
                <button
                  @click="generatePDFReport('video')"
                  class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button"
                >
                  <span class="truncate">📄 PDF REPORT</span>
                </button>
                <button
                  @click="resetAnalysis"
                  class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                >
                  <span class="truncate">↻ ANALYZE ANOTHER VIDEO</span>
                </button>
              </div>
            </div>
          </div>

          <!-- URL Mode -->
          <div v-show="detectionMode === 'url'" class="w-full">
            <div class="flex flex-col gap-4">
              <p class="text-white text-sm font-medium">ENTER A VIDEO URL FROM SUPPORTED PLATFORMS:</p>
              <div class="flex gap-2">
                <input
                  v-model="videoUrl"
                  type="url"
                  placeholder="https://www.youtube.com/watch?v=... or https://www.instagram.com/p/..."
                  class="flex-1 px-4 py-2 rounded-lg bg-[#2e6b6b] text-white placeholder-[#8dcece] border border-[#204b4b] focus:border-[#00ffff] outline-none transition-colors cyber-input"
                />
                <button
                  @click="predictFromUrl"
                  :disabled="urlLoading || !videoUrl"
                  class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed cyber-button"
                >
                  <span class="truncate">{{ urlLoading ? 'PROCESSING...' : '▶ PREDICT' }}</span>
                </button>
              </div>
            </div>

            <div v-if="urlLoading" class="flex flex-col gap-3 mt-6">
              <div class="flex gap-4 justify-between items-center">
                <p class="text-white text-sm font-medium">DOWNLOADING AND ANALYZING...</p>
                <p class="text-[#00ffff] text-xs font-medium">{{ progress }}%</p>
              </div>
              <div class="rounded bg-[#2e6b6b] h-2 cyber-progress-container">
                <div
                  class="h-full rounded bg-[#00ffff] transition-all duration-500 ease-out cyber-progress-bar"
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
            </div>

            <div v-if="analysisComplete && showExplainability && detectionMode === 'url'" class="mt-6">
              <DeepfakeExplainability :result="explainabilityResult" />
              <div class="flex mt-6 justify-center gap-2 flex-col sm:flex-row">
                <button
                  @click="generatePDFReport('video')"
                  class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button"
                >
                  <span class="truncate">📄 PDF REPORT</span>
                </button>
                <button
                  @click="resetUrl"
                  class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                >
                  <span class="truncate">↻ ANALYZE ANOTHER URL</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Image Upload Section -->
        <div class="flex items-center gap-3 mb-4 mt-8">
          <div class="w-6 h-6 bg-[#00ffff] rounded-full flex items-center justify-center">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="text-[#00ffff] text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em]">
            IMAGE UPLOAD
          </h2>
        </div>

        <!-- Image Detection Mode Tabs -->
        <div class="flex gap-2 sm:gap-4 py-2 border-b border-[#2e6b6b] cyber-tabs">
          <button
            @click="imageDetectionMode = 'upload'"
            :class="['px-3 sm:px-4 py-2 text-sm font-medium rounded-t-lg transition-all duration-200 cyber-tab', imageDetectionMode === 'upload' ? 'active' : '']"
          >
            📁 UPLOAD IMAGE
          </button>
          <button
            @click="imageDetectionMode = 'url'"
            :class="['px-3 sm:px-4 py-2 text-sm font-medium rounded-t-lg transition-all duration-200 cyber-tab', imageDetectionMode === 'url' ? 'active' : '']"
          >
            🔗 IMAGE URL
          </button>
        </div>

        <div class="flex flex-col p-3 sm:p-4">
          <!-- Image Upload Mode -->
          <div v-show="imageDetectionMode === 'upload'">
          <div
            v-if="!imageUploaded"
            class="flex flex-col items-center gap-4 sm:gap-6 rounded-xl border-2 border-dashed border-[#2e6b6b] px-4 sm:px-6 py-6 sm:py-14 transition-all duration-300 hover:border-[#00ffff] cyber-upload-zone"
            @dragover.prevent="imagesDraggedOver = true"
            @dragleave.prevent="imagesDraggedOver = false"
            @drop.prevent="handleImageDrop"
            @click="triggerImageFileInput"
          >
            <div class="flex max-w-[320px] sm:max-w-[480px] flex-col items-center gap-2">
              <div class="w-16 h-16 bg-[#00ffff] bg-opacity-20 rounded-full flex items-center justify-center border border-[#00ffff]">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M17 8L12 3L7 8" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 3V15" stroke="#00ffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <p class="text-white text-base sm:text-lg font-bold leading-tight max-w-[320px] sm:max-w-[480px] text-center px-2">
                {{ imagesDraggedOver ? 'RELEASE TO DROP YOUR IMAGE' : 'DRAG AND DROP AN IMAGE HERE' }}
              </p>
              <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal max-w-[320px] sm:max-w-[480px] text-center px-2">
                OR CLICK TO UPLOAD (JPG, PNG, WebP)
              </p>
            </div>
            <button
              class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#204b4b] text-white text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
            >
              <span class="truncate">▶ UPLOAD IMAGE</span>
            </button>
            <input
              type="file"
              ref="imageFileInput"
              accept="image/jpeg,image/png,image/webp"
              @change="handleImageFileUpload"
              class="hidden"
            />
          </div>

          <div v-else class="flex flex-col gap-4 rounded-xl border-2 border-[#00ffff] px-4 py-6 cyber-file-selected">
            <div class="flex flex-col sm:flex-row items-center gap-4">
              <img
                :src="imagePreviewUrl"
                :alt="image?.name"
                class="w-full sm:w-48 h-auto sm:h-48 object-cover rounded-lg border border-[#2e6b6b]"
              />
              <div class="flex-1 flex flex-col gap-3">
                <div class="text-white text-sm font-medium break-all">
                  {{ image?.name }}
                </div>
                <div class="text-[#8dcece] text-xs">
                  SIZE: {{ ((image?.size ?? 0) / 1024 / 1024).toFixed(2) }} MB
                </div>
                <div class="flex gap-2">
                  <button
                    @click="resetImageUpload"
                    class="flex min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                  >
                    <span class="truncate">✕ REMOVE</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

        <div v-if="imageUploaded && !imageAnalysisComplete" class="flex flex-col gap-2 sm:gap-3 p-3 sm:p-4 cyber-analysis-status">
          <div class="flex gap-4 sm:gap-6 justify-between items-center">
            <p class="text-white text-sm sm:text-base font-medium leading-normal">
              {{ isImageAnalyzing ? 'PROCESSING...' : 'READY TO PROCESS' }}
            </p>
            <p class="text-[#00ffff] text-xs sm:text-sm font-medium leading-normal">
              {{ isImageAnalyzing ? imageProgress + '%' : 'CLICK PROCESS TO START' }}
            </p>
          </div>
          <div class="rounded bg-[#2e6b6b] h-3 sm:h-2 cyber-progress-container">
            <div
              class="h-full rounded bg-[#00ffff] transition-all duration-500 ease-out cyber-progress-bar"
              :style="{ width: imageProgress + '%' }"
            ></div>
          </div>
          <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal">
            {{ isImageAnalyzing ? 'PROCESSING IMAGE...' : 'READY TO PROCESS IMAGE' }}
          </p>
        </div>

        <div v-if="imageUploaded && !imageAnalysisComplete" class="flex py-2 sm:py-3 justify-center">
          <button
            @click="startImageAnalysis"
            :disabled="isImageAnalyzing"
            class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#00ffff] text-[#0f2424] text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 disabled:opacity-70 disabled:cursor-not-allowed cyber-button"
          >
            <span class="truncate">
              {{ isImageAnalyzing ? 'PROCESSING...' : '▶ PROCESS IMAGE' }}
            </span>
          </button>
        </div>

        <div v-if="imageAnalysisComplete" class="p-3 sm:p-4">
          <div class="flex flex-col gap-4 rounded-xl border-2 border-[#2e6b6b] bg-[#173636] p-4 sm:p-6 cyber-result-card">
            <div class="flex flex-col sm:flex-row gap-4 items-start">
              <div class="flex flex-col gap-4 items-center w-full sm:w-auto">
                <img
                  :src="imagePreviewUrl"
                  :alt="image?.name"
                  class="w-full sm:w-48 h-auto sm:h-48 object-cover rounded-lg border border-[#2e6b6b]"
                />
                <div v-if="imageHeatmapBase64" class="w-full sm:w-48">
                  <p class="text-[#8dcece] text-xs font-bold mb-2 uppercase tracking-wider">Grad-CAM Heatmap</p>
                  <img
                    :src="imageHeatmapBase64"
                    alt="Grad-CAM Heatmap"
                    class="w-full h-auto object-cover rounded-lg border border-[#00ffff]"
                  />
                </div>
              </div>
              <div class="flex-1 flex flex-col gap-4">
                <div>
                  <p
                    class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight mb-2"
                    :class="imageAnalysisResult === 'AUTHENTIC' ? 'text-green-400' : 'text-red-400'"
                  >
                    {{ imageAnalysisResult }}
                  </p>
                  <p class="text-[#8dcece] text-sm">
                    CONFIDENCE: {{ imageConfidence }}%
                  </p>
                </div>
                <div class="bg-[#204b4b] rounded-lg p-4 border border-[#2e6b6b]">
                  <h3 class="text-white text-sm font-bold mb-2">EXPLANATION ANALYSIS</h3>
                  <p class="text-[#8dcece] text-xs mb-3 italic">"{{ imageExplanationText }}"</p>
                  
                  <div v-if="imageRegionScores" class="space-y-3 mb-3">
                    <div v-for="(score, region) in imageRegionScores" :key="region" class="flex flex-col gap-1">
                      <div class="flex justify-between text-[10px] text-[#8dcece] uppercase tracking-wider">
                        <span>{{ region }}</span>
                        <span>{{ (score * 100).toFixed(1) }}%</span>
                      </div>
                      <div class="h-1.5 bg-[#0a0e2a] rounded-full overflow-hidden">
                        <div class="h-full bg-[#00ffff] rounded-full transition-all duration-500" :style="{ width: (score * 100) + '%' }"></div>
                      </div>
                    </div>
                  </div>

                  <div v-if="imageDominantFocusRegion" class="flex items-center gap-2 text-xs font-bold text-white border-t border-[#2e6b6b] pt-2 mt-2">
                    <span class="text-[#8dcece]">DOMINANT REGION:</span>
                    <span class="text-[#00ffff] uppercase">{{ imageDominantFocusRegion }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex gap-2 w-full sm:w-auto flex-col sm:flex-row">
              <button
                @click="generatePDFReport('image')"
                class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button"
              >
                <span class="truncate">📄 PDF REPORT</span>
              </button>
              <button
                @click="resetImageAnalysis"
                class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
              >
                <span class="truncate">↻ NEW ANALYSIS</span>
              </button>
            </div>
          </div>
        </div>
        </div>

        <!-- Image URL Mode -->
          <div v-show="imageDetectionMode === 'url'" class="w-full">
            <div class="flex flex-col gap-4">
              <p class="text-white text-sm font-medium">ENTER AN IMAGE URL:</p>
              <div class="flex gap-2">
                <input
                  v-model="imageUrl"
                  type="url"
                  placeholder="https://example.com/image.jpg"
                  class="flex-1 px-4 py-2 rounded-lg bg-[#2e6b6b] text-white placeholder-[#8dcece] border border-[#204b4b] focus:border-[#00ffff] outline-none transition-colors cyber-input"
                />
                <button
                  @click="predictImageFromUrl"
                  :disabled="imageUrlLoading || !imageUrl"
                  class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed cyber-button"
                >
                  <span class="truncate">{{ imageUrlLoading ? 'PROCESSING...' : '▶ PREDICT' }}</span>
                </button>
              </div>
            </div>

            <div v-if="imageUrlLoading" class="flex flex-col gap-3 mt-6">
              <div class="flex gap-4 justify-between items-center">
                <p class="text-white text-sm font-medium">DOWNLOADING AND ANALYZING...</p>
                <p class="text-[#00ffff] text-xs font-medium">{{ imageProgress }}%</p>
              </div>
              <div class="rounded bg-[#2e6b6b] h-2 cyber-progress-container">
                <div
                  class="h-full rounded bg-[#00ffff] transition-all duration-500 ease-out cyber-progress-bar"
                  :style="{ width: imageProgress + '%' }"
                ></div>
              </div>
            </div>

            <div v-if="imageAnalysisComplete && imageDetectionMode === 'url'" class="mt-6">
              <div class="flex flex-col gap-4 rounded-xl border-2 border-[#2e6b6b] bg-[#173636] p-4 sm:p-6 cyber-result-card">
                 <div class="flex flex-col sm:flex-row gap-4 items-start">
                  <div class="flex flex-col gap-4 items-center w-full sm:w-auto">
                    <div class="w-full sm:w-48">
                      <p class="text-[#8dcece] text-xs font-bold mb-2 uppercase tracking-wider">Original Image</p>
                      <img
                        :src="imageOriginalUrl"
                        class="w-full h-auto object-cover rounded-lg border border-[#2e6b6b]"
                      />
                    </div>
                    <div v-if="imageHeatmapBase64" class="w-full sm:w-48">
                      <p class="text-[#8dcece] text-xs font-bold mb-2 uppercase tracking-wider">Grad-CAM Heatmap</p>
                      <img
                        :src="imageHeatmapBase64"
                        alt="Grad-CAM Heatmap"
                        class="w-full h-auto object-cover rounded-lg border border-[#00ffff]"
                      />
                    </div>
                  </div>
                  <div class="flex-1 flex flex-col gap-4">
                    <div>
                      <p
                        class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight mb-2"
                        :class="imageAnalysisResult === 'AUTHENTIC' ? 'text-green-400' : 'text-red-400'"
                      >
                        {{ imageAnalysisResult }}
                      </p>
                      <p class="text-[#8dcece] text-sm">
                        CONFIDENCE: {{ imageConfidence }}%
                      </p>
                    </div>
                    <div class="bg-[#204b4b] rounded-lg p-4 border border-[#2e6b6b] w-full">
                      <h3 class="text-white text-sm font-bold mb-2">EXPLANATION ANALYSIS</h3>
                      <p class="text-[#8dcece] text-xs mb-3 italic">"{{ imageExplanationText }}"</p>
                      
                      <div v-if="imageRegionScores" class="space-y-3 mb-3">
                        <div v-for="(score, region) in imageRegionScores" :key="region" class="flex flex-col gap-1">
                          <div class="flex justify-between text-[10px] text-[#8dcece] uppercase tracking-wider">
                            <span>{{ region }}</span>
                            <span>{{ (score * 100).toFixed(1) }}%</span>
                          </div>
                          <div class="h-1.5 bg-[#0a0e2a] rounded-full overflow-hidden">
                            <div class="h-full bg-[#00ffff] rounded-full transition-all duration-500" :style="{ width: (score * 100) + '%' }"></div>
                          </div>
                        </div>
                      </div>

                      <div v-if="imageDominantFocusRegion" class="flex items-center gap-2 text-xs font-bold text-white border-t border-[#2e6b6b] pt-2 mt-2">
                        <span class="text-[#8dcece]">DOMINANT REGION:</span>
                        <span class="text-[#00ffff] uppercase">{{ imageDominantFocusRegion }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="flex mt-6 justify-center gap-2 flex-col sm:flex-row">
                  <button
                    @click="generatePDFReport('image')"
                    class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#00ffff] text-[#0f2424] text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button"
                  >
                    <span class="truncate">📄 PDF REPORT</span>
                  </button>
                  <button
                    @click="resetImageUrl"
                    class="flex flex-1 sm:flex-none min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 cyber-button-secondary"
                  >
                    <span class="truncate">↻ ANALYZE ANOTHER URL</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3 mb-4 mt-8">
          <div class="w-6 h-6 bg-[#00ffff] rounded-full flex items-center justify-center">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="text-[#00ffff] text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em]">
            HOW IT WORKS
          </h2>
        </div>

        <div class="grid grid-cols-[repeat(auto-fit,minmax(140px,1fr))] gap-2 sm:gap-3 p-3 sm:p-4">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="flex flex-1 gap-2 sm:gap-3 rounded-lg border border-[#2e6b6b] bg-[#173636] p-3 sm:p-4 items-center transition-all duration-300 hover:border-[#00ffff] cyber-step"
            :class="{ 'border-[#00ffff]': currentStep === index + 1 }"
          >
            <div
              class="text-white"
              :data-icon="step.icon"
              :data-size="'20px'"
              data-weight="regular"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                :width="currentStep === index + 1 ? '28px' : '20px'"
                :height="currentStep === index + 1 ? '28px' : '20px'"
                fill="currentColor"
                :viewBox="currentStep === index + 1 ? '0 0 256 256' : '0 0 256 256'"
                class="transition-all duration-300"
              >
                <path :d="step.icon === 'FilmSlate' ? 'M216,104H102.09L210,75.51a8,8,0,0,0,5.68-9.84l-8.16-30a15.93,15.93,0,0,0-19.42-11.13L35.81,64.74a15.75,15.75,0,0,0-9.7,7.4,15.51,15.51,0,0,0-1.55,12L32,111.56c0,.14,0,.29,0,.44v88a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V112A8,8,0,0,0,216,104ZM192.16,40l6,22.07-22.62,6L147.42,51.83Zm-66.69,17.6,28.12,16.24-36.94,9.75L88.53,67.37Zm-79.4,44.62-6-22.08,26.5-7L94.69,89.4ZM208,200H48V120H208v80Z' : step.icon === 'Play' ? 'M232.4,114.49,88.32,26.35a16,16,0,0,0-16.2-.3A15.86,15.86,0,0,0,64,39.87V216.13A15.94,15.94,0,0,0,80,232a16.07,16.07,0,0,0,8.36-2.35L232.4,141.51a15.81,15.81,0,0,0,0-27ZM80,215.94V40l143.83,88Z' : 'M200,48H136V16a8,8,0,0,0-16,0V48H56A32,32,0,0,0,24,80V192a32,32,0,0,0,32,32H200a32,32,0,0,0,32-32V80A32,32,0,0,0,200,48Zm16,144a16,16,0,0,1-16,16H56a16,16,0,0,1-16-16V80A16,16,0,0,1,56,64H200a16,16,0,0,1,16,16Zm-52-56H92a28,28,0,0,0,0,56h72a28,28,0,0,0,0-56Zm-28,16v24H120V152ZM80,164a12,12,0,0,1,12-12h12v24H92A12,12,0,0,1,80,164Zm84,12H152V152h12a12,12,0,0,1,0,24ZM72,108a12,12,0,1,1,12,12A12,12,0,0,1,72,108Zm88,0a12,12,0,1,1,12,12A12,12,0,0,1,160,108Z'" />
              </svg>
            </div>
            <h2 class="text-white text-xs sm:text-base font-bold leading-tight">{{ step.title }}</h2>
          </div>
        </div>

        <div class="flex items-center gap-3 mb-4 mt-8">
          <div class="w-6 h-6 bg-[#00ffff] rounded-full flex items-center justify-center">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="text-[#00ffff] text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em]">
            WHY CHOOSE US
          </h2>
        </div>

        <div class="flex flex-wrap gap-3 sm:gap-4 p-3 sm:p-4">
          <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105 cyber-stat-card">
            <p class="text-[#8dcece] text-xs sm:text-sm font-medium leading-normal">F1-SCORE</p>
            <p class="text-[#00ffff] tracking-light text-xl sm:text-2xl font-bold leading-tight">90%</p>
          </div>
          <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105 cyber-stat-card">
            <p class="text-[#8dcece] text-xs sm:text-sm font-medium leading-normal">ACCURACY</p>
            <p class="text-[#00ffff] tracking-light text-xl sm:text-2xl font-bold leading-tight">91.5%</p>
          </div>
          <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105 cyber-stat-card">
            <p class="text-[#8dcece] text-xs sm:text-sm font-medium leading-normal">PROCESSING</p>
            <p class="text-[#00ffff] tracking-light text-xl sm:text-2xl font-bold leading-tight">&lt; 50s</p>
          </div>
        </div>

        <p class="text-[#8dcece] text-sm sm:text-base font-normal leading-normal pb-3 sm:pb-5 pt-2 sm:pt-3 text-center">AUDIO-VISUAL SYNCHRONIZATION ANALYSIS</p>

        <div class="flex items-center gap-3 mb-4 mt-8">
          <div class="w-6 h-6 bg-[#00ffff] rounded-full flex items-center justify-center">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V17L12 22L22 17V7L12 2Z" stroke="#0a0e2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="text-[#00ffff] text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em]">
            FREQUENTLY ASKED QUESTIONS
          </h2>
        </div>

        <div class="flex flex-col p-3 sm:p-4 gap-2 sm:gap-3">
          <details
            v-for="(faq, index) in faqs"
            :key="index"
            class="flex flex-col rounded-xl bg-[#204b4b] px-3 sm:px-4 py-2 sm:py-3 group cyber-faq"
          >
            <summary class="flex cursor-pointer items-center justify-between gap-4 sm:gap-6 py-1 sm:py-2">
              <p class="text-white text-sm sm:text-base font-medium leading-normal">{{ faq.question }}</p>
              <div
                class="text-white group-open:rotate-180 transition-transform duration-300"
                data-icon="CaretDown"
                :data-size="faq.open ? '24px' : '20px'"
                data-weight="regular"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  :width="faq.open ? '24px' : '20px'"
                  :height="faq.open ? '24px' : '20px'"
                  fill="currentColor"
                  viewBox="0 0 256 256"
                >
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </summary>
            <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal pb-2">
              {{ faq.answer }}
            </p>
          </details>
        </div>

        <footer class="flex flex-col gap-4 sm:gap-6 px-3 sm:px-5 py-6 sm:py-10 text-center cyber-footer">
          <div class="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
            <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300 cyber-footer-link">
              PRIVACY POLICY
            </button>
            <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300 cyber-footer-link">
              TERMS OF SERVICE
            </button>
            <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300 cyber-footer-link">
              CONTACT US
            </button>
          </div>
          <p class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal">© 2026 DEEPFAKE DETECTOR. ALL RIGHTS RESERVED.</p>
        </footer>
      </div>
    </div>

    <!-- Hidden PDF Report Template for Images -->
    <div id="imagePdfReport" style="display: none; background: white; padding: 40px; color: #000; font-family: Arial, sans-serif; min-width: 800px; max-width: 900px; margin: 0 auto;">
      <div style="text-align: center; margin-bottom: 30px; border-bottom: 3px solid #00ffff; padding-bottom: 20px;">
        <h1 style="margin: 0; font-size: 28px; color: #0a0e2a;">DEEPFAKE DETECTION REPORT</h1>
        <p style="margin: 10px 0 0 0; color: #666;">Analysis Report for Image Classification</p>
      </div>

      <div style="margin-bottom: 20px; font-size: 14px;">
        <p><strong>Report Date:</strong> {{ new Date().toLocaleString() }}</p>
        <p><strong>Source:</strong> {{ imageDetectionMode === 'url' ? (imageExplanationResult?.filename || imageUrl || 'N/A') : (image?.name || 'Image') }}</p>
        <p v-if="imageDetectionMode === 'upload'"><strong>File Size:</strong> {{ ((image?.size ?? 0) / 1024 / 1024).toFixed(2) }} MB</p>
        <p><strong>Analysis Model:</strong> ResNet50 + Grad-CAM Explainability</p>
      </div>

      <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin-top: 0; color: #0a0e2a;">CLASSIFICATION RESULT</h2>
        <p style="font-size: 24px; font-weight: bold; margin: 10px 0;" 
           :style="{ color: imageAnalysisResult === 'AUTHENTIC' ? '#22c55e' : '#ef4444' }">
          {{ imageAnalysisResult }}
        </p>
        <p style="margin: 10px 0; font-size: 14px;"><strong>Confidence Score:</strong> {{ imageConfidence }}%</p>
        <p style="margin: 10px 0; font-size: 14px;"><strong>Raw Score:</strong> {{ imageExplanationResult?.raw_score?.toFixed(4) ?? 'N/A' }}</p>
      </div>

      <!-- Original Image -->
      <div v-if="imagePreviewUrl || imageOriginalUrl" style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">{{ imageDetectionMode === 'url' ? 'SOURCE IMAGE' : 'UPLOADED IMAGE' }}</h3>
        <img :src="imageDetectionMode === 'url' ? imageOriginalUrl : imagePreviewUrl" style="max-width: 100%; height: auto; max-height: 300px; border: 2px solid #ddd; border-radius: 8px;">
      </div>

      <!-- Heatmap -->
      <div v-if="imageHeatmapBase64" style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">GRAD-CAM HEATMAP VISUALIZATION</h3>
        <p style="font-size: 12px; color: #666; margin: 0 0 10px 0;">Shows which regions influenced the model's decision</p>
        <img :src="imageHeatmapBase64" style="max-width: 100%; height: auto; max-height: 300px; border: 2px solid #ddd; border-radius: 8px;">
      </div>

      <!-- Region Scores -->
      <div v-if="imageRegionScores" style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">REGION-BASED ANALYSIS SCORES</h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <thead>
            <tr style="background: #f0f0f0;">
              <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Facial Region</th>
              <th style="padding: 10px; text-align: right; border: 1px solid #ddd; font-weight: bold;">Score</th>
              <th style="padding: 10px; text-align: right; border: 1px solid #ddd; font-weight: bold;">Percentage</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(score, region) in imageRegionScores" :key="region">
              <td style="padding: 10px; border: 1px solid #ddd;">{{ region }}</td>
              <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{{ score.toFixed(4) }}</td>
              <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{{ (score * 100).toFixed(2) }}%</td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top: 10px; font-size: 14px;"><strong>Dominant Focus Region:</strong> {{ imageDominantFocusRegion }}</p>
      </div>

      <!-- Explanation -->
      <div v-if="imageExplanationText" style="background: #f9f9f9; padding: 15px; border-left: 4px solid #00ffff; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #0a0e2a; font-size: 16px;">DETAILED EXPLANATION</h3>
        <p style="margin: 0; line-height: 1.6; color: #333; font-size: 13px;">{{ imageExplanationText }}</p>
      </div>

      <!-- Footer -->
      <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center;">
        <p style="margin: 5px 0;">Generated by: Deepfake Detection System v1.0</p>
        <p style="margin: 5px 0;">Report ID: {{ imageExplanationResult?.filename || 'N/A' }}</p>
        <p style="margin: 5px 0;">For inquiries or questions, contact support.</p>
      </div>
    </div>

    <!-- Hidden PDF Report Template for Videos -->
    <div id="videoPdfReport" style="display: none; background: white; padding: 40px; color: #000; font-family: Arial, sans-serif; min-width: 800px; max-width: 900px; margin: 0 auto;">
      <div style="text-align: center; margin-bottom: 30px; border-bottom: 3px solid #00ffff; padding-bottom: 20px;">
        <h1 style="margin: 0; font-size: 28px; color: #0a0e2a;">DEEPFAKE DETECTION REPORT</h1>
        <p style="margin: 10px 0 0 0; color: #666;">Analysis Report for Video Classification</p>
      </div>

      <div style="margin-bottom: 20px; font-size: 14px;">
        <p><strong>Report Date:</strong> {{ new Date().toLocaleString() }}</p>
        <p><strong>File Name:</strong> {{ file?.name || videoUrl || 'Video' }}</p>
        <p v-if="file"><strong>File Size:</strong> {{ ((file?.size ?? 0) / 1024 / 1024).toFixed(2) }} MB</p>
        <p><strong>Analysis Model:</strong> Multi-Modal Deepfake Detector (Audio-Visual)</p>
      </div>

      <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin-top: 0; color: #0a0e2a;">CLASSIFICATION RESULT</h2>
        <p style="font-size: 24px; font-weight: bold; margin: 10px 0;" 
           :style="{ color: analysisResult === 'AUTHENTIC' ? '#22c55e' : '#ef4444' }">
          {{ analysisResult }}
        </p>
        <p style="margin: 10px 0; font-size: 14px;"><strong>Confidence Score:</strong> {{ videoConfidence }}%</p>
      </div>

      <!-- Video Thumbnail -->
      <div v-if="analysisImageUrl" style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">VIDEO FRAME</h3>
        <img :src="analysisImageUrl" style="max-width: 100%; height: auto; max-height: 300px; border: 2px solid #ddd; border-radius: 8px;">
      </div>

      <!-- Explainability Data -->
      <div v-if="explainabilityResult" style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">ANALYSIS DETAILS</h3>
        <div style="background: #f9f9f9; padding: 15px; border-left: 4px solid #00ffff;">
          <p style="margin: 5px 0; font-size: 13px;"><strong>Detection Method:</strong> Audio-Visual Synchronization Analysis</p>
          <p style="margin: 5px 0; font-size: 13px;"><strong>Model:</strong> Multi-Modal Deep Learning</p>
          <p style="margin: 5px 0; font-size: 13px;"><strong>Features Analyzed:</strong> Facial movements, audio patterns, temporal consistency</p>
        </div>
      </div>

      <!-- Technical Details -->
      <div style="margin-bottom: 20px;">
        <h3 style="color: #0a0e2a; margin-bottom: 10px; font-size: 16px;">TECHNICAL SUMMARY</h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <thead>
            <tr style="background: #f0f0f0;">
              <th style="padding: 10px; text-align: left; border: 1px solid #ddd; font-weight: bold;">Analysis Metric</th>
              <th style="padding: 10px; text-align: right; border: 1px solid #ddd; font-weight: bold;">Result</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 10px; border: 1px solid #ddd;">Prediction</td>
              <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{{ analysisResult }}</td>
            </tr>
            <tr>
              <td style="padding: 10px; border: 1px solid #ddd;">Confidence</td>
              <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{{ videoConfidence }}%</td>
            </tr>
            <tr>
              <td style="padding: 10px; border: 1px solid #ddd;">Processing Time</td>
              <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">< 10 seconds</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Explanation -->
      <div style="background: #f9f9f9; padding: 15px; border-left: 4px solid #00ffff; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #0a0e2a; font-size: 16px;">ANALYSIS EXPLANATION</h3>
        <p style="margin: 0; line-height: 1.6; color: #333; font-size: 13px;">
          The video was analyzed using a multi-modal deep learning model that examines both visual and audio features. 
          The system checks for inconsistencies in facial movements, audio-visual synchronization, temporal coherence, 
          and other deepfake artifacts. The confidence score reflects the model's certainty in its prediction based on 
          these comprehensive analyses.
        </p>
      </div>

      <!-- Footer -->
      <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center;">
        <p style="margin: 5px 0;">Generated by: Deepfake Detection System v1.0</p>
        <p style="margin: 5px 0;">Report ID: {{ file?.name || videoUrl || new Date().getTime() }}</p>
        <p style="margin: 5px 0;">For inquiries or questions, contact support.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import DeepfakeExplainability from './components/DeepfakeExplainability.vue';

// Vanta.NET background initialization
onMounted(() => {
  // Declare the global VANTA object from CDN
  const VANTA = (window as any).VANTA;
  if (VANTA) {
    VANTA.NET({
      el: '#app',
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x00ffff,       // Cyan net color
      backgroundColor: 0x0a0e2a,  // Dark blue background
      points: 12,
      maxDistance: 25,
      spacing: 18,
      showDots: true
    });
  }
});

// State variables
const fileInput = ref<HTMLInputElement | null>(null);
const file = ref<File | null>(null);
const fileUploaded = ref(false);
const isAnalyzing = ref(false);
const analysisComplete = ref(false);
const analysisResult = ref<'AUTHENTIC' | 'DEEPFAKE'>('AUTHENTIC');
const videoConfidence = ref(0);
const progress = ref(0);
const currentStep = ref(0);
const draggedOver = ref(false);
const analysisImageUrl = ref('');

// URL Prediction
const videoUrl = ref('');
const urlLoading = ref(false);

// Explainability
const showExplainability = ref(false);
const explainabilityResult = ref<any>(null);
const detectionMode = ref<'upload' | 'url'>('upload');

// Image Explainability
const showImageExplainability = ref(false);
const imageExplanationText = ref('');
const imageHeatmapBase64 = ref('');
const imageDominantFocusRegion = ref('');
const imageRegionScores = ref<Record<string, number> | null>(null);
const imageExplanationResult = ref<any>(null);


// Image upload state variables
const imageFileInput = ref<HTMLInputElement | null>(null);
const image = ref<File | null>(null);
const imageUploaded = ref(false);
const isImageAnalyzing = ref(false);
const imageAnalysisComplete = ref(false);
const imageAnalysisResult = ref<'AUTHENTIC' | 'DEEPFAKE'>('AUTHENTIC');
const imageProgress = ref(0);
const imagesDraggedOver = ref(false);
const imagePreviewUrl = ref('');
const imageConfidence = ref(0);
const imageDetectionMode = ref<'upload' | 'url'>('upload');
const imageUrl = ref('');
const imageUrlLoading = ref(false);
const imageOriginalUrl = ref(''); // Store original image URL separately from heatmap

// Steps for the process
const steps = [
  { title: 'EXTRACT FEATURES', icon: 'FilmSlate' },
  { title: 'ANALYZE SYNCHRONIZATION', icon: 'Play' },
  { title: 'PREDICT', icon: 'Robot' }
];

// FAQ data
const faqs = [
  {
    question: 'WHAT TYPES OF FILES CAN I UPLOAD?',
    answer: 'You can upload video files in MP4, AVI, and MOV formats. For URL detection, we support YouTube, Instagram, Facebook, TikTok, Twitter, and direct video links.',
    open: false
  },
  {
    question: 'HOW LONG DOES THE ANALYSIS TAKE?',
    answer: 'Video upload analysis typically completes within a few seconds to a minute depending on file size. URL downloads may take longer depending on video length.',
    open: false
  },
  {
    question: 'IS MY DATA SECURE?',
    answer: 'Files are processed locally in your browser. Temporary files downloaded from URLs are deleted immediately after analysis.',
    open: false
  },
  {
    question: 'WHAT IS EXPLAINABILITY?',
    answer: 'The explainability feature provides detailed temporal analysis showing frame-by-frame consistency scores, anomaly detection, and cross-modal audio-video synchronization analysis.',
    open: false
  }
];

// Methods
const scrollToDetection = () => {
  const detectionSection = document.querySelector('.cyber-tabs');
  if (detectionSection) {
    detectionSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0 && target.files[0]) {
    file.value = target.files[0];
    fileUploaded.value = true;
    progress.value = 0;
    analysisComplete.value = false;
    analysisResult.value = 'AUTHENTIC';
    showExplainability.value = false;
  }
};

const handleFileDrop = (event: DragEvent) => {
  event.preventDefault();
  draggedOver.value = false;

  if (event.dataTransfer && event.dataTransfer.files.length > 0 && event.dataTransfer.files[0]) {
    file.value = event.dataTransfer.files[0];
    fileUploaded.value = true;
    progress.value = 0;
    analysisComplete.value = false;
    analysisResult.value = 'AUTHENTIC';
  }
};

const resetUpload = () => {
  file.value = null;
  fileUploaded.value = false;
  progress.value = 0;
  analysisComplete.value = false;
  currentStep.value = 0;
  videoConfidence.value = 0;
  showExplainability.value = false;
};

const startAnalysis = async () => {
  if (!file.value) return;

  isAnalyzing.value = true;
  progress.value = 5;
  analysisComplete.value = false;

  try {
    const form = new FormData();
    form.append('file', file.value as Blob, (file.value as File).name);

    // POST to backend with explainability
    const resp = await fetch('https://vedant3114-backend-video.hf.space/predict-explain', {
      method: 'POST',
      body: form,
    });

    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`Server error: ${resp.status} ${txt}`);
    }

    progress.value = 80;
    const data = await resp.json();
    console.log('Backend response:', data);
    const result = data?.result ?? data;

    const label = result?.prediction?.label ?? result?.label ?? 'AUTHENTIC';
    const confidence = result?.prediction?.score ?? result?.confidence ?? result?.score ?? 0;
    analysisResult.value = label === 'DEEPFAKE' ? 'DEEPFAKE' : 'AUTHENTIC';
    videoConfidence.value = Math.round(confidence * 100);

    // Store explainability data
    explainabilityResult.value = result;

    // Extract video frame thumbnail
    try {
      const videoElement = document.createElement('video');
      videoElement.preload = 'metadata';
      const videoUrl = URL.createObjectURL(file.value as File);
      videoElement.src = videoUrl;
      
      await new Promise((resolve) => {
        videoElement.onloadedmetadata = () => {
          videoElement.currentTime = Math.min(1, videoElement.duration / 2);
        };
        videoElement.onseeked = () => resolve(null);
      });
      
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx?.drawImage(videoElement, 0, 0);
      analysisImageUrl.value = canvas.toDataURL('image/jpeg', 0.8);
      URL.revokeObjectURL(videoUrl);
    } catch (err) {
      console.warn('Could not extract video frame:', err);
      analysisImageUrl.value = '';
    }

    progress.value = 100;
    analysisComplete.value = true;
    showExplainability.value = true;
  } catch (err: any) {
    console.error(err);
    alert('Analysis failed: ' + (err?.message ?? err));
    isAnalyzing.value = false;
    progress.value = 0;
  } finally {
    isAnalyzing.value = false;
  }
};

const predictFromUrl = async () => {
  if (!videoUrl.value) {
    alert('Please enter a video URL');
    return;
  }

  urlLoading.value = true;
  analysisComplete.value = false;
  progress.value = 10;

  try {
    const resp = await fetch('http://localhost:8000/predict-url-explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: videoUrl.value })
    });

    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`Server error: ${resp.status} ${txt}`);
    }

    progress.value = 80;
    const data = await resp.json();
    console.log('URL prediction response:', data);
    const result = data?.result ?? data;

    const label = result?.prediction?.label ?? result?.label ?? 'AUTHENTIC';
    const confidence = result?.prediction?.score ?? result?.confidence ?? result?.score ?? 0;
    analysisResult.value = label === 'DEEPFAKE' ? 'DEEPFAKE' : 'AUTHENTIC';
    videoConfidence.value = Math.round(confidence * 100);

    explainabilityResult.value = result;

    // Try to extract video thumbnail from URL
    try {
      const videoElement = document.createElement('video');
      videoElement.crossOrigin = 'anonymous';
      videoElement.src = videoUrl.value;
      videoElement.preload = 'metadata';
      
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error('Timeout')), 5000);
        videoElement.onloadedmetadata = () => {
          clearTimeout(timeout);
          videoElement.currentTime = Math.min(1, videoElement.duration / 2);
        };
        videoElement.onseeked = () => {
          clearTimeout(timeout);
          resolve(null);
        };
        videoElement.onerror = () => {
          clearTimeout(timeout);
          reject(new Error('Video load error'));
        };
      });
      
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx?.drawImage(videoElement, 0, 0);
      analysisImageUrl.value = canvas.toDataURL('image/jpeg', 0.8);
    } catch (err) {
      console.warn('Could not extract video thumbnail from URL (CORS may be blocking):', err);
      analysisImageUrl.value = '';
    }

    progress.value = 100;
    analysisComplete.value = true;
    showExplainability.value = true;
  } catch (err: any) {
    console.error(err);
    alert('URL prediction failed: ' + (err?.message ?? err));
    progress.value = 0;
  } finally {
    urlLoading.value = false;
  }
};

const resetAnalysis = () => {
  analysisComplete.value = false;
  progress.value = 0;
  currentStep.value = 0;
  videoConfidence.value = 0;
  showExplainability.value = false;
  explainabilityResult.value = null;
};

const resetUrl = () => {
  videoUrl.value = '';
  analysisComplete.value = false;
  progress.value = 0;
  videoConfidence.value = 0;
  showExplainability.value = false;
  explainabilityResult.value = null;
};

// Image upload methods
const triggerImageFileInput = () => {
  if (imageFileInput.value) {
    imageFileInput.value.click();
  }
};

const handleImageFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0 && target.files[0]) {
    image.value = target.files[0];
    imageUploaded.value = true;
    imageProgress.value = 0;
    imageAnalysisComplete.value = false;
    imageAnalysisResult.value = 'AUTHENTIC';

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviewUrl.value = e.target?.result as string;
    };
    reader.readAsDataURL(target.files[0]);
  }
};

const handleImageDrop = (event: DragEvent) => {
  event.preventDefault();
  imagesDraggedOver.value = false;

  if (event.dataTransfer && event.dataTransfer.files.length > 0 && event.dataTransfer.files[0]) {
    const droppedFile = event.dataTransfer.files[0];
    if (droppedFile.type.startsWith('image/')) {
      image.value = droppedFile;
      imageUploaded.value = true;
      imageProgress.value = 0;
      imageAnalysisComplete.value = false;
      imageAnalysisResult.value = 'AUTHENTIC';

      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreviewUrl.value = e.target?.result as string;
      };
      reader.readAsDataURL(droppedFile);
    }
  }
};

const resetImageUpload = () => {
  image.value = null;
  imageUploaded.value = false;
  imageProgress.value = 0;
  imageAnalysisComplete.value = false;
  imagePreviewUrl.value = '';
  imageConfidence.value = 0;
};

const startImageAnalysis = async () => {
  if (!image.value) return;

  isImageAnalyzing.value = true;
  imageProgress.value = 5;
  imageAnalysisComplete.value = false;

  try {
    const file = image.value;

    const form = new FormData();
    form.append('file', file);

    // Call local backend on port 8000
    const resp = await fetch('https://manya2040-backend-image.hf.space/explain', {
      method: 'POST',
      body: form,
    });

    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`Server error: ${resp.status} ${txt}`);
    }

    imageProgress.value = 60;
    const data = await resp.json();
    console.log('Image backend response:', data);

    // Parse response
    imageAnalysisResult.value = data.prediction === 'Real' ? 'AUTHENTIC' : 'DEEPFAKE';
    
    // Parse confidence string "99.57%" -> 99.57
    const confStr = data.confidence_percentage?.replace('%', '') || '0';
    imageConfidence.value = parseFloat(confStr);

    // Set Explainability Data - store full response for component
    imageExplanationResult.value = {
      filename: data.filename || (image.value as File)?.name || 'image',
      prediction: data.prediction || 'Unknown',
      confidence_percentage: data.confidence_percentage || '0%',
      raw_score: data.raw_score || 0,
      dominant_focus_region: data.dominant_focus_region || 'Unknown',
      region_scores: data.region_scores || { 'Eyes/Forehead': 0, 'Nose/Cheeks': 0, 'Mouth/Chin': 0 },
      explanation: data.explanation || 'No explanation provided.',
      heatmap_image_base64: data.heatmap_image_base64 || '',
      original_image: imagePreviewUrl.value // Keep original image reference
    };
    
    imageExplanationText.value = data.explanation || 'No explanation provided.';
    imageHeatmapBase64.value = data.heatmap_image_base64 || '';
    imageDominantFocusRegion.value = data.dominant_focus_region || '';
    imageRegionScores.value = data.region_scores || null;

    imageProgress.value = 100;
    imageAnalysisComplete.value = true;
    showImageExplainability.value = true;

  } catch (err: any) {
    console.error(err);
    alert('Image analysis failed: ' + (err?.message ?? err));
    imageProgress.value = 0;
    isImageAnalyzing.value = false;
  } finally {
    isImageAnalyzing.value = false;
  }
};



const resetImageAnalysis = () => {
  imageAnalysisComplete.value = false;
  imageProgress.value = 0;
  image.value = null;
  imageUploaded.value = false;
  imagePreviewUrl.value = '';
  imageConfidence.value = 0;
  imageDominantFocusRegion.value = '';
  imageRegionScores.value = null;
};

const predictImageFromUrl = async () => {
    if (!imageUrl.value) {
        alert('Please enter an image URL');
        return;
    }

    imageUrlLoading.value = true;
    imageAnalysisComplete.value = false;
    imageProgress.value = 10;
    
    // Show the URL as preview initially
    imagePreviewUrl.value = imageUrl.value;

    try {
        const resp = await fetch('http://127.0.0.1:8001/explain-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: imageUrl.value })
        });

        if (!resp.ok) {
            const txt = await resp.text();
            throw new Error(`Server error: ${resp.status} ${txt}`);
        }
        
        imageProgress.value = 50;
        const data = await resp.json();
        
        // Parse response
        imageAnalysisResult.value = data.prediction === 'Real' ? 'AUTHENTIC' : 'DEEPFAKE';
        
        const confStr = data.confidence_percentage?.replace('%', '') || '0';
        imageConfidence.value = parseFloat(confStr);

        imageExplanationText.value = data.explanation || 'No explanation provided.';
        imageHeatmapBase64.value = data.heatmap_image_base64 || '';
        imageDominantFocusRegion.value = data.dominant_focus_region || '';
        imageRegionScores.value = data.region_scores || null;

        // Store original image as base64 from backend
        imageOriginalUrl.value = data.original_image_base64 || imageUrl.value;
        
        // Set Explainability Data with URL as filename
        imageExplanationResult.value = {
          filename: imageUrl.value, // Use URL as filename
          prediction: data.prediction || 'Unknown',
          confidence_percentage: data.confidence_percentage || '0%',
          raw_score: data.raw_score || 0,
          dominant_focus_region: data.dominant_focus_region || 'Unknown',
          region_scores: data.region_scores || { 'Eyes/Forehead': 0, 'Nose/Cheeks': 0, 'Mouth/Chin': 0 },
          explanation: data.explanation || 'No explanation provided.',
          heatmap_image_base64: data.heatmap_image_base64 || '',
          original_image: imageUrl.value // Keep original URL reference
        };

        imageProgress.value = 100;
        imageAnalysisComplete.value = true;
        showImageExplainability.value = true;

    } catch (err: any) {
        console.error(err);
        alert('Image URL analysis failed. Please verify the link is accessible. Error: ' + (err?.message ?? err));
        imageProgress.value = 0;
    } finally {
        imageUrlLoading.value = false;
    }
};


const resetImageUrl = () => {
    imageUrl.value = '';
    imageAnalysisComplete.value = false;
    imageProgress.value = 0;
    imageConfidence.value = 0;
    imagePreviewUrl.value = '';
    imageOriginalUrl.value = '';
    imageDominantFocusRegion.value = '';
    imageRegionScores.value = null;
};

const generatePDFReport = async (analysisType: 'image' | 'video') => {
  try {
    const reportElement = document.getElementById(
      analysisType === 'image' ? 'imagePdfReport' : 'videoPdfReport'
    );

    if (!reportElement) {
      console.error('Report element not found');
      alert('Report element not found. Please try again.');
      return;
    }

    // Show loading message
    const originalText = document.activeElement as HTMLButtonElement;
    if (originalText?.textContent) {
      originalText.textContent = '⏳ GENERATING...';
    }

    // Convert all images in the report to base64 to avoid CORS issues
    const images = reportElement.querySelectorAll('img');
    const imagePromises = Array.from(images).map(async (img) => {
      const imgElement = img as HTMLImageElement;
      if (imgElement.src && !imgElement.src.startsWith('data:')) {
        try {
          const response = await fetch(imgElement.src);
          const blob = await response.blob();
          const dataUrl = await new Promise<string>((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result as string);
            reader.readAsDataURL(blob);
          });
          imgElement.src = dataUrl;
        } catch (err) {
          console.warn('Failed to convert image to base64:', err);
        }
      }
    });
    await Promise.all(imagePromises);

    // Convert HTML to canvas with better error handling
    let canvas;
    try {
      canvas = await html2canvas(reportElement, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        logging: false,
        imageTimeout: 5000,
        onclone: (clonedDocument) => {
          // Ensure images are visible in clone
          const clonedElement = clonedDocument.getElementById(
            analysisType === 'image' ? 'imagePdfReport' : 'videoPdfReport'
          );
          if (clonedElement) {
            clonedElement.style.display = 'block';
          }
        }
      });
    } catch (canvasError) {
      console.error('Canvas conversion error:', canvasError);
      alert(`Failed to convert report to image: ${canvasError instanceof Error ? canvasError.message : 'Unknown error'}`);
      if (originalText?.textContent) {
        originalText.textContent = '📄 PDF REPORT';
      }
      return;
    }

    if (!canvas) {
      throw new Error('Canvas generation returned null');
    }

    // Create PDF
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    });

    const imgWidth = 210; // A4 width in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    let heightLeft = imgHeight;
    let position = 0;

    // Add image to PDF, handle multiple pages if needed
    const imgData = canvas.toDataURL('image/png');
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
    heightLeft -= 297; // A4 height in mm

    while (heightLeft >= 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= 297;
    }

    // Download PDF
    const timestamp = new Date().getTime();
    const fileName =
      analysisType === 'image'
        ? `deepfake-analysis-${image.value?.name || 'image'}-${timestamp}.pdf`
        : `deepfake-analysis-${file.value?.name || 'video'}-${timestamp}.pdf`;

    pdf.save(fileName);
    
    // Reset button text
    if (originalText?.textContent) {
      originalText.textContent = '📄 PDF REPORT';
    }
    
  } catch (error) {
    console.error('PDF generation failed:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    alert(`Failed to generate PDF report: ${errorMessage}`);
  }
};
</script>

<style>
/* Global full-screen reset */
html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  background-color: #0a0e2a;
  overflow: hidden;
}

/* Cyber Theme Styles */
.cyber-theme {
  background-color: #0a0e2a;
  color: #00ffff;
}

.cyber-bg {
  background: radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.05) 0%, rgba(0, 255, 255, 0) 50%);
}

.cyber-grid {
  background-image:
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.3;
}

.cyber-scanlines {
  background: repeating-linear-gradient(
    to bottom,
    rgba(0, 255, 255, 0.05),
    rgba(0, 255, 255, 0.05) 1px,
    transparent 1px,
    transparent 4px
  );
}

.cyber-card {
  background: rgba(10, 14, 42, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
}

.cyber-border-bottom {
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
}

.cyber-tabs {
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
}

.cyber-tab {
  background: rgba(10, 14, 42, 0.5);
  color: #8dcece;
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.cyber-tab.active {
  background: #00ffff;
  color: #0a0e2a;
  border-bottom: none;
}

.cyber-upload-zone {
  border: 2px dashed rgba(0, 255, 255, 0.3);
  background: rgba(0, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.cyber-upload-zone:hover {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.cyber-file-selected {
  border: 2px solid #00ffff;
  background: rgba(0, 255, 255, 0.05);
}

.cyber-analysis-status {
  background: rgba(10, 14, 42, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
}

.cyber-progress-container {
  background: rgba(46, 107, 107, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.cyber-progress-bar {
  background: linear-gradient(90deg, #00ffff, #00cccc);
}

.cyber-result-card {
  background: rgba(10, 14, 42, 0.8);
  border: 1px solid rgba(0, 255, 255, 0.2);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
}

.cyber-result-overlay {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.cyber-step {
  background: rgba(10, 14, 42, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.cyber-step:hover {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.05);
}

.cyber-stat-card {
  background: rgba(32, 75, 75, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.cyber-stat-card:hover {
  transform: scale(1.05);
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
}

.cyber-faq {
  background: rgba(32, 75, 75, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.1);
}

.cyber-faq summary {
  list-style: none;
}

.cyber-faq summary::-webkit-details-marker {
  display: none;
}

.cyber-footer {
  border-top: 1px solid rgba(0, 255, 255, 0.1);
  background: rgba(10, 14, 42, 0.3);
}

.cyber-footer-link {
  position: relative;
  transition: all 0.3s ease;
}

.cyber-footer-link:hover {
  color: #00ffff;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

.cyber-button {
  background: #00ffff;
  color: #0a0e2a;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.cyber-button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

.cyber-button:active {
  transform: scale(0.95);
}

.cyber-button-secondary {
  background: rgba(32, 75, 75, 0.7);
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.cyber-button-secondary:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
}

.cyber-text-glow {
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
}

.cyber-pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

.cyber-input {
  background: rgba(46, 107, 107, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.2);
  color: #00ffff;
  transition: all 0.3s ease;
}

.cyber-input:focus {
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  outline: none;
}

/* Main content wrapper: scrollable over fixed Vanta background */
#app > div:first-child {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Custom animation for progress bar */
@keyframes progressAnimation {
  from { width: 0; }
  to { width: var(--progress-width); }
}

/* Improved hover and focus states for interactive elements */
button:focus {
  outline: 2px solid #00ffff;
  outline-offset: 2px;
}

/* Larger focus/ring for keyboard users */
button:focus-visible {
  box-shadow: 0 0 0 4px rgba(0, 255, 255, 0.12);
}
/* Add these styles to your existing CSS in the <style> section */

/* Video Container Styles */
.cyber-video-container {
  position: relative;
  padding-top: 56.25%; /* 16:9 aspect ratio */
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.2);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  border-radius: 0.5rem;
  background: rgba(10, 14, 42, 0.3);
}

.cyber-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}

/* Cyber grid overlay for the video */
.cyber-video-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.15;
  pointer-events: none;
  z-index: 1;
}

/* Video loading state */
.cyber-video:not([src]) {
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), rgba(10, 14, 42, 0.3));
  background-size: 200% 200%;
  animation: videoLoading 2s ease-in-out infinite;
}

@keyframes videoLoading {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .cyber-video-container {
    padding-top: 75%; /* More square aspect on mobile */
    margin-bottom: 1.5rem;
  }
}
</style>