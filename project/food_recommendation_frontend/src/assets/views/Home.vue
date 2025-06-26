<template>
    <div class="home">
      <div class="tavern-door" :class="{ 'open': doorOpen }">
        <img :src="require('@/assets/images/tavern-door.gif')" alt="Tavern Door" class="door-gif">
      </div>
      <transition name="fade">
        <img v-if="logoVisible" :src="require('@/assets/images/logo.png')" alt="Logo" class="logo">
      </transition>
      <transition name="fade">
        <h1 v-if="textVisible" class="welcome-text">Smart Lunch Mate에 오신 것을 환영합니다</h1>
      </transition>
      <transition name="fade">
        <button v-if="buttonVisible" @click="startQuest" class="start-button" :style="{ backgroundImage: `url(${require('@/assets/images/button-background.png')})` }">
          Start
        </button>
      </transition>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Home',
    setup() {
      const router = useRouter();
      const doorOpen = ref(false);
      const logoVisible = ref(false);
      const textVisible = ref(false);
      const buttonVisible = ref(false);
  
      const startAnimation = () => {
        doorOpen.value = true;
        setTimeout(() => {
          logoVisible.value = true;
          setTimeout(() => {
            logoVisible.value = false;
            setTimeout(() => {
              textVisible.value = true;
              buttonVisible.value = true;
            }, 1000);
          }, 2000);
        }, 3000);
      };
  
      const startQuest = () => {
        router.push('/decision');
      };
  
      onMounted(startAnimation);
  
      return {
        doorOpen,
        logoVisible,
        textVisible,
        buttonVisible,
        startQuest
      };
    }
  };
  </script>
  
  <style scoped>
  .home {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-image: url('@/assets/images/tavern-background.jpg');
    background-size: cover;
    background-position: center;
    overflow: hidden;
  }
  
  .tavern-door {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    transition: opacity 1s ease-in-out;
  }
  
  .tavern-door.open {
    opacity: 0;
  }
  
  .door-gif {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .logo {
    width: 300px;
    height: auto;
    margin-bottom: 30px;
  }
  
  .welcome-text {
    font-size: 2.5em;
    color: #FFD700;
    text-shadow: 2px 2px 4px #000;
    margin-bottom: 30px;
    text-align: center;
  }
  
  .start-button {
    margin-top: 20px;
    font-size: 1.5em;
    padding: 15px 30px;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    border: none;
    color: #FFD700;
    text-shadow: 2px 2px 2px #000;
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  
  .start-button:hover {
    transform: scale(1.1);
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  </style>
  