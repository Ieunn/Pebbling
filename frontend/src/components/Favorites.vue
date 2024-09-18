<template>
  <div class="favorites-container">
    <h2>My Favorites</h2>
    <div class="favorites-grid">
      <div v-for="meme in favorites" :key="meme._id" class="favorite-item">
        <img :src="meme.imageUrl" :alt="meme.title" />
        <div class="favorite-info">
          <h3>{{ meme.title }}</h3>
          <p>Source: {{ meme.source }}</p>
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
.favorites-container {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  color: #4a4a4a;
  margin-bottom: 2rem;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.favorite-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.favorite-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.favorite-info {
  padding: 1rem;
}

.favorite-item h3 {
  font-size: 1.1rem;
  margin: 0 0 0.5rem;
  color: #333;
}

.favorite-item p {
  font-size: 0.9rem;
  margin: 0;
  color: #666;
}

@media (max-width: 768px) {
  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
</style>