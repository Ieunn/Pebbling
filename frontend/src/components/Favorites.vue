<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold text-center text-gray-800 dark:text-gray-200 mb-8">My Favorites</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="meme in favorites" :key="meme._id" class="relative w-full aspect-[3/4] max-w-sm max-h-[80vh]">
        <MemeCard 
          :meme="meme"
          :is-empty="false"
          @swipe="removeFavorite(meme._id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import MemeCard from './MemeCard.vue'

export default {
  name: 'Favorites',
  components: {
    MemeCard
  },
  setup() {
    const favorites = ref([])

    const fetchFavorites = () => {
      const storedFavorites = localStorage.getItem('favorites')
      favorites.value = storedFavorites ? JSON.parse(storedFavorites) : []
    }

    const removeFavorite = (memeId) => {
      favorites.value = favorites.value.filter(meme => meme._id !== memeId)
      localStorage.setItem('favorites', JSON.stringify(favorites.value))
    }

    onMounted(fetchFavorites)

    return {
      favorites,
      removeFavorite
    }
  }
}
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}
</style>