<template>
  <div class="decision-process">
    <div class="background-layer"></div>
    <div class="content-layer">
      <h2 class="category-title">{{ currentCategory }}</h2>
      <div class="options-container" :class="{ 'slide-out': isSlideOut }">
        <!-- 각 옵션에 대해 OptionCard 컴포넌트를 렌더링 -->
        <OptionCard 
          v-for="(option, index) in currentOptions" 
          :key="option.id" 
          :option="option"
          :isFlipped="flippedCards[index]"
          :isSelected="selectedIndex === index"
          @click="selectOption(option, index)"
        />
      </div>
      <div class="buttons-container">
        <!-- 무작위 선택 버튼 -->
        <button 
          class="random-select-button" 
          @click="randomSelect"
          :disabled="isSlideOut || isLoading">
          무작위 선택
        </button>
        <!-- 건너뛰기 버튼 -->
        <button 
          class="skip-button" 
          @click="skipCategory"
          :disabled="isSlideOut || isLoading">
          건너뛰기
        </button>
      </div>
      <!-- 로딩 오버레이 -->
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>옵션을 불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import OptionCard from '@/components/OptionCard.vue';

export default {
  name: 'DecisionProcess',
  components: {
    OptionCard
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // 현재 옵션들을 저장하는 반응형 변수
    const currentOptions = ref([]);
    // 카드 뒤집기 상태를 저장하는 반응형 변수
    const flippedCards = ref([]);
    // 슬라이드 아웃 애니메이션 상태를 저장하는 반응형 변수
    const isSlideOut = ref(false);
    // 선택된 옵션의 인덱스를 저장하는 반응형 변수
    const selectedIndex = ref(-1);
    // 로딩 상태를 저장하는 반응형 변수
    const isLoading = ref(false);

    // Vuex 스토어에서 현재 카테고리를 가져오는 계산된 속성
    const currentCategory = computed(() => store.state.decision.currentCategory);
    // Vuex 스토어에서 사용된 카테고리들을 가져오는 계산된 속성
    const usedCategories = computed(() => store.state.decision.usedCategories);

    // 옵션을 로드하는 비동기 함수
    const loadOptions = async () => {
      // 모든 카테고리가 사용되었다면 최종 선택 페이지로 이동
      if (usedCategories.value.size === store.state.decision.categories.length) {
        router.push('/final-selection');
        return;
      }

      isLoading.value = true;
      try {
        // Vuex 액션을 디스패치하여 옵션을 가져옴
        await store.dispatch('decision/fetchOptions');
        currentOptions.value = store.state.decision.currentOptions;
        // 모든 카드를 뒤집히지 않은 상태로 초기화
        flippedCards.value = new Array(currentOptions.value.length).fill(false);
        selectedIndex.value = -1;
      } catch (error) {
        console.error('Error loading options:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // 옵션을 선택하는 비동기 함수
    const selectOption = async (option, index) => {
      if (isSlideOut.value || isLoading.value) return;

      selectedIndex.value = index;
      flippedCards.value[index] = true;
      
      setTimeout(async () => {
        isSlideOut.value = true;
        // Vuex 액션을 디스패치하여 선택된 옵션을 저장
        await store.dispatch('decision/selectOption', option);
        
        setTimeout(async () => {
          // 모든 선택이 완료되었다면 최종 선택 페이지로 이동
          if (store.getters['decision/isSelectionComplete']) {
            router.push('/final-selection');
          } else {
            isSlideOut.value = false;
            await loadOptions();
          }
        }, 500);
      }, 1000);
    };

    // 무작위로 옵션을 선택하는 함수
    const randomSelect = async () => {
      if (isSlideOut.value || isLoading.value || currentOptions.value.length === 0) return;

      const randomIndex = Math.floor(Math.random() * currentOptions.value.length);
      await selectOption(currentOptions.value[randomIndex], randomIndex);
    };

    // 현재 카테고리를 건너뛰는 비동기 함수
    const skipCategory = async () => {
      if (isSlideOut.value || isLoading.value) return;

      isSlideOut.value = true;
      // Vuex 액션을 디스패치하여 카테고리를 건너뜀
      await store.dispatch('decision/skipCategory');
      
      setTimeout(async () => {
        isSlideOut.value = false;
        await loadOptions();
      }, 500);
    };

    // 카테고리가 변경될 때마다 옵션을 새로 로드
    watch(currentCategory, async (newCategory) => {
      if (newCategory && !isSlideOut.value) {
        await loadOptions();
      }
    });

    // 컴포넌트가 마운트될 때 초기화 작업 수행
    onMounted(async () => {
      store.dispatch('decision/resetDecision');
      await loadOptions();
    });

    return {
      currentCategory,
      currentOptions,
      flippedCards,
      isSlideOut,
      selectedIndex,
      isLoading,
      selectOption,
      randomSelect,
      skipCategory
    };
  }
};
</script>

<style scoped>
.decision-process {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.background-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('~@/assets/images/tavern-background.jpg');
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.content-layer {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.category-title {
  color: #FFD700;
  text-shadow: 2px 2px 4px #000;
  font-size: 2.5em;
  margin-bottom: 40px;
  z-index: 3;
}

.options-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 30px;
  padding: 20px;
  transition: transform 0.5s ease-out;
  z-index: 3;
}

.options-container.slide-out {
  transform: translateX(-100vw);
}

.buttons-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  z-index: 3;
}

.random-select-button, .skip-button {
  padding: 12px 24px;
  background: rgba(255, 215, 0, 0.2);
  border: 2px solid #FFD700;
  color: #FFD700;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
  text-shadow: 1px 1px 2px #000;
}

.random-select-button:hover, .skip-button:hover {
  background: rgba(255, 215, 0, 0.4);
  transform: translateY(-2px);
}

.random-select-button:disabled, .skip-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #FFD700;
  border-top: 5px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-overlay p {
  color: #FFD700;
  font-size: 1.2em;
  text-shadow: 1px 1px 2px #000;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .category-title {
    font-size: 2em;
  }
  
  .random-select-button, .skip-button {
    font-size: 1em;
    padding: 10px 20px;
  }

  .options-container {
    gap: 15px;
    padding: 10px;
  }
}
</style>
