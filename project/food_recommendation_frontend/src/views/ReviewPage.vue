<template>
  <div class="review-page">
    <h2>{{ restaurant.name }} 리뷰</h2>
    <div class="restaurant-info">
      <img :src="restaurant.image" :alt="restaurant.name" class="restaurant-image">
      <div class="info">
        <p><strong>주소:</strong> {{ restaurant.address }}</p>
        <p><strong>요리 종류:</strong> {{ restaurant.cuisine }}</p>
        <p><strong>평균 평점:</strong> {{ averageRating.toFixed(1) }} / 5</p>
      </div>
    </div>
    <!-- 리뷰 작성 폼 컴포넌트 -->
    <ReviewForm @submit-review="submitReview" />
    <!-- 리뷰 목록 컴포넌트 -->
    <ReviewList :reviews="reviews" />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import ReviewForm from '@/components/ReviewForm.vue';
import ReviewList from '@/components/ReviewList.vue';

export default {
  name: 'ReviewPage',
  components: {
    ReviewForm,
    ReviewList
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const restaurantId = route.params.id; // URL에서 레스토랑 ID 가져오기

    const restaurant = ref({}); // 레스토랑 정보를 저장할 반응형 변수
    // 현재 레스토랑의 리뷰 목록을 가져오는 computed 속성
    const reviews = computed(() => store.state.reviews.restaurantReviews[restaurantId] || []);
    // 평균 평점을 계산하는 computed 속성
    const averageRating = computed(() => {
      if (reviews.value.length === 0) return 0;
      const sum = reviews.value.reduce((acc, review) => acc + review.rating, 0);
      return sum / reviews.value.length;
    });

    onMounted(async () => {
      // 컴포넌트가 마운트되면 레스토랑 정보와 리뷰를 가져옴
      await store.dispatch('restaurants/fetchRestaurant', restaurantId);
      await store.dispatch('reviews/fetchReviews', restaurantId);
      restaurant.value = store.state.restaurants.currentRestaurant;
    });

    // 새 리뷰를 제출하는 함수
    const submitReview = async (review) => {
      await store.dispatch('reviews/submitReview', { restaurantId, review });
    };

    return {
      restaurant,
      reviews,
      averageRating,
      submitReview
    };
  }
};
</script>

<style scoped>
.review-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.restaurant-info {
  display: flex;
  margin-bottom: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
}

.restaurant-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 20px;
}

.info {
  flex-grow: 1;
}

h2 {
  color: #FFD700;
  margin-bottom: 20px;
}
</style>
