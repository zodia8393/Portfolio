<template>
    <form @submit.prevent="submitReview" class="review-form">
      <div class="form-group">
        <label for="rating">평점:</label>
        <select v-model="review.rating" id="rating" required>
          <option v-for="i in 5" :key="i" :value="i">{{ i }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="comment">리뷰:</label>
        <textarea v-model="review.comment" id="comment" required></textarea>
      </div>
      <button type="submit">리뷰 작성</button>
    </form>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'ReviewForm',
    emits: ['submit-review'],
    setup(props, { emit }) {
      const review = ref({
        rating: 5,
        comment: ''
      });
  
      const submitReview = () => {
        emit('submit-review', { ...review.value });
        review.value = { rating: 5, comment: '' };
      };
  
      return {
        review,
        submitReview
      };
    }
  };
  </script>
  
  <style scoped>
  .review-form {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    color: #FFD700;
  }
  
  select, textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.8);
  }
  
  textarea {
    height: 100px;
    resize: vertical;
  }
  
  button {
    background-color: #FFD700;
    color: #000;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }
  
  button:hover {
    background-color: #FFC800;
  }
  </style>
  