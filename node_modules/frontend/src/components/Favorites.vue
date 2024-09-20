<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-3xl font-bold text-center text-gray-800 dark:text-gray-200 mb-8">My Favorites</h2>
    <div v-if="favorites.length === 0" class="text-center text-gray-600 dark:text-gray-400">
      <p class="text-xl mb-4">You haven't favorited any memes yet.</p>
      <p>Swipe up on memes you like to add them to your favorites!</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <FavoriteMemeCard
        v-for="meme in favorites"
        :key="meme._id"
        :meme="meme"
        @remove-favorite="removeFavorite"
        @show-full-screen="showFullScreenImage"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import FavoriteMemeCard from './FavoriteMemeCard.vue'

export default {
  name: 'Favorites',
  components: {
    FavoriteMemeCard
  },
  setup() {
    const favorites = ref([])
    const setFullScreenImage = inject('setFullScreenImage')

    const fetchFavorites = () => {
      const storedFavorites = localStorage.getItem('favorites')
      favorites.value = storedFavorites ? JSON.parse(storedFavorites) : []
    }

    const removeFavorite = (memeId) => {
      favorites.value = favorites.value.filter(meme => meme._id !== memeId)
      localStorage.setItem('favorites', JSON.stringify(favorites.value))
    }

    const showFullScreenImage = (imageUrl) => {
      setFullScreenImage(imageUrl)
    }

    onMounted(fetchFavorites)

    return {
      favorites,
      removeFavorite,
      showFullScreenImage
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