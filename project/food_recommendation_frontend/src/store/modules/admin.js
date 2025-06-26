import api from '@/services/api';

const state = {
  restaurants: [],
  options: [],
  reviews: []
};

const mutations = {
  SET_RESTAURANTS(state, restaurants) {
    state.restaurants = restaurants;
  },
  SET_OPTIONS(state, options) {
    state.options = options;
  },
  SET_REVIEWS(state, reviews) {
    state.reviews = reviews;
  },
  ADD_RESTAURANT(state, restaurant) {
    state.restaurants.push(restaurant);
  },
  REMOVE_RESTAURANT(state, id) {
    state.restaurants = state.restaurants.filter(r => r.id !== id);
  },
  ADD_OPTION(state, option) {
    state.options.push(option);
  },
  REMOVE_OPTION(state, id) {
    state.options = state.options.filter(o => o.id !== id);
  },
  ADD_REVIEW(state, review) {
    state.reviews.push(review);
  },
  REMOVE_REVIEW(state, id) {
    state.reviews = state.reviews.filter(r => r.id !== id);
  }
};

const actions = {
  async fetchRestaurants({ commit }) {
    const restaurants = await api.getRestaurants();
    commit('SET_RESTAURANTS', restaurants);
  },
  async addRestaurant({ commit }, restaurant) {
    const newRestaurant = await api.addRestaurant(restaurant);
    commit('ADD_RESTAURANT', newRestaurant);
  },
  async deleteRestaurant({ commit }, id) {
    await api.deleteRestaurant(id);
    commit('REMOVE_RESTAURANT', id);
  },
  async fetchOptions({ commit }) {
    const options = await api.getOptions();
    commit('SET_OPTIONS', options);
  },
  async addOption({ commit }, option) {
    const newOption = await api.addOption(option);
    commit('ADD_OPTION', newOption);
  },
  async deleteOption({ commit }, id) {
    await api.deleteOption(id);
    commit('REMOVE_OPTION', id);
  },
  async fetchReviews({ commit }) {
    const reviews = await api.getReviews();
    commit('SET_REVIEWS', reviews);
  },
  async addReview({ commit }, review) {
    const newReview = await api.addReview(review);
    commit('ADD_REVIEW', newReview);
  },
  async deleteReview({ commit }, id) {
    await api.deleteReview(id);
    commit('REMOVE_REVIEW', id);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
