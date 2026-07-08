import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue'),
      meta: { guest: true}
    },
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('@/views/admin/AdminDashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/register/student',
      name: 'register-student',
      component: () => import('@/views/RegisterStudentPage.vue'),
      meta: { guest: true }
    },
     {
      path: '/register/company',
      name: 'register-company',
      component: () => import('@/views/RegisterCompanyPage.vue'),
    },
     // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    // },
     // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    // },
     // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    // },
     // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    // },
     // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    // },
  ]
})

export default router;