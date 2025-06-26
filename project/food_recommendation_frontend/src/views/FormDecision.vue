<template>
  <div class="form-decision">
    <!-- 배경 레이어 -->
    <div class="background-layer"></div>
    <!-- 컨텐츠 레이어 -->
    <div class="content-layer">
      <h2 class="title">옵션 선택</h2>
      <div class="form-container">
        <!-- 카테고리 그리드 -->
        <div class="categories-grid">
          <!-- 각 카테고리 섹션 -->
          <div v-for="category in categories" :key="category" class="category-section">
            <h3 class="category-title">{{ category }}</h3>
            <!-- 옵션 그리드 -->
            <div class="options-grid">
              <!-- 각 옵션 카드 -->
              <div 
                v-for="option in categoryOptions[category]" 
                :key="option.id"
                class="option-card"
                :class="{ 
                  'selected': isSelected(category, option), 
                  'disabled': isDisabled(category, option)
                }"
                :data-option="option.name"
                @click="selectOption(category, option)"
              >
                <div class="option-content">
                  <p>{{ option.name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 선택 완료 버튼 -->
      <button 
        class="confirm-button" 
        @click="confirmSelections"
        :disabled="!isAnySelected">
        선택 완료
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import api from '@/services/api';

export default {
  name: 'FormDecision',
  setup() {
    const store = useStore();
    const router = useRouter();
    const categoryOptions = ref({}); // 카테고리별 옵션 저장
    const selectedOptions = ref({}); // 선택된 옵션 저장
    const isLoading = ref(false); // 로딩 상태

    const categories = ['분류', '주차장', '룸', '도보/차량']; // 카테고리 목록

    // 옵션이 하나라도 선택되었는지 확인
    const isAnySelected = computed(() => {
      return Object.keys(selectedOptions.value).length > 0;
    });

    // 옵션 로드 함수
    const loadOptions = async () => {
      try {
        for (const category of categories) {
          const response = await api.getOptions(category);
          // '무관' 옵션을 맨 앞에 추가하고 나머지 옵션 필터링
          categoryOptions.value[category] = [
            { id: `${category}_무관`, name: '무관', category: category },
            ...response.filter(option => option.name !== '무관')
          ];
        }
      } catch (error) {
        console.error('Error loading options:', error);
      }
    };

    // 옵션이 선택되었는지 확인
    const isSelected = (category, option) => {
      return selectedOptions.value[category]?.id === option.id;
    };

    // 옵션이 비활성화되었는지 확인
    const isDisabled = (category, option) => {
      return selectedOptions.value[category] && selectedOptions.value[category].id !== option.id;
    };

    // 옵션 선택 함수
    const selectOption = (category, option) => {
      if (!isDisabled(category, option)) {
        if (isSelected(category, option)) {
          delete selectedOptions.value[category];
        } else {
          selectedOptions.value[category] = option;
        }
      }
    };

    // 선택 완료 함수
    const confirmSelections = async () => {
      if (isAnySelected.value) {
        try {
          isLoading.value = true;
          const formattedSelections = Object.values(selectedOptions.value);
        
          console.log('Selected options saved:', formattedSelections);
        
          store.commit('decision/SET_SELECTED_OPTIONS', formattedSelections);
        
          const response = await store.dispatch('decision/getRecommendations', {
            selectedOptions: formattedSelections
          });
          
          if (response && !response.error) {
            router.push('/final-selection');
          } else {
            console.error('Failed to get recommendations:', response?.error);
          }
        } catch (error) {
          console.error('Error in confirmSelections:', error);
        } finally {
          isLoading.value = false;
        }
      }
    };

    // 컴포넌트 마운트 시 실행
    onMounted(() => {
      store.commit('decision/RESET_DECISION');
      loadOptions();
    });

    return {
      categories,
      categoryOptions,
      isSelected,
      isDisabled,
      selectOption,
      confirmSelections,
      isAnySelected,
      isLoading
    };
  }
};
</script>

<style scoped>
.form-decision {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.background-layer {
  position: fixed;
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
  z-index: 2;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.title {
  color: #FFD700;
  text-shadow: 2px 2px 4px #000;
  font-size: 2.5em;
  margin-bottom: 20px;
}

.form-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.category-section {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 15px;
  padding: 20px;
}

.category-title {
  color: #FFD700;
  text-shadow: 1px 1px 2px #000;
  font-size: 1.5em;
  margin-bottom: 15px;
  text-align: center;
}

.options-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.option-card {
  width: 120px;
  height: 80px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #FFD700;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

.option-card:not(.disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
}

.option-card.selected {
  transform: scale(1.05);
  box-shadow: 0 0 15px #FFD700;
  background: rgba(255, 215, 0, 0.2);
}

.option-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.option-card[data-option="무관"] {
  background: rgba(128, 128, 128, 0.8);
  border-style: dashed;
}

.option-content p {
  color: #FFD700;
  font-size: 1em;
  text-align: center;
  margin: 0;
  padding: 5px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

.confirm-button {
  padding: 15px 30px;
  background: #FFD700;
  border: none;
  border-radius: 8px;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
  color: #000;
  font-weight: bold;
}

.confirm-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
}

.confirm-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #808080;
}

@media (max-width: 1024px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }

  .option-card {
    width: 100px;
    height: 70px;
  }

  .option-content p {
    font-size: 0.9em;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2em;
  }

  .category-title {
    font-size: 1.3em;
  }

  .option-card {
    width: 90px;
    height: 60px;
  }

  .option-content p {
    font-size: 0.8em;
  }

  .confirm-button {
    padding: 12px 24px;
    font-size: 1em;
  }
}
</style>
