<template>
  <div class="container">
    <header>
      <h1>Pebbling</h1>
      <div class="controls">
        <div class="source-selector">
          <select v-model="selectedSource" @change="resetAndFetchMemes">
            <option value="">All Sources</option>
            <option v-for="source in sources" :key="source" :value="source">{{ source }}</option>
          </select>
        </div>
        <button @click="toggleDarkMode" class="dark-mode-toggle">
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </header>
    <main>
      <div class="meme-stack">
        <TransitionGroup name="meme-card">
          <MemeCard 
            v-for="(meme, index) in memes" 
            :key="meme._id"
            :meme="meme"
            :style="{ zIndex: memes.length - index }"
            @swipe="handleSwipe"
          />
        </TransitionGroup>
      </div>
    </main>
    <footer>
      <router-link to="/favorites" class="favorites-link">My Favorites</router-link>
      <AdComponent />
    </footer>
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
    const selectedSource = ref(localStorage.getItem('lastSelectedSource') || '')
    const sources = ref([])
    const viewedMemes = ref(JSON.parse(localStorage.getItem('viewedMemes') || '[]'))
    const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

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
          memes.value = [...memes.value, ...response.data]
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
      localStorage.setItem('lastSelectedSource', selectedSource.value)
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

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value)
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
      handleSwipe,
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f0f2f5;
  color: #333;
}

.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 1rem;
}

header {
  text-align: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #4a4a4a;
  margin-bottom: 1rem;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.source-selector {
  max-width: 300px;
  margin: 0 auto;
}

.source-selector select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.dark-mode-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.dark-mode {
  background-color: #1a1a1a;
  color: #f0f0f0;
}

.dark-mode .meme-card {
  background-color: #2a2a2a;
}

.dark-mode .favorites-link {
  background-color: #45a049;
}

.dark-mode .favorites-link:hover {
  background-color: #3d8b3d;
}

main {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.meme-stack {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 500px;
}

footer {
  margin-top: 2rem;
  text-align: center;
}

.favorites-link {
  display: inline-block;
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.favorites-link:hover {
  background-color: #45a049;
}

.meme-card-enter-active,
.meme-card-leave-active {
  transition: all 0.5s ease;
}

.meme-card-enter-from,
.meme-card-leave-to {
  opacity: 0;
  transform: translateX(30px);
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