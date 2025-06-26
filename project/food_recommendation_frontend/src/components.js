import { defineComponent } from 'vue';
import imageConfig from '@/config/imageConfig';

// 옵션 카드 컴포넌트
export const OptionCard = defineComponent({
  props: ['option', 'isFlipped'],
  data() {
    return {
      imageConfig
    }
  },
  template: `
    <div class="card" :class="{ 'is-flipped': isFlipped }">
      <div class="card-inner">
        <div class="card-front">
          <img :src="imageConfig.CARD_BACK" alt="Card Back">
        </div>
        <div class="card-back">
          <img :src="imageConfig.OPTION_CARD_FRAME" alt="Card Frame" class="card-frame">
          <div class="card-content">
            <h3>{{ option.name }}</h3>
            <p>{{ option.description }}</p>
          </div>
        </div>
      </div>
    </div>
  `,
  style: `
    /* 카드 스타일링 */
    .card {
      width: 240px;
      height: 340px;
      perspective: 1000px;
      cursor: pointer;
    }
    /* 카드 내부 스타일링 */
    .card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
    }
    /* 카드 뒤집기 애니메이션 */
    .card.is-flipped .card-inner {
      transform: rotateY(180deg);
    }
    /* 카드 앞면과 뒷면 공통 스타일 */
    .card-front, .card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
    }
    /* 카드 이미지 스타일링 */
    .card-front img, .card-back img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    /* 카드 뒷면 회전 */
    .card-back {
      transform: rotateY(180deg);
    }
    /* 카드 내용 스타일링 */
    .card-content {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #FFD700;
      text-shadow: 2px 2px 2px #000;
    }
  `
});

// 레스토랑 카드 컴포넌트
export const RestaurantCard = defineComponent({
  props: ['restaurant', 'isFlipped'],
  template: `
    <div class="card" :class="{ 'is-flipped': isFlipped }">
      <div class="card-inner">
        <div class="card-front">
          <img :src="require('@/assets/images/card-back.png')" alt="Card Back">
        </div>
        <div class="card-back">
          <h3>{{ restaurant.name }}</h3>
          <p>{{ restaurant.cuisine }}</p>
          <p>Rating: {{ restaurant.rating }}</p>
          <img :src="restaurant.image" alt="Restaurant Image">
        </div>
      </div>
    </div>
  `,
  style: `
    /* 레스토랑 카드 스타일링 */
    .card {
      width: 200px;
      height: 300px;
      perspective: 1000px;
      cursor: pointer;
    }
    /* 카드 내부 스타일링 */
    .card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
    }
    /* 카드 뒤집기 애니메이션 */
    .card.is-flipped .card-inner {
      transform: rotateY(180deg);
    }
    /* 카드 앞면과 뒷면 공통 스타일 */
    .card-front, .card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    /* 카드 앞면 이미지 스타일링 */
    .card-front img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 10px;
    }
    /* 카드 뒷면 스타일링 */
    .card-back {
      background-color: #f8f8f8;
      transform: rotateY(180deg);
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      padding: 20px;
    }
    /* 카드 뒷면 이미지 스타일링 */
    .card-back img {
      max-width: 100%;
      max-height: 150px;
      object-fit: contain;
    }
  `
});

// 카드 덱 컴포넌트
export const CardDeck = defineComponent({
    props: ['selectedCards'],
    data() {
      return {
        hoveredCard: null
      }
    },
    methods: {
      showCard(card) {
        this.hoveredCard = card;
      },
      hideCard() {
        this.hoveredCard = null;
      }
    },
    template: `
      <div class="card-deck">
        <div v-for="(card, index) in selectedCards" :key="index" class="deck-card" 
             @mouseover="showCard(card)" @mouseleave="hideCard">
          <span class="card-name">{{ card.name }}</span>
        </div>
        <div v-if="hoveredCard" class="hovered-card">
          <OptionCard :option="hoveredCard" :isFlipped="true" />
        </div>
      </div>
    `,
    style: `
      /* 카드 덱 스타일링 */
      .card-deck {
        position: fixed;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
      }
      /* 덱 내 개별 카드 스타일링 */
      .deck-card {
        width: 150px;
        height: 30px;
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        padding-left: 10px;
        cursor: pointer;
      }
      /* 호버된 카드 스타일링 */
      .hovered-card {
        position: absolute;
        left: -220px;
        top: 0;
      }
    `
  });
  
// 리뷰 폼 컴포넌트
export const ReviewForm = defineComponent({
  data() {
    return {
      rating: 0,
      comment: ''
    }
  },
  methods: {
    submitReview() {
      this.$emit('submit-review', { rating: this.rating, comment: this.comment });
      this.rating = 0;
      this.comment = '';
    }
  },
  template: `
    <form @submit.prevent="submitReview">
      <div>
        <label for="rating">Rating:</label>
        <input id="rating" v-model.number="rating" type="number" min="1" max="5">
      </div>
      <div>
        <label for="comment">Comment:</label>
        <textarea id="comment" v-model="comment"></textarea>
      </div>
      <button type="submit">Submit Review</button>
    </form>
  `
});

// 리뷰 목록 컴포넌트
export const ReviewList = defineComponent({
  props: ['reviews'],
  template: `
    <div class="review-list">
      <div v-for="review in reviews" :key="review.id" class="review">
        <p>Rating: {{ review.rating }}/5</p>
        <p>{{ review.comment }}</p>
      </div>
    </div>
  `
});
