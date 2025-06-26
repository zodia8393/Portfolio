<template>
  <div class="admin-panel">
    <h1>관리자 패널</h1>
    <div class="admin-sections">
      <!-- 옵션 관리 섹션 -->
      <div class="section">
        <h2>옵션 관리</h2>
        <button @click="showOptionModal = true">새 옵션 추가</button>
        <ul>
          <li v-for="option in options" :key="option.id">
            {{ option.name }} - {{ option.category }}
            <button @click="editOption(option)">수정</button>
            <button @click="deleteOption(option.id)">삭제</button>
          </li>
        </ul>
      </div>
      <!-- 식당 관리 섹션 -->
      <div class="section">
        <h2>식당 관리</h2>
        <button @click="showRestaurantModal = true">새 식당 추가</button>
        <ul>
          <li v-for="restaurant in restaurants" :key="restaurant.id">
            {{ restaurant.name }}
            <button @click="editRestaurant(restaurant)">수정</button>
            <button @click="deleteRestaurant(restaurant.id)">삭제</button>
          </li>
        </ul>
      </div>
    </div>
    
    <!-- 옵션 추가/수정 모달 -->
    <modal v-if="showOptionModal" @close="showOptionModal = false">
      <template v-slot:header>
        <h3>{{ editingOption ? '옵션 수정' : '새 옵션 추가' }}</h3>
      </template>
      <template v-slot:body>
        <form @submit.prevent="saveOption">
          <input v-model="currentOption.name" placeholder="옵션 이름" required>
          <select v-model="currentOption.category" required>
            <option value="">카테고리 선택</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
          <button type="submit">저장</button>
        </form>
      </template>
    </modal>

    <!-- 식당 추가/수정 모달 -->
    <modal v-if="showRestaurantModal" @close="showRestaurantModal = false">
      <template v-slot:header>
        <h3>{{ editingRestaurant ? '식당 수정' : '새 식당 추가' }}</h3>
      </template>
      <template v-slot:body>
        <form @submit.prevent="saveRestaurant">
          <input v-model="currentRestaurant.name" placeholder="식당 이름" required>
          <input v-model="currentRestaurant.cuisine" placeholder="요리 종류" required>
          <input v-model="currentRestaurant.address" placeholder="주소" required>
          <button type="submit">저장</button>
        </form>
      </template>
    </modal>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import Modal from '@/components/Modal.vue';

export default {
  name: 'Admin',
  components: { Modal },
  setup() {
    const store = useStore();
    // 상태 변수들
    const options = ref([]);
    const restaurants = ref([]);
    const showOptionModal = ref(false);
    const showRestaurantModal = ref(false);
    const editingOption = ref(null);
    const editingRestaurant = ref(null);
    const currentOption = ref({});
    const currentRestaurant = ref({});
    const categories = ['음식 종류', '가격대', '분위기', '위치', '특별 요구사항'];

    // 컴포넌트 마운트 시 데이터 로드
    onMounted(async () => {
      await fetchOptions();
      await fetchRestaurants();
    });

    // 옵션 데이터 가져오기
    const fetchOptions = async () => {
      options.value = await store.dispatch('admin/fetchOptions');
    };

    // 식당 데이터 가져오기
    const fetchRestaurants = async () => {
      restaurants.value = await store.dispatch('admin/fetchRestaurants');
    };

    // 옵션 수정 모달 열기
    const editOption = (option) => {
      editingOption.value = option;
      currentOption.value = { ...option };
      showOptionModal.value = true;
    };

    // 식당 수정 모달 열기
    const editRestaurant = (restaurant) => {
      editingRestaurant.value = restaurant;
      currentRestaurant.value = { ...restaurant };
      showRestaurantModal.value = true;
    };

    // 옵션 저장 (추가 또는 수정)
    const saveOption = async () => {
      if (editingOption.value) {
        await store.dispatch('admin/updateOption', currentOption.value);
      } else {
        await store.dispatch('admin/addOption', currentOption.value);
      }
      showOptionModal.value = false;
      await fetchOptions();
    };

    // 식당 저장 (추가 또는 수정)
    const saveRestaurant = async () => {
      if (editingRestaurant.value) {
        await store.dispatch('admin/updateRestaurant', currentRestaurant.value);
      } else {
        await store.dispatch('admin/addRestaurant', currentRestaurant.value);
      }
      showRestaurantModal.value = false;
      await fetchRestaurants();
    };

    // 옵션 삭제
    const deleteOption = async (id) => {
      if (confirm('이 옵션을 삭제하시겠습니까?')) {
        await store.dispatch('admin/deleteOption', id);
        await fetchOptions();
      }
    };

    // 식당 삭제
    const deleteRestaurant = async (id) => {
      if (confirm('이 식당을 삭제하시겠습니까?')) {
        await store.dispatch('admin/deleteRestaurant', id);
        await fetchRestaurants();
      }
    };

    return {
      options,
      restaurants,
      showOptionModal,
      showRestaurantModal,
      editingOption,
      editingRestaurant,
      currentOption,
      currentRestaurant,
      categories,
      editOption,
      editRestaurant,
      saveOption,
      saveRestaurant,
      deleteOption,
      deleteRestaurant,
    };
  },
};
</script>

<style scoped>
.admin-panel {
  padding: 20px;
}

.admin-sections {
  display: flex;
  justify-content: space-between;
}

.section {
  width: 45%;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

button {
  margin-left: 10px;
}
</style>
