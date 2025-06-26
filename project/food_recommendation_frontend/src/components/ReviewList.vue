<template>
    <div class="review-list">
      <div v-if="reviews.length === 0" class="no-reviews">
        아직 리뷰가 없습니다.
      </div>
      <div v-else v-for="review in reviews" :key="review.id" class="review">
        <div class="rating">
          <span v-for="i in 5" :key="i" :class="{ 'filled': i <= review.rating }">★</span>
        </div>
        <p class="comment">{{ review.comment }}</p>
        <p class="date">{{ formatDate(review.date) }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ReviewList',
    props: {
      reviews: {
        type: Array,
        required: true
      }
    },
    methods: {
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('ko-KR', options);
      }
    }
  };
  </script>
  
  <style scoped>
  .review-list {
    margin-top: 20px;
  }
  
  .no-reviews {
    text-align: center;
    color: #999;
    font-style: italic;
  }
  
  .review {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
  }
  
  .rating {
    margin-bottom: 10px;
  }
  
  .rating span {
    color: #ddd;
    font-size: 1.2em;
  }
  
  .rating .filled {
    color: #FFD700;
  }
  
  .comment {
    margin-bottom: 10px;
    color: #fff;
  }
  
  .date {
    font-size: 0.8em;
    color: #999;
    text-align: right;
  }
  </style>
  