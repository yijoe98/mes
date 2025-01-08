import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import ProductionTrackingView from '@/views/ProductionTrackingView.vue'
import QualityControlView from '@/views/QualityControlView.vue'
import HomeView from '@/views/DashboardView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Dashboard',
    component: HomeView
  },
  {
    path: '/production',
    name: 'Production',
    component: ProductionTrackingView
  },
  {
    path: '/quality',
    name: 'Quality',
    component: QualityControlView
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
