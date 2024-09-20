<template>
    <div class="favorite-meme-card bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div class="relative aspect-w-3 aspect-h-4">
            <img :src="meme.imageUrl" :alt="meme.title" class="w-full h-full object-cover" />
            <div class="absolute inset-0 bg-black bg-opacity-50 opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <button @click="$emit('show-full-screen', meme.imageUrl)" class="bg-white dark:bg-gray-800 p-2 rounded-full shadow-md">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path>
                    </svg>
                </button>
            </div>
        </div>
        <div class="p-4">
            <h3 class="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">{{ meme.title }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">Source: {{ meme.source }}</p>
            <button @click="$emit('remove-favorite', meme._id)" class="mt-4 w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">
                Remove from Favorites
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FavoriteMemeCard',
    props: {
        meme: {
        type: Object,
        required: true
        }
    },
    emits: ['remove-favorite', 'show-full-screen']
}
</script>