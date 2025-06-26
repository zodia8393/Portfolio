// src/store/modules/auth.js
import api from '@/services/api';

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    user: null
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    SET_USER(state, user) {
      state.user = user;
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login', credentials);
        const token = response.data.access_token;
        commit('SET_TOKEN', token);
        return response.data;
      } catch (error) {
        commit('SET_TOKEN', null);
        throw error;
      }
    },
    async refreshToken({ commit }) {
      try {
        const response = await api.post('/auth/refresh-token');
        const token = response.data.access_token;
        commit('SET_TOKEN', token);
        return response.data;
      } catch (error) {
        commit('SET_TOKEN', null);
        throw error;
      }
    },
    logout({ commit }) {
      commit('SET_TOKEN', null);
      commit('SET_USER', null);
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    getToken: state => state.token
  }
};
