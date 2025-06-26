import api from '@/services/api';

const state = {
  currentCategory: '',
  currentOptions: [],
  selectedOptions: [],
  recommendations: [],
  categories: ['분류', '주차장', '룸', '도보/차량'],
  currentCategoryIndex: 0,
  usedCategories: new Set(),
  isLoading: false,
  randomSelectionInProgress: false,
  excludedRestaurants: []
};

const mutations = {
  SET_CURRENT_CATEGORY(state, category) {
    state.currentCategory = category;
  },
  SET_CURRENT_OPTIONS(state, options) {
    state.currentOptions = options;
  },
  ADD_SELECTED_OPTION(state, option) {
    state.selectedOptions.push(option);
    state.usedCategories.add(option.category);
  },
  SET_LOADING(state, isLoading) {
    state.isLoading = isLoading;
  },
  SET_RECOMMENDATIONS(state, recommendations) {
    state.recommendations = recommendations;
  },
  SET_RANDOM_SELECTION_IN_PROGRESS(state, inProgress) {
    state.randomSelectionInProgress = inProgress;
  },
  SET_FINAL_SELECTION(state, selection) {
    state.finalSelection = selection;
  },  
  RESET_DECISION(state) {
    state.currentCategoryIndex = 0;
    state.selectedOptions = [];
    state.recommendations = null;
    state.usedCategories = new Set();
    state.currentCategory = '';
    state.currentOptions = [];
    state.isLoading = false;
    state.excludedRestaurants = [];
  },
  SET_SELECTED_OPTIONS(state, options) {
    state.selectedOptions = options;
  },
  ADD_EXCLUDED_RESTAURANT(state, restaurantName) {
    if (!state.excludedRestaurants.includes(restaurantName)) {
      state.excludedRestaurants.push(restaurantName);
    }
  },
  ADD_USED_CATEGORY(state, category) {
    state.usedCategories.add(category);
  },
  RESET_USED_CATEGORIES(state) {
    state.usedCategories.clear();
  },
  INCREMENT_CATEGORY_INDEX(state) {
    state.currentCategoryIndex = (state.currentCategoryIndex + 1) % state.categories.length;
  }
};

const actions = {
  async fetchOptions({ commit, state }) {
    if (state.isLoading || state.usedCategories.size === state.categories.length) {
      return;
    }

    try {
      commit('SET_LOADING', true);
      
      const nextCategory = state.categories.find(category => !state.usedCategories.has(category));
      if (nextCategory) {
        commit('SET_CURRENT_CATEGORY', nextCategory);
        console.log('Fetching options for category:', nextCategory);
        const response = await api.getOptions(nextCategory);
        console.log('Fetched options:', response);
        commit('SET_CURRENT_OPTIONS', response);
      }
    } catch (error) {
      console.error('Error in fetchOptions:', error);
      commit('SET_CURRENT_OPTIONS', []);
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async selectOption({ commit, state, dispatch }, option) {
    try {
      commit('ADD_SELECTED_OPTION', option);
      commit('INCREMENT_CATEGORY_INDEX');
      
      if (state.usedCategories.size < state.categories.length) {
        await dispatch('fetchOptions');
      } else {
        const response = await api.getRecommendations({
          selectedOptions: state.selectedOptions,
          excludedRestaurants: state.excludedRestaurants
        });
        commit('SET_RECOMMENDATIONS', response);
      }
    } catch (error) {
      console.error('Error in selectOption:', error);
    }
  },

  // skipCategory 액션 수정
  async skipCategory({ state, dispatch }) {  // commit 제거
    try {
      // 현재 카테고리에 대한 '무관' 옵션 생성
      const skipOption = {
        id: `${state.currentCategory}_무관`,
        name: '무관',
        category: state.currentCategory
      };

      // '무관' 옵션을 선택한 것처럼 처리
      await dispatch('selectOption', skipOption);
    } catch (error) {
      console.error('Error in skipCategory:', error);
    }
  },

  async getRecommendations({ commit, state }, { selectedOptions }) {
    try {
      commit('SET_SELECTED_OPTIONS', selectedOptions);
      
      const response = await api.getRecommendations({
        selectedOptions: selectedOptions,
        excludedRestaurants: state.excludedRestaurants
      });
  
      if (response && !response.error) {
        commit('SET_RECOMMENDATIONS', response);
        if (response.db_recommendation) {
          commit('ADD_EXCLUDED_RESTAURANT', response.db_recommendation.name);
        }
        if (response.ai_recommendation) {
          commit('ADD_EXCLUDED_RESTAURANT', response.ai_recommendation.name);
        }
      }
      return response;
    } catch (error) {
      console.error('Error in getRecommendations:', error);
      return {
        error: "추천을 가져오는데 실패했습니다."
      };
    }
  },

  // randomSelect 액션 수정
  async randomSelect({ commit, state, dispatch }) {
    if (state.randomSelectionInProgress) return;
    
    try {
      commit('SET_RANDOM_SELECTION_IN_PROGRESS', true);
      
      const optionsPromises = state.categories
        .filter(category => !state.usedCategories.has(category))
        .map(category => api.getOptions(category));
      
      const optionsResponses = await Promise.all(optionsPromises);
      
      for (let i = 0; i < optionsResponses.length; i++) {
        const options = optionsResponses[i];
        if (options && options.length > 0) {
          const randomOption = options[Math.floor(Math.random() * options.length)];
          await dispatch('selectOption', randomOption);
        }
      }
    } catch (error) {
      console.error('Error in randomSelect:', error);
    } finally {
      commit('SET_RANDOM_SELECTION_IN_PROGRESS', false);
    }
  },


  resetDecision({ commit }) {
    commit('RESET_DECISION');
    commit('RESET_USED_CATEGORIES');
  },

  initializeDecision({ dispatch }) {
    return dispatch('fetchOptions');
  }
};

const getters = {
  isSelectionComplete: state => state.usedCategories.size === state.categories.length,
  remainingCategories: state => state.categories.filter(
    category => !state.usedCategories.has(category)
  ),
  getCurrentCategory: state => state.currentCategory,
  getUsedCategories: state => state.usedCategories
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
