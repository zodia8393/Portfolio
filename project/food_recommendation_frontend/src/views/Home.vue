<template>
  <div class="home">
    <div class="tavern-door" :class="{ 'open': doorOpen }">
      <img :src="require('@/assets/images/tavern-door.gif')" alt="Tavern Door" class="door-gif">
    </div>
    <div class="content" :class="{ 'visible': contentVisible }">
      <transition name="fade">
        <img v-if="logoVisible" :src="require('@/assets/images/logo.png')" alt="Logo" class="logo">
      </transition>
      <transition name="fade">
        <h1 v-if="textVisible" class="welcome-text">Smart Lunch Mate에 오신 것을 환영합니다</h1>
      </transition>
      <transition name="fade">
        <button v-if="buttonVisible" @click="startQuest" class="start-button">
          Start
        </button>
      </transition>
    </div>
    <button @click="openAdminPopup" class="admin-button">
      <i class="fas fa-cog"></i>
    </button>
    <div v-if="showAdminPopup" class="admin-popup">
      <div class="admin-header">
        <h2>관리자 메뉴</h2>
        <button @click="closeAdminPopup" class="close-button">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="admin-content">
        <div v-if="currentAdminView === 'main'" class="admin-main">
          <button @click="setAdminView('database')" class="admin-menu-button">
            <i class="fas fa-database"></i> 데이터베이스 관리
          </button>
          <button @click="setAdminView('options')" class="admin-menu-button">
            <i class="fas fa-cogs"></i> 옵션 카테고리
          </button>
          <button @click="setAdminView('reviews')" class="admin-menu-button">
            <i class="fas fa-star"></i> 리뷰 및 별점 관리
          </button>
          <button @click="setAdminView('selectedRestaurants')" class="admin-menu-button">
            <i class="fas fa-utensils"></i> 선택된 식당 목록
          </button>
          <button @click="setAdminView('settings')" class="admin-menu-button">
            <i class="fas fa-tools"></i> 관리자 설정
          </button>
        </div>
        
        <div v-else-if="currentAdminView === 'database'" class="admin-database">
          <h3>데이터베이스 관리</h3>
          <div class="database-actions">
            <input v-model="newRestaurant.name" placeholder="식당 이름">
            <input v-model="newRestaurant.address" placeholder="주소">
            <select v-model="newRestaurant.category">
              <option value="">카테고리 선택</option>
              <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
            </select>
            <input v-model="newRestaurant.parking" placeholder="주차 가능 여부">
            <input v-model="newRestaurant.main_menu" placeholder="대표 메뉴">
            <input v-model="newRestaurant.room" placeholder="룸 여부">
            <select v-model="newRestaurant.transport">
              <option value="">이동수단 선택</option>
              <option value="도보">도보</option>
              <option value="차량">차량</option>
            </select>
            <button @click="addRestaurant" class="add-button">
              <i class="fas fa-plus"></i> 식당 추가
            </button>
          </div>
          <div class="database-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>이름</th>
                  <th>주소</th>
                  <th>카테고리</th>
                  <th>주차</th>
                  <th>대표 메뉴</th>
                  <th>룸</th>
                  <th>이동수단</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="restaurant in restaurants" :key="restaurant.id">
                  <td>{{ restaurant.id }}</td>
                  <td>{{ restaurant.name }}</td>
                  <td>{{ restaurant.address }}</td>
                  <td>{{ restaurant.category }}</td>
                  <td>{{ restaurant.parking }}</td>
                  <td>{{ restaurant.main_menu }}</td>
                  <td>{{ restaurant.room }}</td>
                  <td>{{ restaurant.transport }}</td>
                  <td>
                    <button @click="editRestaurant(restaurant)" class="edit-button">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteRestaurant(restaurant.id)" class="delete-button">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else-if="currentAdminView === 'options'" class="admin-options">
          <h3>옵션 카테고리</h3>
          <div class="option-actions">
            <input v-model="newOption.name" placeholder="옵션 이름">
            <select v-model="newOption.category">
              <option value="">카테고리 선택</option>
              <option v-for="category in optionCategories" :key="category" :value="category">{{ category }}</option>
            </select>
            <button @click="addOption" class="add-button">
              <i class="fas fa-plus"></i> 옵션 추가
            </button>
          </div>
          <div class="option-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>이름</th>
                  <th>카테고리</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="option in options" :key="option.id">
                  <td>{{ option.id }}</td>
                  <td>
                    <input v-if="editingOption === option.id" v-model="option.name" @blur="updateOption(option)">
                    <span v-else>{{ option.name }}</span>
                  </td>
                  <td>
                    <select v-if="editingOption === option.id" v-model="option.category" @change="updateOption(option)">
                      <option v-for="category in optionCategories" :key="category" :value="category">{{ category }}</option>
                    </select>
                    <span v-else>{{ option.category }}</span>
                  </td>
                  <td>
                    <button @click="editOption(option.id)" class="edit-button">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteOption(option.id)" class="delete-button">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else-if="currentAdminView === 'reviews'" class="admin-reviews">
          <h3>리뷰 및 별점 관리</h3>
          <div class="review-actions">
            <select v-model="newReview.restaurantId">
              <option value="">식당 선택</option>
              <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.id">
                {{ restaurant.name }}
              </option>
            </select>
            <input v-model="newReview.username" placeholder="작성자">
            <textarea v-model="newReview.content" placeholder="리뷰 내용"></textarea>
            <div class="star-rating">
              <span v-for="i in 5" :key="i" @click="setRating(i)" :class="{ 'filled': i <= newReview.rating }">★</span>
            </div>
            <button @click="addReview" class="add-button">
              <i class="fas fa-plus"></i> 리뷰 추가
            </button>
          </div>
          <div class="review-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>식당</th>
                  <th>작성자</th>
                  <th>내용</th>
                  <th>별점</th>
                  <th>작성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="review in reviews" :key="review.id">
                  <td>{{ review.id }}</td>
                  <td>{{ getRestaurantName(review.restaurant_id) }}</td>
                  <td>{{ review.username }}</td>
                  <td>{{ review.content }}</td>
                  <td>
                    <div class="star-rating">
                      <span v-for="i in 5" :key="i" :class="{ 'filled': i <= review.rating }">★</span>
                    </div>
                  </td>
                  <td>{{ formatDate(review.created_at) }}</td>
                  <td>
                    <button @click="editReview(review)" class="edit-button">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteReview(review.id)" class="delete-button">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else-if="currentAdminView === 'selectedRestaurants'" class="admin-selected-restaurants">
          <h3>선택된 식당 목록</h3>
          <table>
            <thead>
              <tr>
                <th>이름</th>
                <th>선택 날짜</th>
                <th>제외 기간</th>
                <th>카테고리</th>
                <th>주소</th>
                <th>리뷰</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="restaurant in selectedRestaurants" :key="restaurant.id">
                <td>{{ restaurant.name }}</td>
                <td>{{ formatDate(restaurant.selected_date) }}</td>
                <td>{{ formatDate(restaurant.exclude_until) }}</td>
                <td>{{ restaurant.category }}</td>
                <td>{{ restaurant.address }}</td>
                <td>
                  <button @click="showReviewModal(restaurant)" class="review-button">
                    리뷰 보기/작성
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else-if="currentAdminView === 'settings'" class="admin-settings">
          <h3>관리자 설정</h3>
          <div class="settings-form">
            <label>추천 제외 기간 (일)</label>
            <input 
              type="number" 
              v-model.number="exclusionDays" 
              min="1" 
              max="30"
            >
            <button @click="saveExclusionDays" class="save-button">
              저장
            </button>
          </div>
        </div>
      </div>
      <div class="admin-footer">
        <button v-if="currentAdminView !== 'main'" @click="setAdminView('main')" class="back-button">
          <i class="fas fa-arrow-left"></i> 뒤로
        </button>
      </div>
    </div>

    <!-- 레스토랑 편집 모달 -->
    <div v-if="editingRestaurant" class="modal">
      <div class="modal-content">
        <h3>레스토랑 정보 수정</h3>
        <input v-model="editingRestaurant.name" placeholder="식당 이름">
        <input v-model="editingRestaurant.address" placeholder="주소">
        <select v-model="editingRestaurant.category">
          <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
        </select>
        <input v-model="editingRestaurant.parking" placeholder="주차 가능 여부">
        <input v-model="editingRestaurant.main_menu" placeholder="대표 메뉴">
        <input v-model="editingRestaurant.room" placeholder="룸 여부">
        <select v-model="editingRestaurant.transport">
          <option value="도보">도보</option>
          <option value="차량">차량</option>
        </select>
        <div class="modal-actions">
          <button @click="updateRestaurant" class="update-button">수정</button>
          <button @click="cancelEditRestaurant" class="cancel-button">취소</button>
        </div>
      </div>
    </div>

    <!-- 리뷰 편집 모달 -->
    <div v-if="editingReview" class="modal">
      <div class="modal-content">
        <h3>리뷰 수정</h3>
        <select v-model="editingReview.restaurant_id">
          <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.id">
            {{ restaurant.name }}
          </option>
        </select>
        <input v-model="editingReview.username" placeholder="작성자">
        <textarea v-model="editingReview.content" placeholder="리뷰 내용"></textarea>
        <div class="star-rating">
          <span v-for="i in 5" :key="i" @click="setEditingReviewRating(i)" :class="{ 'filled': i <= editingReview.rating }">★</span>
        </div>
        <div class="modal-actions">
          <button @click="updateReview" class="update-button">수정</button>
          <button @click="cancelEditReview" class="cancel-button">취소</button>
        </div>
      </div>
    </div>

    <!-- 리뷰 모달 -->
    <div v-if="showReview" class="review-modal">
      <div class="review-content">
        <h3>{{ currentRestaurant.name }} 리뷰</h3>
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <p>{{ review.content }}</p>
          <div class="star-rating">
            <span v-for="i in 5" :key="i" :class="{ 'filled': i <= review.rating }">★</span>
          </div>
          <p>작성자: {{ review.username }}</p>
          <p>작성일: {{ formatDate(review.created_at) }}</p>
        </div>
        <div class="add-review">
          <input v-model="newReview.username" placeholder="이름을 입력해주세요" />
          <textarea v-model="newReview.content" placeholder="리뷰를 작성해주세요"></textarea>
          <div class="star-rating">
            <span v-for="i in 5" :key="i" @click="setRating(i)" :class="{ 'filled': i <= newReview.rating }">★</span>
          </div>
          <button @click="submitReview">리뷰 제출</button>
        </div>
        <button @click="closeReviewModal">닫기</button>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

