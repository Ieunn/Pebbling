<template>
  <div :class="{'dark': isDarkMode}" class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white">
    <div class="container mx-auto px-4 py-8">
      <header class="mb-8">
        <h1 class="text-4xl font-bold text-center mb-4">Pebbling</h1>
        <nav class="flex justify-center space-x-4 mb-4">
          <router-link to="/" class="text-blue-500 hover:text-blue-600">Home</router-link>
          <router-link to="/favorites" class="text-blue-500 hover:text-blue-600">Favorites</router-link>
        </nav>
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

    return {
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>