// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/components/Home.vue'),
  },
  {
    path: '/Leaderboard',
    component: () => import('@/components/Leaderboard.vue'),
  },
  {
    path: '/Game',
    component: () => import('@/components/Game.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