export default {
  name: 'Home',
  setup() {
    const router = useRouter();
    const doorOpen = ref(false);
    const contentVisible = ref(false);
    const logoVisible = ref(false);
    const textVisible = ref(false);
    const buttonVisible = ref(false);
    const showAdminPopup = ref(false);
    const currentAdminView = ref('main');

    const restaurants = ref([]);
    const options = ref([]);
    const reviews = ref([]);
    const selectedRestaurants = ref([]);

    const newRestaurant = ref({ name: '', address: '', category: '', parking: '', main_menu: '', room: '', transport: '' });
    const newOption = ref({ name: '', category: '' });
    const newReview = ref({ username: '', content: '', rating: 0 });

    const editingOption = ref(null);
    const editingRestaurant = ref(null);
    const editingReview = ref(null);

    const categories = ref(['한식', '중식', '일식', '양식', '분식', '기타']);
    const optionCategories = ref(['분류', '주차장', '룸', '도보/차량']);

    const exclusionDays = ref(7);
    const showReview = ref(false);
    const currentRestaurant = ref({});

    const startAnimation = () => {
      if (router.currentRoute.value.query.from === 'result') {
        doorOpen.value = true;
        contentVisible.value = true;
        textVisible.value = true;
        buttonVisible.value = true;
        return;
      }

      doorOpen.value = true;
      setTimeout(() => {
        contentVisible.value = true;
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
      router.push('/select-mode');
    };

    const openAdminPopup = () => {
      showAdminPopup.value = true;
      loadAdminData();
    };

    const closeAdminPopup = () => {
      showAdminPopup.value = false;
      currentAdminView.value = 'main';
    };

    const setAdminView = (view) => {
      currentAdminView.value = view;
      if (view === 'settings') {
        loadExclusionDays();
      } else if (view === 'selectedRestaurants') {
        loadSelectedRestaurants();
      }
    };

    const loadAdminData = async () => {
      try {
        const [restaurantsData, optionsData] = await Promise.all([
          api.getRestaurants(),
          api.getOptions()
        ]);
        restaurants.value = restaurantsData;
        options.value = optionsData;
      } catch (error) {
        console.error('Error loading admin data:', error);
      }
    };


    const addRestaurant = async () => {
      try {
        const response = await api.addRestaurant(newRestaurant.value);
        restaurants.value.push(response);
        newRestaurant.value = { name: '', address: '', category: '', parking: '', main_menu: '', room: '', transport: '' };
      } catch (error) {
        console.error('Error adding restaurant:', error);
      }
    };

    const editRestaurant = (restaurant) => {
      editingRestaurant.value = { ...restaurant };
    };

    const updateRestaurant = async () => {
      try {
        const response = await api.updateRestaurant(editingRestaurant.value.id, editingRestaurant.value);
        const index = restaurants.value.findIndex(r => r.id === response.id);
        if (index !== -1) {
          restaurants.value[index] = response;
        }
        editingRestaurant.value = null;
      } catch (error) {
        console.error('Error updating restaurant:', error);
      }
    };

    const cancelEditRestaurant = () => {
      editingRestaurant.value = null;
    };

    const deleteRestaurant = async (id) => {
      try {
        await api.deleteRestaurant(id);
        restaurants.value = restaurants.value.filter(r => r.id !== id);
      } catch (error) {
        console.error('Error deleting restaurant:', error);
      }
    };

    const addOption = async () => {
      try {
        const response = await api.addOption(newOption.value);
        options.value.push(response);
        newOption.value = { name: '', category: '' };
      } catch (error) {
        console.error('Error adding option:', error);
      }
    };

    const editOption = (id) => {
      editingOption.value = id;
    };

    const updateOption = async (option) => {
      try {
        await api.updateOption(option.id, option);
        editingOption.value = null;
      } catch (error) {
        console.error('Error updating option:', error);
      }
    };

    const deleteOption = async (id) => {
      try {
        await api.deleteOption(id);
        options.value = options.value.filter(o => o.id !== id);
      } catch (error) {
        console.error('Error deleting option:', error);
      }
    };

    const showReviewModal = async (restaurant) => {
      if (!restaurant || !restaurant.id) {
        console.error('Invalid restaurant object:', restaurant);
        return;
      }
      currentRestaurant.value = restaurant;
      showReview.value = true;
      try {
        reviews.value = await api.getReviews(restaurant.id);
      } catch (error) {
        console.error('Error loading reviews:', error);
        reviews.value = [];
      }
    };

    const closeReviewModal = () => {
      showReview.value = false;
      newReview.value = { username: '', content: '', rating: 0 };
    };

    const setRating = (rating) => {
      newReview.value.rating = rating;
    };

    const submitReview = async () => {
      try {
        console.log('Submitting review:', newReview.value);
        const response = await api.addReview({
          restaurant_id: currentRestaurant.value.id,
          username: newReview.value.username,
          content: newReview.value.content,
          rating: newReview.value.rating
        });
        console.log('Review submitted:', response);
        reviews.value = await api.getReviews(currentRestaurant.value.id);
        newReview.value = { username: '', content: '', rating: 0 };
        alert('리뷰가 성공적으로 등록되었습니다.');
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('리뷰 등록에 실패했습니다. 다시 시도해주세요.');
      }
    };

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString();
    };

    const loadExclusionDays = async () => {
      try {
        const days = await api.getExclusionDays();
        exclusionDays.value = days;
      } catch (error) {
        console.error('Error loading exclusion days:', error);
      }
    };

    const saveExclusionDays = async () => {
      try {
        await api.setExclusionDays(exclusionDays.value);
        alert('설정이 저장되었습니다.');
      } catch (error) {
        console.error('Error saving exclusion days:', error);
        alert('설정 저장 중 오류가 발생했습니다.');
      }
    };

    const loadSelectedRestaurants = async () => {
      try {
        selectedRestaurants.value = await api.getSelectedRestaurants();
      } catch (error) {
        console.error('Error loading selected restaurants:', error);
      }
    };

    onMounted(() => {
      startAnimation();
    });

    return {
      doorOpen,
      contentVisible,
      logoVisible,
      textVisible,
      buttonVisible,
      showAdminPopup,
      currentAdminView,
      restaurants,
      options,
      reviews,
      selectedRestaurants,
      newRestaurant,
      newOption,
      newReview,
      editingOption,
      editingRestaurant,
      editingReview,
      categories,
      optionCategories,
      exclusionDays,
      showReview,
      currentRestaurant,
      startQuest,
      openAdminPopup,
      closeAdminPopup,
      setAdminView,
      addRestaurant,
      editRestaurant,
      updateRestaurant,
      cancelEditRestaurant,
      deleteRestaurant,
      addOption,
      editOption,
      updateOption,
      deleteOption,
      showReviewModal,
      closeReviewModal,
      setRating,
      submitReview,
      formatDate,
      loadExclusionDays,
      saveExclusionDays,
      loadSelectedRestaurants
    };
  }
};
</script>



<style scoped>
.home {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-image: url('~@/assets/images/tavern-background.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tavern-door {
  position: absolute;
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

.content {
  position: relative;
  z-index: 20;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 1s ease-in-out;
  padding: 2vw;
  text-align: center;
}

.content.visible {
  opacity: 1;
}

.logo {
  max-width: 60%;
  height: auto;
  margin-bottom: 5vh;
}

.welcome-text {
  font-size: 2.5vw;
  color: #FFD700;
  text-shadow: 2px 2px 4px #000;
  margin-bottom: 5vh;
}

.start-button {
  font-size: 1.5vw;
  padding: 1vh 2vw;
  background-color: transparent;
  border: 2px solid #FFD700;
  color: #FFD700;
  text-shadow: 1px 1px 2px #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-button:hover {
  background-color: rgba(255, 215, 0, 0.2);
  transform: scale(1.1);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.admin-button {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  border: 2px solid #FFD700;
  border-radius: 50%;
  padding: 10px;
  color: #FFD700;
  font-size: 24px;
  cursor: pointer;
  z-index: 100;
}

.admin-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.9);
  border: 2px solid #FFD700;
  border-radius: 10px;
  padding: 20px;
  z-index: 1000;
  width: 90%;
  max-width: 1200px;
  height: 90vh;
  max-height: 800px;
  overflow-y: auto;
  color: #FFD700;
  display: flex;
  flex-direction: column;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.admin-header h2 {
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  color: #FFD700;
  font-size: 20px;
  cursor: pointer;
}

.admin-content {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  padding-right: 10px;
}

.admin-content::-webkit-scrollbar {
  width: 8px;
}

.admin-content::-webkit-scrollbar-track {
  background: rgba(255, 215, 0, 0.1);
  border-radius: 4px;
}

.admin-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 215, 0, 0.5);
  border-radius: 4px;
}

.admin-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 215, 0, 0.7);
}

