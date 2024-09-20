<template>
    <div class="flex flex-col h-full">
        <main class="flex-grow relative flex items-center justify-center">
            <div v-if="memeStore.loading" class="absolute inset-0 flex items-center justify-center">
                <p>Loading memes...</p>
            </div>
            <TransitionGroup v-else name="meme-card" tag="div" class="relative w-full h-full flex items-center justify-center">
                <MemeCard 
                v-for="(meme, index) in displayedMemes" 
                :key="meme._id || 'empty'"
                :meme="meme"
                :is-empty="memeStore.memes.length === 0"
                :style="{ zIndex: displayedMemes.length - index }"
                @swipe="handleSwipe"
                />
            </TransitionGroup>
        </main>
    </div>
    <div v-if="memeStore.showAuthModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg">
        <h2 class="text-xl font-bold mb-4">授权小红书账号</h2>
        <p class="mb-4">为了获取小红书的内容，我们需要您的授权。请点击下面的按钮登录小红书。</p>
        <button @click="authXiaohongshu" class="bg-red-500 text-white px-4 py-2 rounded">登录小红书</button>
        <button @click="cancelAuth" class="ml-4 text-gray-600">取消</button>
      </div>
    </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useMemeStore } from '../stores/memeStore'
import MemeCard from './MemeCard.vue'

export default {
    name: 'Home',
    components: {
        MemeCard
    },
    setup() {
        const memeStore = useMemeStore()

        const displayedMemes = computed(() => {
            if (memeStore.memes.length === 0) {
                return [{ _id: 'empty', isEmpty: true }]
            }
            return memeStore.memes
        })

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
            memeStore.showAuthModal = false
            memeStore.selectedSource = ''
            memeStore.memes = []
        }

        const handleSwipe = (memeId, action, direction) => {
            memeStore.handleSwipe(memeId, action)
            const memeElement = document.querySelector(`[data-meme-id="${memeId}"]`)
            if (memeElement) {
                memeElement.dataset.direction = direction
            }
            setTimeout(() => {
                memeStore.handleSwipe(memeId, action)
            }, 500)
        }

        onMounted(() => {
            memeStore.fetchMemes()
        })

        return {
            memeStore,
            displayedMemes,
            authXiaohongshu,
            cancelAuth,
            handleSwipe
        }
    }
}
</script>
  
<style scoped>
.meme-card-leave-active {
  transition: all 0.5s ease-out;
  position: absolute;
}

.meme-card-leave-to[data-direction="left"] {
  transform: translateX(-120%) rotate(-10deg);
  opacity: 0;
}

.meme-card-leave-to[data-direction="right"] {
  transform: translateX(120%) rotate(10deg);
  opacity: 0;
}

.meme-card-leave-to[data-direction="up"] {
  transform: translateY(-120%) rotate(5deg);
  opacity: 0;
}
</style>