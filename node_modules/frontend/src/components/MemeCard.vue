<template>
  <transition name="slide" @after-leave="onLeave">
    <div v-if="!isLeaving" class="meme-card absolute inset-0 bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden touch-none"
         @touchstart="touchStart" 
         @touchmove="touchMove" 
         @touchend="touchEnd"
         @mousedown="mouseDown"
         @mousemove="mouseMove"
         @mouseup="mouseUp"
         @mouseleave="mouseUp"
         :style="cardStyle">
      <div v-if="isEmpty" class="flex flex-col items-center justify-center h-full p-4 text-center">
        <p class="text-xl font-semibold mb-2">No more memes available!</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">Check back later for new memes</p>
      </div>
      <template v-else>
        <div v-if="!meme.imageUrl" class="loading-indicator flex justify-center items-center h-full">
          <div class="spinner w-10 h-10 border-4 border-blue-200 border-t-4 border-t-blue-500 rounded-full animate-spin"></div>
        </div>
        <template v-else>
          <img :src="meme.imageUrl" :alt="meme.title" @load="imageLoaded = true" 
              class="w-full h-full object-contain transition-opacity duration-300"
              :class="{ 'opacity-0': !imageLoaded, 'opacity-100': imageLoaded }" />
          <div class="meme-info absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black to-transparent text-white">
            <h2 class="text-xl font-semibold mb-1">{{ meme.title }}</h2>
            <p class="text-sm opacity-80">Source: {{ meme.source }}</p>
          </div>
          <button @click="showFullScreenImage" class="absolute top-2 right-2 bg-white dark:bg-gray-800 p-2 rounded-full shadow-md z-10">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
            </svg>
          </button>
        </template>
      </template>
      <div class="reaction-overlay absolute inset-0 flex justify-center items-center pointer-events-none" :style="overlayStyle">
        <div v-if="currentAction === 'like'" class="reaction like text-green-500">
          <span class="emoji text-6xl">😂</span>
          <span class="text text-2xl font-bold">LOL</span>
        </div>
        <div v-else-if="currentAction === 'dislike'" class="reaction dislike text-red-500">
          <span class="emoji text-6xl">😒</span>
          <span class="text text-2xl font-bold">BRUH</span>
        </div>
        <div v-else-if="currentAction === 'favorite'" class="reaction favorite text-yellow-500">
          <span class="emoji text-6xl">❤️</span>
          <span class="text text-2xl font-bold">LMAO</span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, computed, inject } from 'vue'

export default {
  name: 'MemeCard',
  props: {
    meme: {
      type: Object,
      required: true
    },
    isEmpty: {
      type: Boolean,
      default: false
    }
  },
  emits: ['swipe'],
  setup(props, { emit }) {
    const offset = ref({ x: 0, y: 0 })
    const imageLoaded = ref(false)
    const isLeaving = ref(false)
    let startX = 0
    let startY = 0
    let isDragging = false

    const setFullScreenImage = inject('setFullScreenImage')

    const showFullScreenImage = () => {
      setFullScreenImage(props.meme.imageUrl)
    }

    const currentAction = computed(() => {
      const absX = Math.abs(offset.value.x)
      const absY = Math.abs(offset.value.y)
      if (absX > absY) {
        return offset.value.x > 50 ? 'dislike' : (offset.value.x < -50 ? 'like' : '')
      } else {
        return offset.value.y > 50 ? 'favorite' : ''
      }
    })

    const cardStyle = computed(() => ({
      transform: `translate(${offset.value.x}px, ${-offset.value.y}px) rotate(${offset.value.x * 0.1}deg)`,
      transition: (offset.value.x === 0 && offset.value.y === 0) ? 'transform 0.3s ease-out' : 'none'
    }))

    const overlayStyle = computed(() => ({
      opacity: Math.min(Math.sqrt(Math.pow(offset.value.x, 2) + Math.pow(offset.value.y, 2)) / 100, 1)
    }))

    const touchStart = (event) => {
      startX = event.touches[0].clientX
      startY = event.touches[0].clientY
      event.preventDefault()
    }

    const touchMove = (event) => {
      const currentX = event.touches[0].clientX
      const currentY = event.touches[0].clientY
      handleMove(currentX, currentY)
      event.preventDefault()
    }

    const touchEnd = (event) => {
      handleEnd()
      event.preventDefault()
    }

    const mouseDown = (event) => {
      isDragging = true
      startX = event.clientX
      startY = event.clientY
      event.preventDefault()
    }

    const mouseMove = (event) => {
      if (isDragging) {
        handleMove(event.clientX, event.clientY)
      }
      event.preventDefault()
    }

    const mouseUp = (event) => {
      if (isDragging) {
        isDragging = false
        handleEnd()
      }
      event.preventDefault()
    }

    const handleMove = (currentX, currentY) => {
      const deltaX = currentX - startX
      const deltaY = startY - currentY
      offset.value = { x: deltaX, y: deltaY }
    }

    const handleEnd = () => {
      if (props.isEmpty) {
        offset.value = { x: 0, y: 0 }
        return
      }

      const distance = Math.sqrt(Math.pow(offset.value.x, 2) + Math.pow(offset.value.y, 2))
      if (distance > 100) {
        const direction = Math.abs(offset.value.x) > Math.abs(offset.value.y)
          ? (offset.value.x > 0 ? 'right' : 'left')
          : (offset.value.y > 0 ? 'down' : 'up')
        
        if (direction === 'down') {
          offset.value = { x: 0, y: 0 }
        } else {
          isLeaving.value = true
          emit('swipe', props.meme._id, currentAction.value, direction)
        }
      } else {
        offset.value = { x: 0, y: 0 }
      }
    }

    const onLeave = () => {
      emit('cardLeft')
    }

    return {
      offset,
      imageLoaded,
      isLeaving,
      cardStyle,
      overlayStyle,
      currentAction,
      showFullScreenImage,
      touchStart,
      touchMove,
      touchEnd,
      mouseDown,
      mouseMove,
      mouseUp,
      onLeave
    }
  }
}
</script>

<style scoped>
.meme-card {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .meme-card {
    max-width: 95vw;
    max-height: 70vh;
  }
}

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