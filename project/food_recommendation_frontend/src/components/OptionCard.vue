<template>
  <div 
    class="option-card" 
    :class="{ 
      'is-flipped': isFlipped,
      'is-selected': isSelected 
    }" 
    @click="$emit('click')"
  >
    <div class="card-inner">
      <div class="card-front">
        <div class="card-frame">
          <img src="@/assets/images/option-card-frame.png" alt="Card Frame" class="frame-image">
          <div class="card-content">
            <h3>{{ option.name }}</h3>
          </div>
        </div>
      </div>
      <div class="card-back">
        <div class="card-frame">
          <img src="@/assets/images/card-back.png" alt="Card Back" class="frame-image">
        </div>
      </div>
    </div>
    <div class="card-glow"></div>
  </div>
</template>
  
  <script>
  export default {
    name: 'OptionCard',
    props: {
      option: {
        type: Object,
        required: true
      },
      isFlipped: {
        type: Boolean,
        default: false
      },
      isSelected: {
        type: Boolean,
        default: false
      }
    }
  };
  </script>
  
  <style scoped>
  .option-card {
    width: 250px;
    height: 350px;
    perspective: 1000px;
    position: relative;
    cursor: pointer;
    margin: 20px;
  }
  
  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
  }
  
  .option-card.is-flipped .card-inner {
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
  }
  
  .card-content h3 {
    font-size: 1.8em;
    color: #FFD700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    margin: 0;
    word-break: keep-all;
    line-height: 1.2;
  }
  
  .option-card.is-selected .card-glow {
    box-shadow: 0 0 30px #FFD700;
  }
  
  @keyframes select-glow {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
  }
  
  .option-card.is-selected {
    animation: select-glow 0.5s ease-in-out;
  }
  
  @media (max-width: 768px) {
    .option-card {
      width: 200px;
      height: 280px;
    }
    
    .card-content h3 {
      font-size: 1.5em;
    }
  }
  </style>
  