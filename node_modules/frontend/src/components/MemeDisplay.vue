<template>
  <div class="meme-container" v-if="meme">
    <img :src="meme.imageUrl" :alt="meme.title" />
    <h2>{{ meme.title }}</h2>
    <p>Source: {{ meme.source }}</p>
  </div>
</template>

<script>
export default {
  name: 'MemeDisplay',
  props: {
    meme: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.meme-container {
  max-width: 500px;
  text-align: center;
}
img {
  max-width: 100%;
  height: auto;
}
</style>