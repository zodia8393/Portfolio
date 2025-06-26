<template>
  <div class="restaurant-card" :class="{ 'is-flipped': isFlipped }" @click="$emit('click')">
    <div class="card-inner">
      <div class="card-front">
        <div class="card-frame">
          <img src="@/assets/images/card-back.png" alt="Card Back" class="frame-image">
        </div>
      </div>
      <div class="card-back">
        <div class="card-frame">
          <img src="@/assets/images/card-front.png" alt="Card Front" class="frame-image">
          <div class="card-content">
            <h3>{{ restaurant.name }}</h3>
            <p class="cuisine">{{ restaurant.cuisine }}</p>
            <div class="rating">
              <span v-for="i in 5" :key="i" :class="{ 'filled': i <= restaurant.rating }">★</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  export default {
    name: 'RestaurantCard',
    props: {
      restaurant: {
        type: Object,
        required: true
      },
      isFlipped: {
        type: Boolean,
        default: false
      }
    }
  };
  </script>
  
  <style scoped>
  .restaurant-card {
    width: 250px;
    height: 350px;
    perspective: 1000px;
    cursor: pointer;
  }
  
  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s;
    transform-style: preserve-3d;
  }
  
  .restaurant-card.is-flipped .card-inner {
    transform: rotateY(180deg);
  }
  
  .card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
  }
  
  .card-back {
    transform: rotateY(180deg);
  }
  
  .card-frame {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .frame-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    pointer-events: none;
  }
  
  .card-content {
    position: relative;
    z-index: 1;
    padding: 20px;
    width: 80%;
    margin: 0 auto;
    text-align: center;
  }
  
  .card-content h3 {
    font-size: 1.5em;
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    margin: 0 0 10px;
    word-break: keep-all;
    line-height: 1.2;
  }
  
  .cuisine {
    color: #FFD700;
    font-size: 1.1em;
    margin: 10px 0;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  }
  
  .rating {
    color: #FFD700;
    font-size: 1.2em;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  }
  
  .rating span {
    margin: 0 2px;
  }
  
  .rating .filled {
    color: #FFD700;
  }
  
  @media (max-width: 768px) {
    .restaurant-card {
      width: 200px;
      height: 280px;
    }
    
    .card-content h3 {
      font-size: 1.3em;
    }
    
    .cuisine {
      font-size: 1em;
    }
    
    .rating {
      font-size: 1.1em;
    }
  }
  </style>
  