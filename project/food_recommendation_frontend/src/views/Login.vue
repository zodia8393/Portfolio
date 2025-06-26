<template>
  <div class="login">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>로그인</h2>
      <div class="form-group">
        <input 
          v-model="email" 
          type="email" 
          placeholder="이메일"
          required
          class="form-input"
        >
      </div>
      <div class="form-group">
        <input 
          v-model="password" 
          type="password" 
          placeholder="비밀번호"
          required
          class="form-input"
        >
      </div>
      <button type="submit" class="login-button">로그인</button>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  setup() {
    const store = useStore();
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const error = ref('');

    // 로그인 처리 함수
    const handleLogin = async () => {
      try {
        error.value = ''; // 에러 메시지 초기화
        // Vuex 액션을 통해 로그인 시도
        await store.dispatch('auth/login', {
          email: email.value,
          password: password.value
        });
        router.push('/decision'); // 로그인 성공 시 decision 페이지로 이동
      } catch (err) {
        // 로그인 실패 시 에러 메시지 설정
        error.value = '로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.';
        console.error('Login failed:', err);
      }
    };

    return {
      email,
      password,
      error,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-image: url('~@/assets/images/tavern-background.jpg');
  background-size: cover;
  background-position: center;
}

.login-form {
  background: rgba(0, 0, 0, 0.8);
  padding: 2rem;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

h2 {
  color: #FFD700;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 24px;
}

.form-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 5px;
  color: #FFD700;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: #FFD700;
  color: #000;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.login-button:hover {
  background: #FFC800;
}
</style>
