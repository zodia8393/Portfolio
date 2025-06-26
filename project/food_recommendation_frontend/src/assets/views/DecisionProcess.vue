<template>
    <div class="decision-process">
      <h2>{{ currentCategory }} 선택</h2>
      <div class="options-container">
        <OptionCard 
          v-for="(option, index) in currentOptions" 
          :key="option.id" 
          :option="option"
          :isFlipped="flippedCards[index]"
          @click="selectOption(option, index)"
        />
      </div>
      <CardDeck :selectedCards="selectedOptions" />
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import OptionCard from '@/components/OptionCard.vue';
  import CardDeck from '@/components/CardDeck.vue';
  
  export default {
    name: 'DecisionProcess',
    components: {
      OptionCard,
      CardDeck
    },
    setup() {
      const store = useStore();
      const router = useRouter();
      
      const currentOptions = ref([]);
      const flippedCards = ref([]);
  
      const currentCategory = computed(() => store.state.decision.currentCategory);
      const selectedOptions = computed(() => store.state.decision.selectedOptions);
  
      const loadOptions = async () => {
        await store.dispatch('decision/fetchOptions');
        currentOptions.value = store.state.decision.currentOptions;
        flippedCards.value = new Array(currentOptions.value.length).fill(false);
      };
  
      const selectOption = async (option, index) => {
        flippedCards.value[index] = true;
        await store.dispatch('decision/selectOption', option);
        if (store.state.decision.isSelectionComplete) {
          router.push('/final-selection');
        } else {
          loadOptions();
        }
      };
  
      onMounted(loadOptions);
  
      return {
        currentCategory,
        currentOptions,
        flippedCards,
        selectedOptions,
        selectOption
      };
    }
  };
  </script>
  
  <style scoped>
  .decision-process {
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .options-container {
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
  