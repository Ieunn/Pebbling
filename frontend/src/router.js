import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Favorites from './components/Favorites.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: App
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: Favorites
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router