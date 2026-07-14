<template>
    <div class="main-page">
        <div class="home-card card">
            <img src="../assets/placement.png" alt="Job Search SVG" width="250" height="250">   
            <div>
                <h1 class="page-title">Manage placement drives, applications, interviews and more...</h1>
                <p>
                    Welcome to the placement portal application! We welcome distinguished organisations and companies across different fields of work to join our hiring drive! 
                    Our students excel in the latest technologies and innovations in their respective fields of study,
                    while simultaneously maintaining a strong grasp of the fundamentals. Anyone looking to hire final year students from our campus for full-time jobs or semester-long internships, or our budding pre-final year students for 2-month internships, this is the place!
                </p>
            </div>
        </div>
        <div class="cards mb-24" :style="gridStyle">
            <router-link v-for="card in currentCards" :key="card.link" :to="card.link">
                <div class="card clickable">  
                    <i :class="card.icon"></i>
                    <h2 class="section-heading mb-8">{{ card.title }}</h2>
                    <p>{{ card.message }}</p>
                </div>
            </router-link>
        </div>
        <AppSpinner v-if="loading" />
        <div v-else class="stats-grid">
            <div class="stat-card">
                <div class="stat-card-value is-success">{{ stats.total_students }}</div>
                <div class="stat-card-label">Students</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value is-success">{{ stats.total_companies }}</div>
                <div class="stat-card-label">Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value is-success">{{ stats.total_placements }}</div>
                <div class="stat-card-label">Placements</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value is-success">{{ stats.avg_placement_salary }}</div>
                <div class="stat-card-label">Average Salary</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.home-card {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 24px;
}

.page-title {
    font-size: 2rem;
    color: var(--accent-primary-background)
}

.cards {
    display: grid;
    gap: 12px;
}

.cards > a {
    display: flex;
    text-decoration: none;
    color: inherit;
}

.clickable {
    flex: 1;
    cursor: pointer;
    color: var(--surface-foreground);
}

.clickable:hover {
    transform: translateY(-1px);
}

.clickable i {
    font-size: 40px;
    margin-bottom: 16px;
    color: var(--accent-primary-background);
}

.stats-grid {
    grid-template-columns: repeat(4, 1fr);
}

</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { computed, onMounted, ref } from 'vue';

const authStore = useAuthStore();
const notify = useNotificationStore();
const loading = ref(true);
const stats = ref({});

onMounted(fetchDashboard);

const link_cards = {
    admin: [
        {
            link: '/admin',
            icon: 'fas fa-chart-line',
            title: 'View Dashboard',
            message: 'View a complete summary of companies, drives, students, placements...'
        },
        {
            link: '/admin/companies',
            icon: 'fas fa-building',
            title: 'Manage Companies',
            message: 'Search, filter, and manage companies - even blacklist unethical organizations'
        },
        {
            link: '/admin/drives',
            icon: 'fas fa-briefcase',
            title: 'Manage Drives',
            message: 'View and manage the drives organised by companies'
        },
        {
            link: '/admin/students',
            icon: 'fas fa-user-graduate',
            title: 'Manage Students',
            message: 'View all registered students, deactivate graduates, blacklist students'
        },
        {
            link: '/admin/applications',
            icon: 'fas fa-file-alt',
            title: 'View Applications',
            message: 'View all applications made by students for different placement drives'
        },
        {
            link: '/admin/placements',
            icon: 'fas fa-trophy',
            title: 'View Placements',
            message: 'View details of all the students who have been placed as of now'
        }
    ],
    company: [
        {
            link: '/company',
            icon: 'fas fa-chart-line',
            title: 'View Dashboard',
            message: 'View a complete summary of different KPIs of your drives, students, applications...'
        },
        {
            link: '/company/profile',
            icon: 'fas fa-building',
            title: 'Manage Profile',
            message: 'View and update your profile details, point of communication...'
        },
        {
            link: '/company/drives',
            icon: 'fas fa-briefcase',
            title: 'Manage Drives',
            message: 'Create and manage placement drives, applications, and interviews for 3rd year and final year students'
        }
    ],
    student: [
        {
            link: '/student',
            icon: 'fas fa-chart-line',
            title: 'View Dashboard',
            message: 'View a complete summary of your activity in this portal, including placement details, drives you have been shortlisted for...'
        },
        {
            link: '/student/profile',
            icon: 'fas fa-user',
            title: 'Manage Profile',
            message: 'Manage your profile, update your skills, CGPA, and resume with your academic and learning progress'
        },
        {
            link: '/student/drives',
            icon: 'fas fa-briefcase',
            title: 'View and Apply to Drives',
            message: 'View drives that you are eligible for, filter by your salary expectations, and apply to them'
        },
        {
            link: '/student/applications',
            icon: 'fas fa-file-alt',
            title: 'Manage Applications',
            message: 'View all of your applications, their current statuses, your interview details, and also withdraw your application if necessary'
        },
    ],
    no_role: [
        {
            link: '/login',
            icon: 'fas fa-user-shield',
            title: 'Login',
            message: 'Already registered and verified? You can login to the portal and access it.'
        },
        {
            link: '/verify-otp',
            icon: 'fas fa-lock-open',
            title: 'Verify OTP',
            message: 'Already registered as student? Verify the OTP sent to your email to access the portal!'
        },
        {
            link: '/register/company',
            icon: 'fas fa-building',
            title: 'Register as Company',
            message: 'Register and organize placement drives for the students of our institution with ease through this portal! You can login after registration and admin approval.'
        },
        {
            link: '/register/student',
            icon: 'fas fa-user',
            title: 'Register as Student',
            message: '3rd and 4th year students can register with their university email addresses!'
        },
    ]
}

const currentCards = computed(() => link_cards[authStore.userRole] ?? link_cards.no_role);
const gridStyle = computed(() => ({gridTemplateColumns: `repeat(${currentCards.value.length}, 1fr)`}));

async function fetchDashboard() {
    loading.value = true;
    try {
        const result = await api.get('/shared/dashboard');
        stats.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to fetch portal statistics');
    } finally {
        loading.value = false;
    }
}
</script>