.admin-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 215, 0, 0.5) rgba(255, 215, 0, 0.1);
}

.admin-main {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.admin-menu-button {
  background-color: rgba(255, 215, 0, 0.2);
  border: 1px solid #FFD700;
  color: #FFD700;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-menu-button:hover {
  background-color: rgba(255, 215, 0, 0.4);
}

.database-actions, .option-actions, .review-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.database-actions input, .option-actions input, .option-actions select, .review-actions select, .review-actions textarea, .review-actions input {
  flex: 1;
  padding: 5px;
  background-color: rgba(0, 0, 0, 0.7);
  border: 1px solid #FFD700;
  color: #FFD700;
}

.add-button, .delete-button, .edit-button {
  background-color: rgba(255, 215, 0, 0.2);
  border: 1px solid #FFD700;
  color: #FFD700;
  padding: 5px 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-button:hover, .delete-button:hover, .edit-button:hover {
  background-color: rgba(255, 215, 0, 0.4);
}

.database-table, .option-table, .review-table {
  overflow-x: auto;
  max-width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

th, td {
  border: 1px solid #FFD700;
  padding: 10px;
  text-align: left;
}

th {
  background-color: rgba(255, 215, 0, 0.2);
}

.admin-footer {
  display: flex;
  justify-content: flex-start;
}

.back-button {
  background-color: rgba(255, 215, 0, 0.2);
  border: 1px solid #FFD700;
  color: #FFD700;
  padding: 5px 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgba(255, 215, 0, 0.4);
}

select {
  background-color: rgba(0, 0, 0, 0.7);
  color: #FFD700;
  border: 1px solid #FFD700;
}

.modal {
  position: fixed;
  z-index: 2000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: rgba(0, 0, 0, 0.9);
  margin: auto;
  padding: 20px;
  border: 1px solid #FFD700;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 10px;
}

.modal-content h3 {
  color: #FFD700;
  margin-bottom: 20px;
}

.modal-content input,
.modal-content select,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border: 1px solid #FFD700;
  color: #FFD700;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.update-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-button {
  background-color: #4CAF50;
  color: white;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}

.update-button:hover,
.cancel-button:hover {
  opacity: 0.8;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: rgba(255, 215, 0, 0.1);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 215, 0, 0.5);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 215, 0, 0.7);
}

