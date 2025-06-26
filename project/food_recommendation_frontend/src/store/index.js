import { createStore } from 'vuex';
import decision from './modules/decision';
import restaurants from './modules/restaurants';
import reviews from './modules/reviews';
import user from './modules/user';

export default createStore({
  modules: {
    decision,
    restaurants,
    reviews,
    user
  }
});
