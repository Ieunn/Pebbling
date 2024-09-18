<template>
  <div :class="['min-h-screen transition-colors duration-300', isDarkMode ? 'dark bg-gray-900 text-white' : 'bg-gray-100 text-gray-900']">
    <div class="container mx-auto px-4 py-8">
      <header class="mb-8">
        <h1 class="text-4xl font-bold text-center mb-4">Pebbling</h1>
        <div class="flex justify-center items-center space-x-4">
          <div class="relative">
            <select v-model="selectedSource" @change="resetAndFetchMemes" class="appearance-none bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md py-2 pl-3 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">All Sources</option>
              <option v-for="source in sources" :key="source" :value="source">{{ source }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 dark:text-gray-300">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
          <button @click="toggleDarkMode" class="p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
            <svg v-if="isDarkMode" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
          </button>
        </div>
      </header>
      <main class="mb-8">
        <div class="relative w-full max-w-md mx-auto h-96">
          <TransitionGroup name="meme-card" tag="div" class="absolute inset-0">
            <MemeCard 
              v-for="(meme, index) in memes" 
              :key="meme._id"
              :meme="meme"
              :style="{ zIndex: memes.length - index }"
              @swipe="handleSwipe"
              class="absolute inset-0"
            />
          </TransitionGroup>
        </div>
      </main>
      <footer class="text-center">
        <router-link to="/favorites" class="inline-block px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors duration-300">My Favorites</router-link>
        <AdComponent class="mt-4" />
      </footer>
    </div>
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
.meme-card-enter-active,
.meme-card-leave-active {
  transition: all 0.5s ease;
}

.meme-card-enter-from,
.meme-card-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>