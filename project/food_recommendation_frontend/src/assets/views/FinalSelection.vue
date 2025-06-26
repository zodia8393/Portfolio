<template>
    <div class="final-selection">
      <h2>추천 식당</h2>
      <div class="recommendations-container">
        <RestaurantCard 
          v-for="(restaurant, index) in recommendations" 
          :key="restaurant.id" 
          :restaurant="restaurant"
          :isFlipped="flippedCards[index]"
          @click="selectRestaurant(restaurant, index)"
        />
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import RestaurantCard from '@/components/RestaurantCard.vue';
  
  export default {
    name: 'FinalSelection',
    components: {
      RestaurantCard
    },
    setup() {
      const store = useStore();
      const router = useRouter();
      
      const flippedCards = ref([]);
  
      const recommendations = computed(() => store.state.decision.recommendations);
  
      const loadRecommendations = async () => {
        await store.dispatch('decision/getRecommendations');
        flippedCards.value = new Array(recommendations.value.length).fill(false);
      };
  
      const selectRestaurant = (restaurant, index) => {
        flippedCards.value[index] = true;
        setTimeout(() => {
          router.push({ name: 'Result', params: { id: restaurant.id } });
        }, 1000);
      };
  
      onMounted(loadRecommendations);
  
      return {
        recommendations,
        flippedCards,
        selectRestaurant
      };
    }
  };
  </script>
  
  <style scoped>
  .final-selection {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .recommendations-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
  }
  
  h2 {
    color: #FFD700;
    text-shadow: 2px 2px 4px #000;
    font-size: 2em;
    margin-bottom: 20px;
  }
  </style>
  