import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './index.css'
import Vue3TouchEvents from "vue3-touch-events";

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
   .use(router)
   .use(Vue3TouchEvents)
   .mount('#app')