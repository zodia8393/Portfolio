<template>
  <div class="user-profile page-container">
    <h1>사용자 프로필</h1>
    <div v-if="user" class="profile-info">
      <!-- 사용자 정보 표시 -->
      <img :src="user.avatar" alt="User Avatar" class="avatar">
      <h2>{{ user.username }}</h2>
      <p>이메일: {{ user.email }}</p>
      <p>가입일: {{ formatDate(user.createdAt) }}</p>
      
      <!-- 사용자 선호 옵션 표시 -->
      <h3>선호 옵션</h3>
      <ul>
        <li v-for="preference in user.preferences" :key="preference.id">
          {{ preference.category }}: {{ preference.value }}
        </li>
      </ul>
      
      <!-- 최근 선택한 식당 목록 표시 -->
      <h3>최근 선택</h3>
      <ul>
        <li v-for="selection in recentSelections" :key="selection.id">
          {{ selection.restaurant.name }} - {{ formatDate(selection.date) }}
        </li>
      </ul>
      
      <!-- 프로필 수정 버튼 -->
      <button @click="showEditModal = true">프로필 수정</button>
    </div>
    <p v-else>로딩 중...</p>

    <!-- 프로필 수정 모달 -->
    <modal v-if="showEditModal" @close="showEditModal = false">
      <template v-slot:header>
        <h3>프로필 수정</h3>
      </template>
      <template v-slot:body>
        <form @submit.prevent="updateProfile">
          <input v-model="editedUser.username" placeholder="사용자 이름" required>
          <input v-model="editedUser.email" type="email" placeholder="이메일" required>
          <button type="submit">저장</button>
        </form>
      </template>
    </modal>
  </div>
</template>
  
<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Modal from '@/components/Modal.vue';

export default {
  name: 'UserProfile',
  components: { Modal },
  setup() {
    const store = useStore();
    const showEditModal = ref(false);
    const editedUser = ref({});

    // Vuex 스토어에서 사용자 정보와 최근 선택 가져오기
    const user = computed(() => store.state.user.user);
    const recentSelections = computed(() => store.state.user.recentSelections);

    // 컴포넌트 마운트 시 사용자 프로필과 최근 선택 정보 가져오기
    onMounted(async () => {
      await store.dispatch('user/fetchUserProfile');
      await store.dispatch('user/fetchRecentSelections');
    });

    // 날짜 형식 변환 함수
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    // 프로필 업데이트 함수
    const updateProfile = async () => {
      await store.dispatch('user/updateUserProfile', editedUser.value);
      showEditModal.value = false;
    };

    return {
      user,
      recentSelections,
      showEditModal,
      editedUser,
      formatDate,
      updateProfile,
    };
  },
};
</script>
  
  <style scoped>
  .user-profile {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  h1, h2, h3 {
    color: #FFD700;
    text-shadow: 2px 2px 4px #000;
  }
  
  h1 {
    font-size: 4vw;
    margin-bottom: 3vh;
  }
  
  h2 {
    font-size: 3vw;
    margin-bottom: 2vh;
  }
  
  h3 {
    font-size: 2.5vw;
    margin: 2vh 0;
  }
  
  .avatar {
    width: 20vw;
    height: 20vw;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 2vh;
  }
  
  .profile-info {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 3vw;
    border-radius: 10px;
    width: 80%;
    max-width: 600px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    font-size: 2vw;
    margin-bottom: 1vh;
  }
  
  button {
    margin-top: 3vh;
    padding: 1vh 2vw;
    font-size: 2vw;
    background-color: #FFD700;
    color: #000;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #FFC800;
  }
  
  @media (max-width: 768px) {
    h1 { font-size: 6vw; }
    h2 { font-size: 5vw; }
    h3 { font-size: 4vw; }
    .avatar { width: 40vw; height: 40vw; }
    li { font-size: 4vw; }
    button { font-size: 4vw; }
  }
  </style>
  