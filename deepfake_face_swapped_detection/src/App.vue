<template>
  <div
    class="relative flex h-auto min-h-screen w-full flex-col bg-[#0f2424] dark group/design-root overflow-x-hidden"
    style='font-family: "Space Grotesk", "Noto Sans", sans-serif;'
  >
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-4 sm:px-6 md:px-10 lg:px-20 xl:px-40 flex flex-1 justify-center py-3 sm:py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] w-full flex-1">
          <div>
            <div class="sm:p-4">
              <div
                class="flex min-h-[200px] sm:min-h-[280px] md:min-h-[320px] lg:min-h-[400px] xl:min-h-[480px] flex-col gap-4 sm:gap-6 md:gap-8 bg-contain sm:bg-cover bg-center bg-no-repeat sm:gap-8 sm:rounded-xl items-center justify-center p-3 sm:p-4 md:p-6 mobile-bg-contain"
                style='background-image: linear-gradient(rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuCqtijFadhSaZhtasCkpaPDDRdOW91-laIe8GfEf62qPQbqm8AzfzFxw56yJFa1i2niLVzzcxMEDLvMIhwy0rySBS53xp1UIzCo2TNosDNqxaSRjh3NJLH48UgzdoZMQk-xkF6XIkLAhx-tKkJQDZkUv683h1wnbPZUWuiq08TQkBAlqUZebQ-Qm7caXuKLmZxKkJn0qbXxqKSti8-o6swFufsxNx2FWxtJYS2_uJ4xpjp3LeMSwS_LLZjxciP0eUwKF9WqsmwSjGo");'
              >
                <h1
                  class="text-white text-xl sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl font-black leading-tight tracking-[-0.033em] sm:text-5xl text-center px-2 sm:px-4"
                >
                  Deepfake Detector: Verify Authenticity in Seconds
                </h1>
                <button
                  @click="scrollToDetection"
                  class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 md:h-12 px-3 sm:px-4 md:px-5 bg-[#00ffff] text-[#0f2424] text-xs sm:text-sm md:text-base font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105"
                >
                  <span class="truncate">Start Analysis</span>
                </button>
              </div>
            </div>
          </div>

          <h2 class="text-white text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em] px-3 sm:px-4 md:px-6 pb-2 sm:pb-3 pt-3 sm:pt-5">Detection Tool</h2>

          <div class="flex flex-col p-3 sm:p-4">
            <div 
              v-if="!fileUploaded" 
              class="flex flex-col items-center gap-4 sm:gap-6 rounded-xl border-2 border-dashed border-[#2e6b6b] px-4 sm:px-6 py-6 sm:py-14 transition-all duration-300 hover:border-[#00ffff]"
              @dragover.prevent
              @drop.prevent="handleFileDrop"
              @click="triggerFileInput"
            >
              <div class="flex max-w-[320px] sm:max-w-[480px] flex-col items-center gap-2">
                <p class="text-white text-base sm:text-lg font-bold leading-tight max-w-[320px] sm:max-w-[480px] text-center px-2">
                  {{ draggedOver ? 'Release to drop your video' : 'Drag and drop a video here' }}
                </p>
                <p class="text-white text-xs sm:text-sm font-normal leading-normal max-w-[320px] sm:max-w-[480px] text-center px-2">
                  Or click to upload
                </p>
              </div>
              <button
                class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#204b4b] text-white text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105"
              >
                <span class="truncate">Upload Video</span>
              </button>
              <input
                type="file"
                ref="fileInput"
                accept="video/mp4,video/avi,video/mov"
                @change="handleFileUpload"
                class="hidden"
              />
            </div>

            <div v-else class="flex flex-col items-center gap-4 rounded-xl border-2 border-[#00ffff] px-4 py-6">
              <div class="w-full max-w-[480px] flex items-center gap-4">
                <div class="text-white text-sm font-medium truncate max-w-[200px]">
                  {{ file?.name }}
                </div>
                <div class="flex gap-2">
                  <button
                    @click="resetUpload"
                    class="flex min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105"
                  >
                    <span class="truncate">Remove</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

            <div v-if="fileUploaded && !analysisComplete" class="flex flex-col gap-2 sm:gap-3 p-3 sm:p-4">
            <div class="flex gap-4 sm:gap-6 justify-between">
              <p class="text-white text-sm sm:text-base font-medium leading-normal">
                {{ isAnalyzing ? 'Analyzing...' : 'Ready to analyze' }}
              </p>
              <p class="text-[#00ffff] text-xs sm:text-sm font-medium leading-normal">
                {{ isAnalyzing ? progress + '%' : 'Click Analyze to start' }}
              </p>
            </div>
            <div class="rounded bg-[#2e6b6b] h-3 sm:h-2">
              <div 
                class="h-full rounded bg-[#00ffff] transition-all duration-500 ease-out" 
                :style="{ width: progress + '%' }"
              ></div>
            </div>
            <p class="text-[#8dcece] text-xs sm:text-sm font-normal leading-normal">
              {{ isAnalyzing ? 'This may take a few seconds' : 'Analysis will start when you click the button' }}
            </p>
          </div>

          <div v-if="fileUploaded && !analysisComplete" class="flex px-3 sm:px-4 py-2 sm:py-3 justify-center">
            <button
              @click="startAnalysis"
              :disabled="isAnalyzing"
              class="flex min-w-[64px] sm:min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 sm:h-10 px-3 sm:px-4 bg-[#00ffff] text-[#0f2424] text-xs sm:text-sm font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              <span class="truncate">
                {{ isAnalyzing ? 'Analyzing...' : 'Analyze' }}
              </span>
            </button>
          </div>

          <div v-if="analysisComplete" class="p-3 sm:p-4">
            <div
              class="bg-cover bg-center flex flex-col items-stretch justify-end rounded-xl pt-[100px] sm:pt-[120px] md:pt-[132px]"
              :style="`background-image: linear-gradient(0deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0) 100%), url('${analysisImageUrl}');`"
            >
              <div class="flex w-full items-end justify-between gap-2 sm:gap-4 p-3 sm:p-4">
                <p 
                  class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight flex-1"
                  :class="analysisResult === 'AUTHENTIC' ? 'text-green-400' : 'text-red-400'"
                >
                  {{ analysisResult }}
                </p>
                <button
                  @click="resetAnalysis"
                  class="flex min-w-[64px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-3 bg-[#204b4b] text-white text-xs font-bold leading-normal tracking-[0.015em] transition-transform duration-200 hover:scale-105"
                >
                  <span class="truncate">New Analysis</span>
                </button>
              </div>
              <div class="p-4">
                <div 
                  class="bg-[#204b4b] rounded-lg p-4"
                  v-if="analysisResult === 'DEEPFAKE'"
                >
                  <h3 class="text-white text-sm font-bold mb-2">Deepfake Detection Report</h3>
                  <ul class="text-[#8dcece] text-xs space-y-1">
                    <li>• Facial inconsistencies detected in 72% of frames</li>
                    <li>• Eye movement unnaturalness: high probability</li>
                    <li>• Lighting inconsistencies detected</li>
                    <li>• Audio-visual desynchronization noted</li>
                  </ul>
                </div>
                <div 
                  class="bg-[#173636] rounded-lg p-4"
                  v-else
                >
                  <h3 class="text-white text-sm font-bold mb-2">Authenticity Verification Report</h3>
                  <ul class="text-[#8dcece] text-xs space-y-1">
                    <li>• No facial inconsistencies detected</li>
                    <li>• Natural eye movement pattern confirmed</li>
                    <li>• Lighting consistent throughout video</li>
                    <li>• Audio-visual synchronization within normal range</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <h2 class="text-white text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em] px-3 sm:px-4 md:px-6 pb-2 sm:pb-3 pt-3 sm:pt-5">How It Works</h2>

          <div class="grid grid-cols-[repeat(auto-fit,minmax(140px,1fr))] gap-2 sm:gap-3 p-3 sm:p-4">
            <div 
              v-for="(step, index) in steps" 
              :key="index"
              class="flex flex-1 gap-2 sm:gap-3 rounded-lg border border-[#2e6b6b] bg-[#173636] p-3 sm:p-4 items-center transition-all duration-300 hover:border-[#00ffff]"
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

          <h2 class="text-white text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em] px-3 sm:px-4 md:px-6 pb-2 sm:pb-3 pt-3 sm:pt-5">Why Choose Us</h2>
          <div class="flex flex-wrap gap-3 sm:gap-4 p-3 sm:p-4">
            <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105">
              <p class="text-white text-sm sm:text-base font-medium leading-normal">F1-Score</p>
              <p class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight">97%</p>
            </div>
            <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105">
              <p class="text-white text-sm sm:text-base font-medium leading-normal">Accuracy</p>
              <p class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight">98.5%</p>
            </div>
            <div class="flex min-w-[140px] flex-1 flex-col gap-2 rounded-xl p-4 sm:p-6 bg-[#204b4b] transition-all duration-300 hover:scale-105">
              <p class="text-white text-sm sm:text-base font-medium leading-normal">Processing</p>
              <p class="text-white tracking-light text-xl sm:text-2xl font-bold leading-tight">&lt; 10s</p>
            </div>
          </div>

          <p class="text-white text-sm sm:text-base font-normal leading-normal pb-3 sm:pb-5 pt-2 sm:pt-3 px-3 sm:px-4 text-center">Audio-Visual Synchronization Analysis</p>

          <h2 class="text-white text-[18px] sm:text-[20px] md:text-[22px] font-bold leading-tight tracking-[-0.015em] px-3 sm:px-4 md:px-6 pb-2 sm:pb-3 pt-3 sm:pt-5">Frequently Asked Questions</h2>
          <div class="flex flex-col p-3 sm:p-4 gap-2 sm:gap-3">
            <details 
              v-for="(faq, index) in faqs" 
              :key="index"
              class="flex flex-col rounded-xl bg-[#204b4b] px-3 sm:px-4 py-2 sm:py-3 group"
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

          <footer class="flex flex-col gap-4 sm:gap-6 px-3 sm:px-5 py-6 sm:py-10 text-center">
            <div class="flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
              <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300">
                Privacy Policy
              </button>
              <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300">
                Terms of Service
              </button>
              <button class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal hover:text-white transition-colors duration-300">
                Contact Us
              </button>
            </div>
            <p class="text-[#8dcece] text-xs sm:text-base font-normal leading-normal">© 2025 Deepfake Detector. All rights reserved.</p>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// State variables
const fileInput = ref<HTMLInputElement | null>(null);
const file = ref<File | null>(null);
const fileUploaded = ref(false);
const isAnalyzing = ref(false);
const analysisComplete = ref(false);
const analysisResult = ref<'AUTHENTIC' | 'DEEPFAKE'>('AUTHENTIC');
const progress = ref(0);
const currentStep = ref(0);
const draggedOver = ref(false);
const analysisImageUrl = ref('');

// Steps for the process
const steps = [
  { title: 'Extract Features', icon: 'FilmSlate' },
  { title: 'Analyze Synchronization', icon: 'Play' },
  { title: 'Predict', icon: 'Robot' }
];

// FAQ data
const faqs = [
  {
    question: 'What types of files can I upload?',
    answer: 'You can upload video files in MP4, AVI, and MOV formats. Ensure the file size does not exceed 100MB for optimal performance.',
    open: false
  },
  {
    question: 'How long does the analysis take?',
    answer: 'Analysis typically completes within a few seconds to a minute depending on file size and hardware.',
    open: false
  },
  {
    question: 'Is my data secure?',
    answer: 'Files are processed locally in your browser for the current demo; no files are uploaded in this version.',
    open: false
  }
];

// Methods
const scrollToDetection = () => {
  const detectionSection = document.querySelector('.flex.flex-col.p-3');
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
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
    fileUploaded.value = true;
    progress.value = 0;
    analysisComplete.value = false;
    analysisResult.value = 'AUTHENTIC';
  }
};

