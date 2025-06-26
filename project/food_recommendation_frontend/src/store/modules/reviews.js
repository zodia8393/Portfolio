import api from '@/services/api';

const state = {
  restaurantReviews: {},
};

const mutations = {
  SET_RESTAURANT_REVIEWS(state, { restaurantId, reviews }) {
    state.restaurantReviews = {
      ...state.restaurantReviews,
      [restaurantId]: reviews,
    };
  },
  ADD_REVIEW(state, { restaurantId, review }) {
    if (!state.restaurantReviews[restaurantId]) {
      state.restaurantReviews[restaurantId] = [];
    }
    state.restaurantReviews[restaurantId].push(review);
  },
};

const actions = {
  async fetchReviews({ commit }, restaurantId) {
    try {
      const response = await api.get(`/restaurants/${restaurantId}/reviews`);
      commit('SET_RESTAURANT_REVIEWS', { restaurantId, reviews: response.data });
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  },
  async submitReview({ commit }, { restaurantId, review }) {
    try {
      const response = await api.post(`/restaurants/${restaurantId}/reviews`, review);
      commit('ADD_REVIEW', { restaurantId, review: response.data });
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
