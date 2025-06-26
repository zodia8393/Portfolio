<template>
    <div class="card-deck">
      <div v-for="(card, index) in selectedCards" :key="index" class="selected-card">
        <img :src="card.image" :alt="card.name" class="card-image">
        <span class="card-name">{{ card.name }}</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CardDeck',
    props: {
      selectedCards: {
        type: Array,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  .card-deck {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1vw;
    margin-top: 2vh;
  }
  
  .selected-card {
    position: relative;
    width: 10vw;
    height: 15vw;
    border-radius: 0.5vw;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
  }
  
  .card-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .card-name {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0,0,0,0.7);
    color: white;
    padding: 0.5vw;
    font-size: 1vw;
    text-align: center;
  }
  
  @media (max-width: 768px) {
    .selected-card {
      width: 20vw;
      height: 30vw;
    }
  
    .card-name {
      font-size: 2vw;
    }
  }
  </style>
  