<template>
  <div class="container">
    <h1>Random Meme Delivery</h1>
    <MemeDisplay v-if="!loading" :meme="meme" />
    <p v-else>Loading...</p>
    <button @click="fetchMeme">Get Another Meme</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MemeDisplay from './components/MemeDisplay.vue'

export default {
  name: 'App',
  components: {
    MemeDisplay
  },
  setup() {
    const meme = ref(null)
    const loading = ref(true)

    const fetchMeme = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/getMeme')
        meme.value = response.data
      } catch (error) {
        console.error('Error fetching meme:', error)
      }
      loading.value = false
    }

    onMounted(fetchMeme)

    return {
      meme,
      loading,
      fetchMeme
    }
  }
}
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 0 0.5rem;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}
h1 {
  margin-bottom: 2rem;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}
</style>