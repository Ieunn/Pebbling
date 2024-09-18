<template>
  <div class="meme-card" 
       @touchstart="touchStart" 
       @touchmove="touchMove" 
       @touchend="touchEnd"
       :style="cardStyle">
    <div v-if="!meme.imageUrl" class="loading-indicator">
      <div class="spinner"></div>
    </div>
    <template v-else>
      <img :src="meme.imageUrl" :alt="meme.title" @load="imageLoaded = true" :style="{ opacity: imageLoaded ? 1 : 0 }" />
      <h2>{{ meme.title }}</h2>
      <p>Source: {{ meme.source }}</p>
      <div class="reaction-overlay" :style="overlayStyle">
        <div v-if="offset > 0" class="reaction like">
          <span class="emoji">😂</span>
          <span class="text">LOL</span>
        </div>
        <div v-else-if="offset < 0" class="reaction dislike">
          <span class="emoji">😒</span>
          <span class="text">BRUH</span>
        </div>
        <div v-if="swipeUp" class="reaction favorite">
          <span class="emoji">❤️</span>
          <span class="text">LMAO</span>
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
.meme-card {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  touch-action: none;
}
img {
  width: 100%;
  height: 70%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}
h2 {
  font-size: 1.5rem;
  margin: 1rem;
}
p {
  font-size: 1rem;
  color: #666;
  margin: 0 1rem 1rem;
}
.reaction-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
}
.reaction {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 2rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.reaction .emoji {
  font-size: 4rem;
}
.like {
  color: #4CAF50;
}
.dislike {
  color: #F44336;
}
.favorite {
  color: #FF9800;
}
.loading-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  h2 {
    font-size: 1.2rem;
  }
  p {
    font-size: 0.9rem;
  }
}
</style>