<template>
    <div class="main-page">
        <h1 class="page-title text-center">Profile</h1>
        <AppSpinner v-if="loading" />
        <template v-else>
            <div class="card">
                <h2 class="card-title">Account Information</h2>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label for="register_no" class="form-label">Register No.</label>
                        <input id="register_no" type="text" class="form-input" readonly v-model="profile.register_no">
                    </div>
                    <div class="flex-1">
                        <label for="email" class="form-label">University Email Address</label>
                        <input id="email" type="text" class="form-input" readonly v-model="profile.email">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-2">
                        <label for="branch_name" class="form-label">Branch Name</label>
                        <input id="branch_name" type="text" class="form-input" readonly v-model="profile.branch_name">
                    </div>
                    <div class="flex-1">
                        <label for="year_of_study" class="form-label">Year</label>
                        <input id="year_of_study" type="text" class="form-input" readonly v-model="profile.year_of_study">
                    </div>
                    <div class="flex-1">
                        <label for="created_at" class="form-label">Created At</label>
                        <input id="created_at" type="text" class="form-input" readonly v-model="profile.created_at">
                    </div>
                </div>      
            </div>  
            <div class="card">
                <h2 class="card-title">Editable Details</h2>
                <form @submit.prevent="saveProfile">
                    <div class="form-group flex gap-16">
                        <div class="flex-1">
                            <label class="form-label" for="fname">First Name</label>
                            <input id="fname" type="text" class="form-input" v-model="studentProfile.fname">
                        </div>
                        <div class="flex-1">
                            <label class="form-label" for="lname">Last Name</label>
                            <input id="lname" type="text" class="form-input" v-model="studentProfile.lname">
                        </div>
                    </div>
                    <div class="form-group flex gap-16">
                        <div class="flex-2">
                            <label class="form-label" for="dob">Date of Birth</label>
                            <input id="dob" type="date" class="form-input" v-model="studentProfile.dob">
                        </div>
                        <div class="flex-2">
                            <label class="form-label" for="phone">Phone Number</label>
                            <input id="phone" type="text" class="form-input" v-model="studentProfile.phone">
                        </div>
                        <div class="flex-1">
                            <label class="form-label" for="cgpa">CGPA</label>
                            <input id="cgpa" type="text" class="form-input" v-model="studentProfile.cgpa">
                        </div>
                    </div>  
                    <div class="form-group">
                        <label for="skills" class="form-label mb-16">Select/Deselect Your Skills</label>
                        <AppMultiSelect
                        v-model="studentProfile.skill_ids"
                        :options="skills"
                        value="skill_name"
                        id="skill_id"
                    />     
                    </div> 
                    <div class="form-group">
                        <label for="resume" class="form-label">Resume</label>
                        <AppFileUpload
                            v-model="resume"
                            :file="profile.resume"
                            @download="downloadResume"
                            accept=".pdf,.doc,.docx"
                            hint="Accepted formats: PDF, DOC, DOCX"
                        />
                    </div>
                    <button type="submit" class="btn is-primary full-width-btn" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button> 
                </form>                
            </div>
        </template>
    </div>
</template>

<style scoped>
.card {
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 24px;
}
</style>

<script setup>
import AppFileUpload from '@/components/ui/AppFileUpload.vue';
import AppMultiSelect from '@/components/ui/AppMultiSelect.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { onMounted, reactive, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const saving = ref(false);
const profile = ref({});
const skills = ref([]);
const resume = ref(null);

const studentProfile = reactive({
    fname: '',
    lname: '',
    dob: '',
    phone: '',
    cgpa: '',
    skill_ids: []
});

onMounted(fetchProfile);

async function fetchProfile() {
    try {
        const [profileResult, skillsResult] = await Promise.all([
            api.get('/student/profile'),
            api.get('/shared/skills')
        ]);
        profile.value = profileResult.data;
        skills.value = skillsResult.data.skills;
        profile.value.created_at = formatDateTime(profile.value.created_at);
        Object.assign(studentProfile, profile.value);
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load profile');
    } finally {
        loading.value = false;
    }
}

async function saveProfile() {
    saving.value = true;
    try {
        const result = await api.put('/student/profile', studentProfile);        
        notify.success(result.data?.message || 'Profile updated successfully');
        const resumeResult = await uploadResume();
        if (resumeResult) notify.success(resumeResult.data?.message || 'Resume updated successfully');
        fetchProfile();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to update profile');
    } finally {
        saving.value = false;
    }
}

async function uploadResume() {
    if (!resume.value) return;

    const formData = new FormData();
    formData.append('resume', resume.value);

    const result = await api.post('/student/resume', formData, {
        headers: {'Content-Type': 'multipart/form-data'}
    });
    resume.value = null;
    return result;
}

async function downloadResume() {
    try {
        const result = await api.get('student/resume', { responseType: 'blob'} );
        const url = window.URL.createObjectURL(new Blob([result.data]));
        const link = document.createElement('a');
        link.href = url;
        link.download = profile.value.resume || 'resume.pdf';
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        notify.error('Failed to download resume');
    }
}
</script> 