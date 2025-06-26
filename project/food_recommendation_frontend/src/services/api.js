import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1';
const MAX_RETRIES = 3;
const INITIAL_TIMEOUT = 300000; // 300초 (5분)

const logError = (error) => {
  console.error('API Error:', error);
  if (error.response) {
    console.error('Data:', error.response.data);
    console.error('Status:', error.response.status);
    console.error('Headers:', error.response.headers);
  } else if (error.request) {
    console.error('Request:', error.request);
  } else {
    console.error('Error:', error.message);
  }
};

const defaultHeaders = {
  'Content-Type': 'application/json'
};

const getRecommendationsWithRetry = async (data, retryCount = 0, timeout = INITIAL_TIMEOUT) => {
  try {
    const response = await axios({
      method: 'post',
      url: `${API_URL}/recommendations`,
      data: {
        selectedOptions: {
          selectedOptions: data.selectedOptions
        },
        excludedRestaurants: data.excludedRestaurants || []
      },
      headers: defaultHeaders,
      timeout: timeout
    });

    console.log('Recommendations response:', response.data);
    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED' && retryCount < MAX_RETRIES) {
      console.log(`Timeout occurred. Retrying (${retryCount + 1}/${MAX_RETRIES})...`);
      return getRecommendationsWithRetry(data, retryCount + 1, timeout * 1.5);
    }
    throw error;
  }
};

export default {
  async getOptions(category) {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/options`,
        params: { 
          category,
          timestamp: new Date().getTime() // 캐시 방지
        },
        headers: defaultHeaders,
        timeout: 30000
      });
      console.log('Options response:', response.data);
      return response.data;
    } catch (error) {
      logError(error);
      console.error('Error fetching options:', error);
      return [];
    }
  },

  async getRestaurants(filters) {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/restaurants`,
        params: filters,
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      console.error('Error fetching restaurants:', error);
      return [];
    }
  },

  async getRecommendations(data) {
    try {
      console.log('Sending recommendations request:', data);

      if (!data.selectedOptions || !Array.isArray(data.selectedOptions)) {
        throw new Error('선택된 옵션이 없습니다.');
      }

      return await getRecommendationsWithRetry(data);
    } catch (error) {
      logError(error);
      
      if (error.response?.status === 500) {
        console.error('Server Error:', error.response.data);
        return {
          error: "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
          detail: error.response.data.detail
        };
      }
      
      return {
        error: error.message || "추천을 가져오는데 실패했습니다."
      };
    }
  },

  // 관리자 기능 API
  async addRestaurant(restaurant) {
    try {
      const response = await axios.post(`${API_URL}/admin/restaurants`, restaurant, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async deleteRestaurant(id) {
    try {
      await axios.delete(`${API_URL}/admin/restaurants/${id}`, {
        headers: defaultHeaders,
        timeout: 30000
      });
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async addOption(option) {
    try {
      const response = await axios.post(`${API_URL}/admin/options`, option, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async deleteOption(id) {
    try {
      await axios.delete(`${API_URL}/admin/options/${id}`, {
        headers: defaultHeaders,
        timeout: 30000
      });
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async updateOption(id, option) {
    try {
      const response = await axios.put(`${API_URL}/admin/options/${id}`, option, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async getReviews(restaurantId) {
    try {
      if (!restaurantId) {
        throw new Error('Restaurant ID is undefined');
      }
      const response = await axios.get(`${API_URL}/reviews/${restaurantId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching reviews:', error);
      return [];
    }
  },
  

  async addReview(review) {
    try {
      console.log('Sending review:', review);  // 디버깅용 로그
      const response = await axios.post(`${API_URL}/reviews`, review);
      console.log('Review response:', response.data);  // 디버깅용 로그
      return response.data;
    } catch (error) {
      console.error('Error in addReview:', error);
      throw error;
    }
  },
  
  async deleteReview(id) {
    try {
      await axios.delete(`${API_URL}/admin/reviews/${id}`, {
        headers: defaultHeaders,
        timeout: 30000
      });
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async updateReview(id, review) {
    try {
      const response = await axios.put(`${API_URL}/admin/reviews/${id}`, review, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  // 선택된 식당 관리 API
  async saveSelectedRestaurant(restaurant) {
    try {
      const response = await axios.post(`${API_URL}/selected-restaurant`, restaurant, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },

  async getSelectedRestaurants() {
    try {
      const response = await axios.get(`${API_URL}/selected-restaurants`, {
        headers: defaultHeaders,
        timeout: 30000
      });
      return response.data;
    } catch (error) {
      logError(error);
      console.error('Error fetching selected restaurants:', error);
      return [];
    }
  },

  async setExclusionDays(days) {
    try {
      const response = await axios.post(`${API_URL}/admin/settings/exclusion-days`, { days: parseInt(days) });
      return response.data;
    } catch (error) {
      logError(error);
      throw error;
    }
  },
  
  async getExclusionDays() {
    try {
      const response = await axios.get(`${API_URL}/admin/settings/exclusion-days`);
      return response.data.days;
    } catch (error) {
      logError(error);
      return 7; // 기본값
    }
  },
}
