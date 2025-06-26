import api from '@/services/api';

const state = {
  user: null,
  token: localStorage.getItem('token') || null,
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
  },
  SET_TOKEN(state, token) {
    state.token = token;
    localStorage.setItem('token', token);
  },
  CLEAR_USER(state) {
    state.user = null;
    state.token = null;
    localStorage.removeItem('token');
  },
};

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await api.post('/login', credentials);
      commit('SET_TOKEN', response.data.token);
      commit('SET_USER', response.data.user);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  async logout({ commit }) {
    commit('CLEAR_USER');
  },
  async fetchUserProfile({ commit }) {
    try {
      const response = await api.get('/user/profile');
      commit('SET_USER', response.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  },
  async updateUserProfile({ commit }, profileData) {
    try {
      const response = await api.put('/user/profile', profileData);
      commit('SET_USER', response.data);
    } catch (error) {
      console.error('Error updating user profile:', error);
      throw error;
    }
  },
};

const getters = {
  isLoggedIn: state => !!state.token,
  currentUser: state => state.user,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
