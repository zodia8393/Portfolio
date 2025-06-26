import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import DecisionProcess from '@/views/DecisionProcess.vue';
import FinalSelection from '@/views/FinalSelection.vue';
import Result from '@/views/Result.vue';
import UserProfile from '@/views/UserProfile.vue';
import ReviewPage from '@/views/ReviewPage.vue';
import Admin from '@/views/Admin.vue';
import SelectMode from '@/views/SelectMode.vue';  // 추가
import FormDecision from '@/views/FormDecision.vue';  // 추가

const routes = [
  { 
    path: '/', 
    name: 'Home', 
    component: Home 
  },
  { 
    path: '/decision', 
    name: 'DecisionProcess', 
    component: DecisionProcess
  },
  { 
    path: '/final-selection', 
    name: 'FinalSelection', 
    component: FinalSelection
  },
  { 
    path: '/result', 
    name: 'Result', 
    component: Result
  },
  { 
    path: '/profile', 
    name: 'UserProfile', 
    component: UserProfile
  },
  { 
    path: '/review/:id', 
    name: 'ReviewPage', 
    component: ReviewPage
  },
  { 
    path: '/admin', 
    name: 'Admin', 
    component: Admin
  },
  {
    path: '/select-mode',
    name: 'SelectMode',
    component: SelectMode  // 수정
  },
  {
    path: '/form-decision',
    name: 'FormDecision',
    component: FormDecision  // 수정
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
