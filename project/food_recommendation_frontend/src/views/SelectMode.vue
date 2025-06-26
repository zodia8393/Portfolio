<template>
  <div class="select-mode">
    <div class="background-layer"></div>
    <div class="content-layer">
      <h2 class="title">선택 방식</h2>
      <div class="mode-container">
        <!-- 카드게임 방식 선택 카드 -->
        <div class="mode-card" @click="selectMode('card')" :class="{ 'selected': selectedMode === 'card' }">
          <h3>카드게임 방식</h3>
          <div class="mode-icon">🎴</div>
          <p>하나씩 순차적으로 선택하며 진행합니다</p>
          <div class="mode-description">
            <p>- 카드를 한 장씩 선택</p>
            <p>- 단계별로 진행</p>
            <p>- 게임처럼 즐기며 선택</p>
          </div>
        </div>
        <!-- 한 번에 선택 방식 카드 -->
        <div class="mode-card" @click="selectMode('form')" :class="{ 'selected': selectedMode === 'form' }">
          <h3>한 번에 선택</h3>
          <div class="mode-icon">📋</div>
          <p>모든 옵션을 한 화면에서 선택합니다</p>
          <div class="mode-description">
            <p>- 모든 옵션을 한눈에 확인</p>
            <p>- 주차장, 룸 옵션에 '무관' 선택 가능</p>
            <p>- 빠른 선택 가능</p>
            <p>- 간편한 방식</p>
          </div>
        </div>
      </div>
      <!-- 선택 확정 버튼 -->
      <button 
        class="confirm-button" 
        @click="confirmMode"
        :disabled="!selectedMode">
        선택 확정
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'SelectMode',
  setup() {
    const router = useRouter();
    const selectedMode = ref(null);

    // 모드 선택 함수
    const selectMode = (mode) => {
      selectedMode.value = mode;
    };

    // 선택 확정 및 라우팅 함수
    const confirmMode = () => {
      if (selectedMode.value === 'card') {
        router.push('/decision');  // 카드게임 방식 페이지로 이동
      } else {
        router.push('/form-decision');  // 한 번에 선택 방식 페이지로 이동
      }
    };

    return {
      selectedMode,
      selectMode,
      confirmMode
    };
  }
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.select-mode {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 배경 이미지 레이어 */
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

/* 콘텐츠 레이어 */
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

/* 제목 스타일 */
.title {
  color: #FFD700;
  text-shadow: 2px 2px 4px #000;
  font-size: 2.5em;
  margin-bottom: 40px;
}

/* 모드 선택 카드 컨테이너 */
.mode-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 40px;
}

/* 모드 선택 카드 스타일 */
.mode-card {
  width: 300px;
  background: rgba(0, 0, 0, 0.8);
  border: 3px solid #FFD700;
  border-radius: 15px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

/* 모드 카드 호버 효과 */
.mode-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

/* 선택된 모드 카드 스타일 */
.mode-card.selected {
  transform: scale(1.05);
  box-shadow: 0 0 30px #FFD700;
}

/* 모드 카드 제목 스타일 */
.mode-card h3 {
  color: #FFD700;
  font-size: 1.5em;
  margin-bottom: 20px;
}

/* 모드 아이콘 스타일 */
.mode-icon {
  font-size: 4em;
  margin: 20px 0;
}

/* 모드 카드 설명 텍스트 스타일 */
.mode-card p {
  color: white;
  margin-bottom: 20px;
}

/* 모드 상세 설명 스타일 */
.mode-description {
  text-align: left;
  color: #FFD700;
  margin-top: 20px;
}

.mode-description p {
  color: #FFD700;
  margin: 10px 0;
  font-size: 0.9em;
}

/* 확인 버튼 스타일 */
.confirm-button {
  padding: 15px 30px;
  background: #FFD700;
  border: none;
  border-radius: 8px;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 확인 버튼 호버 효과 */
.confirm-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
}

/* 비활성화된 확인 버튼 스타일 */
.confirm-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* 반응형 디자인: 모바일 화면 */
@media (max-width: 768px) {
  .mode-container {
    flex-direction: column;
    gap: 20px;
  }

  .mode-card {
    width: 90%;
    margin: 0 auto;
  }
}
</style>
