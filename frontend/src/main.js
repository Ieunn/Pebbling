import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import './index.css'
import Vue3TouchEvents from "vue3-touch-events";

createApp(App)
  .use(router)
  .use(Vue3TouchEvents)
  .mount('#app')