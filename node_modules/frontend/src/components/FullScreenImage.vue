<template>
    <div class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50" @click="$emit('close')">
      <div class="relative max-w-full max-h-full p-4">
        <img :src="imageUrl" alt="Full screen image" class="max-w-full max-h-full object-contain" />
        <button @click="$emit('close')" class="absolute top-4 right-4 bg-white rounded-full p-2">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FullScreenImage',
    props: {
      imageUrl: {
        type: String,
        required: true,
      },
    },
  }
  </script>