import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'
import store from './store'
import ganttastic from '@infectoone/vue-ganttastic';

createApp(App).use(store).use(router).use(ElementPlus).use(ganttastic).mount('#app')
