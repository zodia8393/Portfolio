import axios from 'axios';

// API 기본 설정
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL
});

// 인증 관련 서비스
export const authService = {
  // 일반 사용자 로그인
  login: (credentials) => api.post('/auth/login', credentials),
  // 관리자 로그인
  adminLogin: (credentials) => api.post('/auth/admin-login', credentials)
};

// 옵션 관련 서비스
export const optionService = {
  // 모든 옵션 가져오기
  getOptions: () => api.get('/options'),
  // 특정 옵션 선택하기
  selectOption: (optionId) => api.post('/options/select', { optionId })
};

// 식당 관련 서비스
export const restaurantService = {
  // 추천 식당 목록 가져오기
  getRecommendations: () => api.get('/restaurants/recommendations'),
  // 특정 식당의 상세 정보 가져오기
  getRestaurantDetails: (id) => api.get(`/restaurants/${id}`)
};

// 리뷰 관련 서비스
export const reviewService = {
  // 특정 식당의 리뷰 목록 가져오기
  getReviews: (restaurantId) => api.get(`/reviews/${restaurantId}`),
  // 특정 식당에 리뷰 작성하기
  submitReview: (restaurantId, review) => api.post(`/reviews/${restaurantId}`, review)
};

// 사용자 관련 서비스
export const userService = {
  // 현재 사용자의 프로필 정보 가져오기
  getUserProfile: () => api.get('/users/profile'),
  // 현재 사용자의 프로필 정보 업데이트하기
  updateUserProfile: (profile) => api.put('/users/profile', profile)
};
