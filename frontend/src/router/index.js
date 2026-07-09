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
    {
      path: '/verify-otp',
      name: 'verify-otp',
      component: () => import('@/views/VerifyOTPPage.vue'),
    },    
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('@/views/admin/AdminDashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/companies',
      name: 'admin-companies',
      component: () => import('@/views/admin/AdminCompanies.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/drives',
      name: 'admin-drives',
      component: () => import('@/views/admin/AdminDrives.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
    // {
    //   path: '',
    //   name: '',
    //   component: () => import('@/'),
    //   meta: { requiresAuth: true, role: '' }
    // },
  ]
})

export default router;