<template>
    <div class="carousel">
      <div class="slides" >
        <div v-for="(item, index) in items" :key="index" class="slide" :class="{ active: index === currentIndex }">
          <img :src="item.imageUrl" alt="Slide Image" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      items: Array,
    },
    data() {
      return {
        currentIndex: 0,
        intervalId: null,
      };
    },
    methods: {
      startSlider() {
        // Automatically advance to the next slide every 3 seconds
        this.intervalId = setInterval(() => {
          this.nextSlide();
        }, 3000);
      },
      stopSlider() {
        // Stop the automatic sliding when the component is destroyed
        clearInterval(this.intervalId);
      },
      nextSlide() {
        // Move to the next slide
        this.currentIndex = (this.currentIndex + 1) % this.items.length;
      },
    },
    created() {
      // Start the automatic sliding when the component is created
      this.startSlider();
    },
    beforeDestroy() {
      // Stop the automatic sliding when the component is destroyed
      this.stopSlider();
    },
  };
  </script>
  
  <style scoped>
  .carousel {
    position: relative;
    overflow: hidden;
    margin: auto;
    width: 100%;
    height: 400px;
    display: flex;
    justify-content: center;
  }
  
  .slides {
    display: flex;
    transition: transform 0.5s ease-in-out;
    min-width: 100%;
    
  }
  
  .slide {
    position: absolute;
    display: flex;
    justify-content: center;
    width: 100%;
    transition: opacity 0.5s ease-in-out;
    opacity: 0;
  }
  
  .slide.active {
    opacity: 1;
  }
  </style>
  