const handleFileDrop = (event: DragEvent) => {
  event.preventDefault();
  draggedOver.value = false;
  
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
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
};

const startAnalysis = () => {
  if (!file.value) return;
  
  isAnalyzing.value = true;
  progress.value = 0;
  currentStep.value = 0;
  analysisComplete.value = false;
  
  // Simulate analysis progress
  const interval = setInterval(() => {
    progress.value += 10;
    
    // Update current step based on progress
    if (progress.value >= 30 && currentStep.value < 1) {
      currentStep.value = 1;
    } else if (progress.value >= 70 && currentStep.value < 2) {
      currentStep.value = 2;
    }
    
    if (progress.value >= 100) {
      clearInterval(interval);
      completeAnalysis();
    }
  }, 300);
};

const completeAnalysis = () => {
  isAnalyzing.value = false;
  analysisComplete.value = true;
  
  // Randomly determine result (60% chance for authentic, 40% for deepfake)
  analysisResult.value = Math.random() < 0.6 ? 'AUTHENTIC' : 'DEEPFAKE';
  
  // Set analysis image based on result
  if (analysisResult.value === 'AUTHENTIC') {
    analysisImageUrl.value = "https://lh3.googleusercontent.com/aida-public/AB6AXuBWykGhzIhAAROV41C5B3xoquJD9m81hBvD8p1gT6EhIjDdIGG9gev_yvHpgEF_RNke8_0jE2zdQo_Uj1hBPHwFiVdcwwt4VZJZzWzzf8CZPDjye1RT59yI_qUNXWyDiqcO7Beca8C6nkZOQkzTIqPBBu1P5sxTHIHPWqv8EH68Sf1mcEVy1W0U_sOz3oDl-91RMe4WHCc56ROdbJ5J-i-rgM7sp56j69mJry4mR5Xau4klNDx1yBGegqPrp-ddQFjMe_a5Ibde2pk";
  } else {
    analysisImageUrl.value = "https://lh3.googleusercontent.com/aida-public/AB6AXuBWykGhzIhAAROV41C5B3xoquJD9m81hBvD8p1gT6EhIjDdIGG9gev_yvHpgEF_RNke8_0jE2zdQo_Uj1hBPHwFiVdcwwt4VZJZzWzzf8CZPDjye1RT59yI_qUNXWyDiqcO7Beca8C6nkZOQkzTIqPBBu1P5sxTHIHPWqv8EH68Sf1mcEVy1W0U_sOz3oDl-91RMe4WHCc56ROdbJ5J-i-rgM7sp56j69mJry4mR5Xau4klNDx1yBGegqPrp-ddQFjMe_a5Ibde2pk";
  }
};

const resetAnalysis = () => {
  analysisComplete.value = false;
  progress.value = 0;
  currentStep.value = 0;
};
</script>

<style scoped>
/* Additional mobile-first styles */
.layout-content-container { 
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

/* Ensure proper scrolling on mobile */
@media (max-width: 640px) {
  .layout-content-container {
    padding: 0 10px;
  }
  /* Ensure hero background is contained on small screens to avoid cropping important text */
  .mobile-bg-contain {
    background-size: contain !important;
    background-position: center !important;
  }
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

details summary::-webkit-details-marker {
  display: none;
}
</style>