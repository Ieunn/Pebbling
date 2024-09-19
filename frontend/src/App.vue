<template>
  <div :class="{'dark': isDarkMode}" class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white">
    <div class="container mx-auto px-4 py-8">
      <header class="mb-8">
        <h1 class="text-4xl font-bold text-center mb-4">Pebbling</h1>
        <nav class="flex justify-center space-x-4 mb-4">
          <router-link to="/" class="text-blue-500 hover:text-blue-600">Home</router-link>
          <router-link to="/favorites" class="text-blue-500 hover:text-blue-600">Favorites</router-link>
        </nav>
        <button @click="toggleDarkMode" class="p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
          <svg v-if="isDarkMode" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>
      </header>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value)
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    onMounted(() => {
        if (isDarkMode.value) {
          document.documentElement.classList.add('dark')
        }
      })

    return {
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>