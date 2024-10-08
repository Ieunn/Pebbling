<template>
  <div :class="{'dark': isDarkMode}" class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white flex flex-col">
    <div class="flex-grow flex flex-col max-w-md w-full mx-auto px-4 py-4">
      <header class="flex justify-between items-center mb-4">
        <nav class="flex space-x-4">
          <router-link to="/" class="text-lg font-semibold text-gray-700 dark:text-gray-300 hover:text-blue-500 dark:hover:text-blue-400">Home</router-link>
          <router-link to="/favorites" class="text-lg font-semibold text-gray-700 dark:text-gray-300 hover:text-blue-500 dark:hover:text-blue-400">Favorites</router-link>
        </nav>
        <div class="flex items-center space-x-4">
          <div class="relative">
            <select v-model="memeStore.selectedSource" @change="memeStore.handleSourceChange" class="appearance-none bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md py-2 pl-3 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">All Sources</option>
              <option v-for="source in memeStore.sources" :key="source" :value="source">{{ source }}</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 dark:text-gray-300">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
          <button @click="toggleDarkMode" class="p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
            <svg v-if="isDarkMode" class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            <svg v-else class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
          </button>
        </div>
      </header>
      <router-view class="flex-grow flex flex-col"></router-view>
      <footer class="mt-4 text-center">
        <AdComponent />
      </footer>
    </div>
    <FullScreenImage v-if="fullScreenImage" :image-url="fullScreenImage" @close="fullScreenImage = null" />
    <div v-if="memeStore.showAuthModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg max-w-sm w-full">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">授权小红书账号</h2>
        <p class="mb-4 text-gray-700 dark:text-gray-300">为了获取小红书的内容，我们需要您的授权。请点击下面的按钮登录小红书。</p>
        <div class="flex justify-end space-x-4">
          <button @click="cancelAuth" class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors">取消</button>
          <button @click="authXiaohongshu" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition-colors">登录小红书</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, provide, watch } from 'vue'
import { useMemeStore } from './stores/memeStore'
import FullScreenImage from './components/FullScreenImage.vue'
import AdComponent from './components/AdComponent.vue'

export default {
  name: 'App',
  components: {
    AdComponent,
    FullScreenImage,
  },
  setup() {
    const fullScreenImage = ref(null)
    const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
    const memeStore = useMemeStore()

    provide('setFullScreenImage', (imageUrl) => {
      fullScreenImage.value = imageUrl
    })

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value)
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
    
    const authXiaohongshu = async () => {
      const authWindow = window.open('https://www.xiaohongshu.com/login', '_blank');

      return new Promise((resolve, reject) => {
        window.addEventListener('message', async (event) => {
          if (event.origin === 'https://www.xiaohongshu.com' && event.data.type === 'login_success') {
            authWindow.close();
            memeStore.showAuthModal = false;
            
            setTimeout(async () => {
              try {
                await memeStore.scrapeMemes();
                resolve();
              } catch (error) {
                reject(error);
              }
            }, 1000);
          }
        });
      });
    }

    const cancelAuth = () => {
      memeStore.showAuthModal = false
      memeStore.selectedSource = ''
      memeStore.memes = []
    }

    onMounted(() => {
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
      }
      memeStore.fetchSources()
    })

    watch(() => memeStore.selectedSource, async (newSource) => {
      if (newSource === 'Xiaohongshu') {
        if (!memeStore.checkXiaohongshuCookies()) {
          memeStore.showAuthModal = true
        } else {
          await memeStore.handleSourceChange()
        }
      } else {
        await memeStore.handleSourceChange()
      }
    })

    return {
      isDarkMode,
      toggleDarkMode,
      fullScreenImage,
      memeStore,
      authXiaohongshu,
      cancelAuth
    }
  }
}
</script>