.modal-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 215, 0, 0.5) rgba(255, 215, 0, 0.1);
}

/* 새로 추가된 스타일 */
.admin-selected-restaurants {
  margin-top: 20px;
}

.admin-selected-restaurants table {
  width: 100%;
  border-collapse: collapse;
}

.admin-selected-restaurants th,
.admin-selected-restaurants td {
  border: 1px solid #FFD700;
  padding: 10px;
  text-align: left;
}

.admin-selected-restaurants th {
  background-color: rgba(255, 215, 0, 0.2);
}

.review-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.review-content {
  background-color: rgba(0, 0, 0, 0.9);
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  color: #FFD700;
}

.review-item {
  margin-bottom: 20px;
  border-bottom: 1px solid #FFD700;
  padding-bottom: 10px;
}

.star-rating {
  font-size: 24px;
  color: #ddd;
  cursor: pointer;
}

.star-rating span {
  transition: color 0.2s;
}

.star-rating span.filled {
  color: #FFD700;
}

.add-review input,
.add-review textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border: 1px solid #FFD700;
  color: #FFD700;
}

.add-review textarea {
  height: 100px;
}

@media (max-width: 1024px) {
  .admin-popup {
    width: 95%;
    height: 95vh;
    padding: 15px;
  }

  .database-actions, .option-actions, .review-actions {
    flex-direction: column;
  }

  .database-actions input, .option-actions input, .option-actions select, 
  .review-actions select, .review-actions textarea, .review-actions input {
    width: 100%;
    margin-bottom: 10px;
  }

  table {
    font-size: 14px;
  }

  .review-content {
    width: 90%;
  }
}

@media (max-width: 768px) {
  .admin-popup {
    padding: 10px;
  }

  .welcome-text {
    font-size: 4vw;
  }
  
  .start-button {
    font-size: 3vw;
  }

  .admin-button {
    font-size: 20px;
  }

  table {
    font-size: 12px;
  }

  .star-rating {
    font-size: 20px;
  }
}
</style>
