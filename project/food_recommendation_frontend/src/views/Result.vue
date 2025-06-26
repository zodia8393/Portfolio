<template>
  <div class="result">
    <!-- 배경 이미지 레이어 -->
    <div class="background-layer"></div>
    <!-- 내용을 담는 레이어 -->
    <div class="content-layer">
      <h2 class="title">최종 결정</h2>
      <!-- 선택된 식당 정보를 보여주는 카드 -->
      <div class="final-card">
        <h3>{{ finalSelection.name }}</h3>
        <div class="card-content">
          <p>주소: {{ finalSelection.address }}</p>
          <p>분류: {{ finalSelection.category }}</p>
          <p>대표 메뉴: {{ finalSelection.main_menu }}</p>
          <p>주차: {{ finalSelection.parking }}</p>
          <p>룸: {{ finalSelection.room }}</p>
          <p>이동수단: {{ finalSelection.transport }}</p>
        </div>
      </div>
      <!-- 다시 시작 버튼 -->
      <button class="restart-button" @click="restart">다시 시작</button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'Result',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // Vuex 스토어에서 최종 선택 정보를 가져옴
    const finalSelection = computed(() => store.state.decision.finalSelection);

    // 다시 시작 함수
    const restart = () => {
      // Vuex 스토어의 상태를 초기화
      store.dispatch('decision/resetDecision');
      // 홈 페이지로 이동하면서 결과 페이지에서 돌아왔음을 쿼리 파라미터로 표시
      router.push({
        path: '/',
        query: { from: 'result' }
      });
    };

    return {
      finalSelection,
      restart
    };
  }
};
</script>

<style scoped>
/* 결과 페이지 전체를 화면에 고정 */
.result {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 배경 이미지 스타일 */
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

/* 내용 레이어 스타일 */
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

/* 최종 선택 카드 스타일 */
.final-card {
  width: 400px;
  background: rgba(0, 0, 0, 0.8);
  border: 3px solid #FFD700;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 40px;
}

/* 카드 내 식당 이름 스타일 */
.final-card h3 {
  color: #FFD700;
  text-align: center;
  font-size: 1.8em;
  margin-bottom: 20px;
}

/* 카드 내용 스타일 */
.card-content {
  color: white;
  font-size: 1.2em;
}

/* 카드 내용의 각 항목 스타일 */
.card-content p {
  margin: 10px 0;
}

/* 다시 시작 버튼 스타일 */
.restart-button {
  padding: 15px 30px;
  background: #FFD700;
  border: none;
  border-radius: 8px;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 다시 시작 버튼 호버 효과 */
.restart-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
}
</style>
