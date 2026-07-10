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
    {
      path: '/admin/students',
      name: 'admin-students',
      component: () => import('@/views/admin/AdminStudents.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/applications',
      name: 'admin-applications',
      component: () => import('@/views/admin/AdminApplications.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/placements',
      name: 'admin-placements',
      component: () => import('@/views/admin/AdminPlacements.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/company',
      name: 'company-dashboard',
      component: () => import('@/views/company/CompanyDashboard.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/profile',
      name: 'company-profile',
      component: () => import('@/views/company/CompanyProfile.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drives',
      name: 'company-drives',
      component: () => import('@/views/company/CompanyDrives.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drives/:id',
      name: 'company-drive-detail',
      component: () => import('@/views/company/CompanyDriveDetail.vue'),
      meta: { requiresAuth: true, role: 'company' }
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
  ]
})

export default router;