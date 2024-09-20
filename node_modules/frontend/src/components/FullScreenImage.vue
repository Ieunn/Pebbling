<template>
    <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click="$emit('close')">
      <div class="relative w-full h-full overflow-hidden" @click.stop>
        <div class="absolute inset-0 flex items-center justify-center">
          <img 
            :src="imageUrl" 
            :alt="'Full screen image'" 
            class="max-w-none"
            :style="imageStyle"
            @wheel="handleWheel"
            @mousedown="startDrag"
            @mousemove="drag"
            @mouseup="endDrag"
            @mouseleave="endDrag"
            @touchstart="startDrag"
            @touchmove="drag"
            @touchend="endDrag"
          >
        </div>
      </div>
      <button @click="$emit('close')" class="absolute top-4 right-4 text-white">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>
</template>
  
<script>
  import { ref, computed } from 'vue'
  
  export default {
    props: {
      imageUrl: {
        type: String,
        required: true
      }
    },
    setup() {
      const scale = ref(1)
      const translateX = ref(0)
      const translateY = ref(0)
      let isDragging = false
      let startX = 0
      let startY = 0
  
      const imageStyle = computed(() => {
        return {
          transform: `scale(${scale.value}) translate(${translateX.value}px, ${translateY.value}px)`,
          transition: isDragging ? 'none' : 'transform 0.2s'
        }
      })
  
      const handleWheel = (event) => {
        event.preventDefault()
        const delta = event.deltaY > 0 ? 0.9 : 1.1
        scale.value = Math.max(0.1, Math.min(5, scale.value * delta))
      }
  
      const startDrag = (event) => {
        isDragging = true
        startX = event.clientX || event.touches[0].clientX
        startY = event.clientY || event.touches[0].clientY
      }
  
      const drag = (event) => {
        if (!isDragging) return
        const clientX = event.clientX || event.touches[0].clientX
        const clientY = event.clientY || event.touches[0].clientY
        const dx = clientX - startX
        const dy = clientY - startY
        translateX.value += dx / scale.value
        translateY.value += dy / scale.value
        startX = clientX
        startY = clientY
      }
  
      const endDrag = () => {
        isDragging = false
      }
  
      return {
        imageStyle,
        handleWheel,
        startDrag,
        drag,
        endDrag
      }
    }
  }
</script>
  
<style scoped>
.max-w-none {
    max-width: none;
}
</style>