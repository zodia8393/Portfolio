import api from '@/services/api';

const state = {
  allRestaurants: [],
  currentRestaurant: null,
};

const mutations = {
  SET_ALL_RESTAURANTS(state, restaurants) {
    state.allRestaurants = restaurants;
  },
  SET_CURRENT_RESTAURANT(state, restaurant) {
    state.currentRestaurant = restaurant;
  },
};

const actions = {
  async fetchAllRestaurants({ commit }) {
    try {
      const response = await api.get('/restaurants');
      commit('SET_ALL_RESTAURANTS', response.data);
    } catch (error) {
      console.error('Error fetching restaurants:', error);
    }
  },
  async fetchRestaurant({ commit }, id) {
    try {
      const response = await api.get(`/restaurants/${id}`);
      commit('SET_CURRENT_RESTAURANT', response.data);
    } catch (error) {
      console.error('Error fetching restaurant:', error);
    }
  },
};

const getters = {
  getRestaurantById: (state) => (id) => {
    return state.allRestaurants.find(restaurant => restaurant.id === id);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
