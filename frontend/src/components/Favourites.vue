<template>
    <div class="favorites-container">
      <h2>My Favorites</h2>
      <div class="favorites-grid">
        <div v-for="meme in favorites" :key="meme._id" class="favorite-item">
          <img :src="meme.imageUrl" :alt="meme.title" />
          <h3>{{ meme.title }}</h3>
          <p>Source: {{ meme.source }}</p>
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
  .favorites-container {
    padding: 1rem;
  }
  
  .favorites-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .favorite-item {
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .favorite-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  
  .favorite-item h3 {
    font-size: 1rem;
    margin: 0.5rem;
  }
  
  .favorite-item p {
    font-size: 0.8rem;
    margin: 0.5rem;
    color: #666;
  }
  </style>