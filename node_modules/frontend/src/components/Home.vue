<template>
    <div class="container mx-auto px-4 py-8">
        <header class="mb-8">
            <h1 class="text-4xl font-bold text-center mb-4">Pebbling</h1>
            <div class="flex justify-center items-center space-x-4">
                <div class="relative">
                    <select v-model="selectedSource" @change="handleSourceChange" class="appearance-none bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md py-2 pl-3 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="">All Sources</option>
                        <option v-for="source in sources" :key="source" :value="source">{{ source }}</option>
                    </select>
                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700 dark:text-gray-300">
                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                    </div>
                </div>
                <div v-if="showAuthModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                    <div class="bg-white p-6 rounded-lg">
                        <h2 class="text-xl font-bold mb-4">授权小红书账号</h2>
                        <p class="mb-4">为了获取小红书的内容，我们需要您的授权。请点击下面的按钮登录小红书。</p>
                        <button @click="authXiaohongshu" class="bg-red-500 text-white px-4 py-2 rounded">登录小红书</button>
                        <button @click="cancelAuth" class="ml-4 text-gray-600">取消</button>
                    </div>
                </div>
            </div>
        </header>
        <main class="mb-8">
            <div class="relative w-full mx-auto flex justify-center items-center" style="height: 80vh;">
            <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
                <p>Loading memes...</p>
            </div>
            <TransitionGroup v-else name="meme-card" tag="div" class="relative" style="aspect-ratio: 3/4; width: 90%; max-width: 400px; max-height: 100%;">
                <MemeCard 
                v-for="(meme, index) in displayedMemes" 
                :key="meme._id || 'empty'"
                :meme="meme"
                :is-empty="memes.length === 0"
                :style="{ zIndex: displayedMemes.length - index }"
                @swipe="handleSwipe"
                />
            </TransitionGroup>
            </div>
        </main>
        <footer class="text-center">
            <AdComponent class="mt-4" />
        </footer>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, watch } from 'vue'
  import axios from 'axios'
  import MemeCard from './MemeCard.vue'
  import AdComponent from './AdComponent.vue'
  
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
      const loading = ref(true)
      const error = ref(null)
  
      const showAuthModal = ref(false)
  
      const checkXiaohongshuCookies = () => {
        const cookies = document.cookie;
        return cookies.includes('xhsTrackerId') || cookies.includes('websectokenx');
      }
  
      const handleSourceChange = async () => {
        if (selectedSource.value === 'Xiaohongshu') {
          memes.value = memes.value.filter((meme) => { return meme.source == 'Xiaohongshu' })
          if (checkXiaohongshuCookies()) {
            if (memes.value.length > 0) {
              console.log('Using existing memes');
            } else {
              await scrapeMemes();
            }
          }
          else {
            showAuthModal.value = true
          }
        } else {
          await resetAndFetchMemes()
        }
      }
  
      const scrapeMemes = async () => {
        if (memes.value.length > 0) {
          console.log('Still have unviewed memes, skipping scraping');
          return;
        }
  
        loading.value = true;
        error.value = null;
        try {
          const scrapedMemes = await scrapeXiaohongshuMemes();
          if (scrapedMemes.length > 0) {
            const response = await axios.post('/api/process_scraped_memes', { memes: scrapedMemes });
            if (response.status === 429) {
              console.log('Rate limit exceeded, fetching from server');
              await fetchMemes();
            } else {
              memes.value = response.data;
            }
          } else {
            console.log('No new memes found, fetching from server');
            await fetchMemes();
          }
        } catch (err) {
          if (err.response && err.response.status === 429) {
            console.log('Rate limit exceeded, fetching from server');
          } else {
            console.error('Error scraping memes:', err);
            error.value = 'Error scraping memes: ' + (err.response?.data?.error || err.message);
          }
          await fetchMemes();
        } finally {
          loading.value = false;
        }
      }
  
      const scrapeXiaohongshuMemes = async () => {
        const memes = [];
        const pageUrl = 'https://www.xiaohongshu.com/search_result?keyword=meme';
        
        try {
          const response = await fetch(pageUrl, {
            credentials: 'include',
            headers: {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const html = await response.text();
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          
          const noteItems = doc.querySelectorAll('.note-item');
          for (let i = 0; i < Math.min(noteItems.length, 10); i++) {
            const noteItem = noteItems[i];
            const titleElement = noteItem.querySelector('.note-title');
            const linkElement = noteItem.querySelector('a');
            
            if (titleElement && linkElement) {
              const title = titleElement.textContent.trim();
              const noteUrl = 'https://www.xiaohongshu.com' + linkElement.getAttribute('href');
              
              const noteResponse = await fetch(noteUrl, {
                credentials: 'include',
                headers: {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
              });
              
              if (noteResponse.ok) {
                const noteHtml = await noteResponse.text();
                const noteDoc = parser.parseFromString(noteHtml, 'text/html');
                
                const imageElements = noteDoc.querySelectorAll('.note-img');
                for (const imageElement of imageElements) {
                  const imageUrl = imageElement.src;
                  if (imageUrl) {
                    memes.push({
                      title: title,
                      imageUrl: imageUrl,
                      originalUrl: noteUrl
                    });
                  }
                }
              }
            }
            
            if (memes.length >= 20) break;
          }
        } catch (error) {
          console.error('Error scraping Xiaohongshu:', error);
        }
        
        return memes;
      }
  
      const authXiaohongshu = async () => {
        const authWindow = window.open('https://www.xiaohongshu.com/login', '_blank');
  
        return new Promise((resolve, reject) => {
          window.addEventListener('message', async (event) => {
            if (event.origin === 'https://www.xiaohongshu.com' && event.data.type === 'login_success') {
              authWindow.close();
              showAuthModal.value = false;
              
              setTimeout(async () => {
                try {
                  await scrapeMemes();
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
        showAuthModal.value = false
        selectedSource.value = ''
      }
  
      const displayedMemes = computed(() => {
        if (memes.value.length === 0) {
          return [{ _id: 'empty', isEmpty: true }]
        }
        return memes.value
      })
  
      const fetchSources = async () => {
        try {
          const response = await axios.get('/api/get_sources')
          sources.value = response.data
          if (sources.value.length > 0) {
            if (!sources.value.includes('Xiaohongshu')) {
              sources.value.push('Xiaohongshu')
            }
            if (!selectedSource.value) {
              selectedSource.value = localStorage.getItem('lastSelectedSource') || sources.value[0]
            }
          }
        } catch (error) {
          console.error('Error fetching sources:', error)
        }
      }
      
      const fetchMemes = async (count = 5) => {
        loading.value = true
        error.value = null
        try {
          const response = await axios.get('/api/get_memes', {
            params: { 
              source: selectedSource.value,
              exclude: viewedMemes.value,
              count: count
            }
          })
          if (response.data && response.data.length > 0) {
            memes.value = response.data
          } else {
            memes.value = []
          }
        } catch (err) {
          console.error('Error fetching memes:', err)
          error.value = 'Error fetching memes: ' + (err.response?.data?.error || err.message)
        } finally {
          loading.value = false
        }
      }
  
      const resetAndFetchMemes = () => {
        memes.value = []
        fetchMemes()
        localStorage.setItem('lastSelectedSource', selectedSource.value)
      }
  
      const handleSwipe = async (memeId, action, direction) => {
        if (memeId !== 'empty') {
          viewedMemes.value.push(memeId)
          localStorage.setItem('viewedMemes', JSON.stringify(viewedMemes.value))
  
          try {
            await axios.post('/api/update_meme_status', { memeId, action })
            if (action === 'favorite') {
              console.log('Meme added to favorites')
            }
          } catch (error) {
            console.error(`Error updating meme status:`, error)
          }
        }
  
        setTimeout(() => {
          memes.value.shift()
          if (memes.value.length < 3) {
            fetchMemes(3)
          }
        }, 300)
      }
  
      onMounted(() => {
        fetchSources().then(() => {
          fetchMemes()
        })
      })
  
      watch(selectedSource, resetAndFetchMemes)
  
      return {
        memes,
        displayedMemes,
        selectedSource,
        sources,
        handleSwipe,
        loading,
        error,
        showAuthModal,
        handleSourceChange,
        authXiaohongshu,
        cancelAuth,
      }
    }
  }
  </script>
  
  <style>
  .meme-card-leave-active {
    transition: all 0.3s ease-out;
    position: absolute;
    width: 100%;
    height: 100%;
  }
  
  .meme-card-leave-to {
    opacity: 0;
    transform: translateX(100%) rotate(10deg);
  }
  
  .meme-card-leave-to[data-direction="left"] {
    transform: translateX(-100%) rotate(-10deg);
  }
  
  .meme-card-leave-to[data-direction="up"] {
    transform: translateY(-100%) rotate(5deg);
  }
  </style>