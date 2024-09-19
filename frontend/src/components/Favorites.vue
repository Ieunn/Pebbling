<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold text-center text-gray-800 dark:text-gray-200 mb-8">My Favorites</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="meme in favorites" :key="meme._id" class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
        <div class="aspect-ratio-box" style="padding-top: 133.33%;">
          <img :src="meme.imageUrl" :alt="meme.title" class="absolute top-0 left-0 w-full h-full object-cover" />
        </div>
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">{{ meme.title }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">Source: {{ meme.source }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Favorites',
  setup() {
    const favorites = ref([])

    const fetchFavorites = async () => {
      try {
        const response = await axios.get('/api/get_favorites')
        favorites.value = response.data
      } catch (error) {
        console.error('Error fetching favorites:', error)
      }
    }

    onMounted(fetchFavorites)

    return {
      favorites
    }
  }
}
</script>

<style scoped>
.aspect-ratio-box {
  position: relative;
  height: 0;
  overflow: hidden;
}
</style>