<template>
  <div class="final-selection">
    <div class="background-layer"></div>
    <div class="content-layer">
      <h2 class="title">최종 선택</h2>
      <!-- 로딩 중일 때 표시할 내용 -->
      <div v-if="isLoading" class="loading">
        <p>맛있는 식당을 찾는 중</p>
      </div>
      <template v-else>
        <div class="cards-container">
          <!-- DB 추천 카드 -->
          <div class="recommendation-card" 
               :class="{ 'selected': selectedCard === 'db' }"
               @click="selectCard('db')"
               v-if="recommendations?.db_recommendation">
            <h3>데이터베이스 추천</h3>
            <div class="card-content">
              <!-- DB 추천 식당 정보 표시 -->
              <p class="restaurant-name">{{ recommendations.db_recommendation.name }}</p>
              <p>주소: {{ recommendations.db_recommendation.address }}</p>
              <p>분류: {{ recommendations.db_recommendation.category }}</p>
              <p>대표 메뉴: {{ recommendations.db_recommendation.main_menu }}</p>
              <p>주차: {{ recommendations.db_recommendation.parking }}</p>
              <p>룸: {{ recommendations.db_recommendation.room }}</p>
              <p>이동수단: {{ recommendations.db_recommendation.transport }}</p>
            </div>
          </div>

          <!-- AI 추천 카드 -->
          <div class="recommendation-card" 
               :class="{ 'selected': selectedCard === 'ai' }"
               @click="selectCard('ai')"
               v-if="recommendations?.ai_recommendation">
            <h3>AI 추천</h3>
            <div class="card-content">
              <!-- AI 추천 식당 정보 표시 -->
              <p class="restaurant-name">{{ recommendations.ai_recommendation.name }}</p>
              <p>주소: {{ recommendations.ai_recommendation.address }}</p>
              <p>분류: {{ recommendations.ai_recommendation.category }}</p>
              <p>대표 메뉴: {{ recommendations.ai_recommendation.main_menu }}</p>
              <p>주차: {{ recommendations.ai_recommendation.parking }}</p>
              <p>룸: {{ recommendations.ai_recommendation.room }}</p>
              <p>이동수단: {{ recommendations.ai_recommendation.transport }}</p>
            </div>
          </div>
        </div>

        <div class="button-container">
          <!-- 다시 추천받기 버튼 -->
          <button 
            class="reroll-button" 
            @click="rerollRecommendations"
            :disabled="isLoading">
            다시 추천받기
          </button>

          <!-- 선택 확정 버튼 -->
          <button 
            class="confirm-button" 
            @click="confirmSelection"
            :disabled="!selectedCard || isLoading">
            선택 확정
          </button>
        </div>
      </template>
    </div>
    <!-- 로딩 중 메시지 -->
    <div v-if="isLoading" class="loading-message">
      추천을 가져오는 중입니다. 잠시만 기다려주세요...
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'FinalSelection',
  setup() {
    const store = useStore();
    const router = useRouter();
    const selectedCard = ref(null);
    const isLoading = ref(false);

    // Vuex 스토어에서 추천 정보 가져오기
    const recommendations = computed(() => store.state.decision.recommendations);

    // 컴포넌트 마운트 시 로딩 효과 표시
    onMounted(() => {
      isLoading.value = true;
      setTimeout(() => {
        isLoading.value = false;
      }, 1500);
    });

    // 카드 선택 함수
    const selectCard = (type) => {
      selectedCard.value = type;
    };

    // 다시 추천받기 함수
    const rerollRecommendations = async () => {
      try {
        isLoading.value = true;
        selectedCard.value = null;
      
        const selectedOptions = store.state.decision.selectedOptions;
        console.log('현재 선택된 옵션들:', selectedOptions);
      
        if (!selectedOptions || selectedOptions.length === 0) {
          throw new Error('선택된 옵션이 없습니다. 옵션을 먼저 선택해주세요.');
        }
      
        const response = await store.dispatch('decision/getRecommendations', {
          selectedOptions: selectedOptions
        });
      
        if (!response || response.error) {
          throw new Error(response?.error || '추천을 가져오는데 실패했습니다.');
        }
      
      } catch (error) {
        console.error('리롤 중 오류 발생:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // 선택 확정 함수
    const confirmSelection = () => {
      if (selectedCard.value) {
        const selection = selectedCard.value === 'db' ? 
          recommendations.value.db_recommendation : 
          recommendations.value.ai_recommendation;
        
        store.commit('decision/SET_FINAL_SELECTION', selection);
        router.push('/result');
      }
    };

    return {
      recommendations,
      selectedCard,
      isLoading,
      selectCard,
      rerollRecommendations,
      confirmSelection
    };
  }
};
</script>
  
  <style scoped>
  .final-selection {
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
    padding: 20px;
  }
  
  .title {
    color: #FFD700;
    text-shadow: 2px 2px 4px #000;
    font-size: 2.5em;
    margin-bottom: 40px;
  }
  
  .cards-container {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-bottom: 40px;
  }
  
  .recommendation-card {
    width: 350px;
    min-height: 450px;
    background: rgba(0, 0, 0, 0.8);
    border: 3px solid #FFD700;
    border-radius: 15px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .recommendation-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  }
  
  .recommendation-card.selected {
    transform: scale(1.05);
    box-shadow: 0 0 30px #FFD700;
  }
  
  .recommendation-card h3 {
    color: #FFD700;
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.5em;
  }
  
  .card-content {
    color: white;
  }
  
  .restaurant-name {
    color: #FFD700;
    font-size: 1.2em;
    margin-bottom: 15px;
    font-weight: bold;
  }
  
  .card-content p {
    margin: 10px 0;
    line-height: 1.4;
  }
  
  .button-container {
    display: flex;
    gap: 20px;
  }
  
  .confirm-button, .reroll-button {
    padding: 15px 30px;
    border: none;
    border-radius: 8px;
    font-size: 1.2em;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .confirm-button {
    background: #FFD700;
    color: #000;
  }
  
  .reroll-button {
    background: #4a4a4a;
    color: #FFD700;
  }
  
  .confirm-button:hover, .reroll-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
  }
  
  .confirm-button:disabled, .reroll-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
  
  .loading {
    color: #FFD700;
    font-size: 1.5em;
    text-align: center;
    text-shadow: 2px 2px 4px #000;
    animation: pulse 1.5s infinite;
  }
  
  @keyframes pulse {
    0% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.5;
      transform: scale(0.95);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  .loading::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
  }
  
  @keyframes dots {
    0%, 20% { content: ''; }
    40% { content: '.'; }
    60% { content: '..'; }
    80% { content: '...'; }
  }
  
  @media (max-width: 768px) {
    .cards-container {
      flex-direction: column;
      gap: 20px;
    }
  
    .recommendation-card {
      width: 90%;
      margin: 0 auto;
    }
  }
  </style>
  