<template>
    <div class="flex-grow flex items-center justify-center">
        <div v-if="memeStore.loading" class="text-center">
            <p>Loading memes...</p>
        </div>
        <div v-else class="relative w-full aspect-[3/4] max-w-sm max-h-[80vh]">
            <TransitionGroup name="meme-card" tag="div" class="absolute inset-0">
                <MemeCard 
                v-for="(meme, index) in displayedMemes" 
                    :key="meme._id || 'empty'"
                    :meme="meme"
                    :is-empty="memeStore.memes.length === 0"
                    :style="{ zIndex: displayedMemes.length - index }"
                    @swipe="handleSwipe"
                />
            </TransitionGroup>
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

        const handleSwipe = (memeId, action, direction) => {
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