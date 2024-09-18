<template>
  <div class="meme-card absolute inset-0 bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden touch-none transition-transform duration-300 ease-out"
       @touchstart="touchStart" 
       @touchmove="touchMove" 
       @touchend="touchEnd"
       :style="cardStyle">
    <div v-if="!meme.imageUrl" class="loading-indicator flex justify-center items-center h-full">
      <div class="spinner w-10 h-10 border-4 border-blue-200 border-t-4 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
    <template v-else>
      <img :src="meme.imageUrl" :alt="meme.title" @load="imageLoaded = true" 
           class="w-full h-full object-cover transition-opacity duration-300"
           :class="{ 'opacity-0': !imageLoaded, 'opacity-100': imageLoaded }" />
      <div class="meme-info absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black to-transparent text-white">
        <h2 class="text-xl font-semibold mb-1">{{ meme.title }}</h2>
        <p class="text-sm opacity-80">Source: {{ meme.source }}</p>
      </div>
      <div class="reaction-overlay absolute inset-0 flex justify-center items-center pointer-events-none" :style="overlayStyle">
        <div v-if="offset > 0" class="reaction like text-green-500">
          <span class="emoji text-6xl">😂</span>
          <span class="text text-2xl font-bold">LOL</span>
        </div>
        <div v-else-if="offset < 0" class="reaction dislike text-red-500">
          <span class="emoji text-6xl">😒</span>
          <span class="text text-2xl font-bold">BRUH</span>
        </div>
        <div v-if="swipeUp" class="reaction favorite text-yellow-500">
          <span class="emoji text-6xl">❤️</span>
          <span class="text text-2xl font-bold">LMAO</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'MemeCard',
  props: {
    meme: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const offset = ref(0)
    const swipeUp = ref(false)
    const imageLoaded = ref(false)
    let startX = 0
    let startY = 0

    const cardStyle = computed(() => ({
      transform: `translateX(${offset.value}px) rotate(${offset.value * 0.1}deg)`,
      transition: offset.value === 0 ? 'transform 0.3s ease-out' : 'none'
    }))

    const overlayStyle = computed(() => ({
      opacity: Math.min(Math.abs(offset.value) / 100, 1)
    }))

    const touchStart = (event) => {
      startX = event.touches[0].clientX
      startY = event.touches[0].clientY
    }

    const touchMove = (event) => {
      const currentX = event.touches[0].clientX
      const currentY = event.touches[0].clientY
      const deltaX = currentX - startX
      const deltaY = startY - currentY

      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        offset.value = deltaX
        swipeUp.value = false
      } else if (deltaY > 50) {
        swipeUp.value = true
      }
      event.preventDefault()
    }

    const touchEnd = () => {
      if (Math.abs(offset.value) > 100) {
        const action = offset.value > 0 ? 'like' : 'dislike'
        emit('swipe', props.meme._id, action)
      } else if (swipeUp.value) {
        emit('swipe', props.meme._id, 'favorite')
      } else {
        offset.value = 0
        swipeUp.value = false
      }
    }

    return {
      offset,
      swipeUp,
      imageLoaded,
      cardStyle,
      overlayStyle,
      touchStart,
      touchMove,
      touchEnd
    }
  }
}
</script>

<style scoped>
.reaction {
  @apply flex flex-col items-center text-4xl font-bold;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.reaction .emoji {
  @apply text-6xl;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .meme-info h2 {
    @apply text-lg;
  }
  .meme-info p {
    @apply text-xs;
  }
}
</style>