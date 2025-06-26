<template>
    <div class="result" v-if="restaurant">
      <h2>{{ restaurant.name }}</h2>
      <img :src="restaurant.image" :alt="restaurant.name">
      <p class="description">{{ restaurant.description }}</p>
      <div class="details">
        <p><strong>주소:</strong> {{ restaurant.address }}</p>
        <p><strong>전화번호:</strong> {{ restaurant.phone }}</p>
        <p><strong>영업시간:</strong> {{ restaurant.hours }}</p>
      </div>
      <div class="reviews">
        <h3>리뷰</h3>
        <ReviewList :reviews="restaurantReviews" />
        <ReviewForm @submit-review="submitReview" />
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useStore } from 'vuex';
  import { useRoute } from 'vue-router';
  import ReviewForm from '@/components/ReviewForm.vue';
  import ReviewList from '@/components/ReviewList.vue';
  
  export default {
    name: 'Result',
    components: {
      ReviewForm,
      ReviewList
    },
    setup() {
      const store = useStore();
      const route = useRoute();
      
      const restaurant = ref(null);
      const restaurantReviews = computed(() => store.state.reviews.restaurantReviews[route.params.id] || []);
  
      const loadRestaurantDetails = async () => {
        const { id } = route.params;
        await store.dispatch('restaurants/fetchRestaurant', id);
        restaurant.value = store.state.restaurants.currentRestaurant;
        await store.dispatch('reviews/fetchReviews', id);
      };
  
      const submitReview = async (review) => {
        await store.dispatch('reviews/submitReview', { 
          restaurantId: restaurant.value.id, 
          review 
        });
      };
  
      onMounted(loadRestaurantDetails);
  
      return {
        restaurant,
        restaurantReviews,
        submitReview
      };
    }
  };
  </script>
  
  <style scoped>
  .result {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
  }
  
  h2 {
    color: #FFD700;
    text-shadow: 2px 2px 4px #000;
    font-size: 2em;
    margin-bottom: 20px;
  }
  
  img {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  
  .description {
    font-style: italic;
    margin-bottom: 20px;
  }
  
  .details {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  
  .reviews {
    margin-top: 30px;
  }
  
  h3 {
    color: #FFD700;
    margin-bottom: 15px;
  }
  </style>
  