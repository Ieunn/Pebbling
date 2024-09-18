<template>
  <div class="container">
    <h1>Pebbling</h1>
    <div class="source-selector">
      <select v-model="selectedSource" @change="resetAndFetchMemes">
        <option value="">All Sources</option>
        <option v-for="source in sources" :key="source" :value="source">{{ source }}</option>
      </select>
    </div>
    <div class="meme-stack">
      <MemeCard 
        v-for="(meme, index) in memes" 
        :key="meme._id"
        :meme="meme"
        :style="{ zIndex: memes.length - index }"
        @swipe="handleSwipe"
      />
    </div>
    <router-link to="/favorites" class="favorites-link">My Favorites</router-link>
    <AdComponent />
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import MemeCard from './components/MemeCard.vue'
import AdComponent from './components/AdComponent.vue'

export default {
  name: 'App',
  components: {
    MemeCard,
    AdComponent
  },
  setup() {
    const memes = ref([])
    const selectedSource = ref('')
    const sources = ref([])
    const viewedMemes = ref(JSON.parse(localStorage.getItem('viewedMemes') || '[]'))

    const fetchMemes = async (count = 5) => {
      try {
        const response = await axios.get('/api/get_memes', {
          params: { 
            source: selectedSource.value,
            exclude: viewedMemes.value,
            count: count
          }
        })
        if (response.data && response.data.length > 0) {
          memes.value.push(...response.data)
        } else {
          console.error('No meme data received')
        }
      } catch (error) {
        console.error('Error fetching memes:', error.response ? error.response.data : error.message)
      }
    }

    const resetAndFetchMemes = () => {
      memes.value = []
      fetchMemes()
    }

    const fetchSources = async () => {
      try {
        const response = await axios.get('/api/get_sources')
        sources.value = response.data
      } catch (error) {
        console.error('Error fetching sources:', error)
      }
    }

    const handleSwipe = async (memeId, action) => {
      viewedMemes.value.push(memeId)
      localStorage.setItem('viewedMemes', JSON.stringify(viewedMemes.value))

      try {
        await axios.post('/api/update_meme_status', { memeId, action })
      } catch (error) {
        console.error(`Error updating meme status:`, error)
      }

      memes.value.shift()
      if (memes.value.length < 3) {
        fetchMemes(3)
      }
    }

    onMounted(() => {
      fetchMemes()
      fetchSources()
    })

    watch(selectedSource, resetAndFetchMemes)

    return {
      memes,
      selectedSource,
      sources,
      handleSwipe
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
  padding: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}
h1 {
  margin-bottom: 1rem;
  font-size: 2.5rem;
}
.source-selector {
  margin-bottom: 1rem;
  width: 100%;
  max-width: 300px;
}
.favorites-link {
  margin-top: 1rem;
}
.meme-stack {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 500px;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  .meme-stack {
    height: 400px;
  }
}
</style>