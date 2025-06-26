<template>
  <div id="app">
    <header>
      <!-- 로고 이미지 표시 -->
      <img :src="require('@/assets/images/logo.png')" alt="Logo" class="logo">
      <nav>
        <!-- 네비게이션 링크 -->
        <router-link to="/">Home</router-link> |
        <router-link to="/profile">Profile</router-link> |
        <a href="#" @click.prevent="logout">Logout</a>
      </nav>
    </header>
    <main>
      <!-- 라우터 뷰 컴포넌트 표시 -->
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'App',
  methods: {
    // Vuex 스토어의 auth 모듈에서 logout 액션을 가져옴
    ...mapActions('auth', ['logout'])
  }
}
</script>

<style>
#app {
  /* 하스스톤 선술집 스타일 CSS 파일 임포트 */
  @import './assets/hearthstone-tavern.css';
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body {
  margin: 0;
  padding: 0;
  /* 배경 이미지 설정 */
  background-image: url('./assets/images/tavern-background.jpg');
  background-size: cover;
  background-attachment: fixed;
}

header {
  padding: 20px;
  /* 헤더 배경색 설정 (약간 투명한 검정) */
  background-color: rgba(0, 0, 0, 0.7);
}

.logo {
  height: 50px;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #FFD700; /* 네비게이션 링크 색상 (금색) */
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #FFA500; /* 활성 링크 색상 (주황색) */
}

main {
  padding: 20px;
  /* 메인 컨텐츠 영역 배경색 설정 (약간 투명한 흰색) */
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  margin: 20px auto;
  max-width: 800px;
}
</style>
