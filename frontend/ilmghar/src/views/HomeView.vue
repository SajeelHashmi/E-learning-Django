<template>
    <div>
      <div class="">
        <div class="flex justifyCenter m-t-2em section">
      <div class="m-t-2em m-b-2em " >
        <img class="heroImg" src="@/assets/Hero.png"  />
        
      </div>
    </div>
        <!-- <carousel class="" :items="carouselItems" /> -->
        <div class="section flex space-around align-center">
          <div>
            
            <img src="@/assets/harvard.webp" alt="">
          </div>
          <div>
            <img src="@/assets/Berkerly.webp" alt="">
          </div>
          <div>
            <img src="@/assets/Cambridge.webp" alt="">
          </div>
          <div>
            <img src="@/assets/Boston.webp" alt="">
          </div>
          <div>
            <img src="@/assets/oxford.webp" alt="">
          </div>
        </div>
      </div>

      <div class="section courses with languages">

        <div >
          <h1 class="heading">
            <span class="yellow">
               Learn in 

            </span>
            <span class="blue">
              your languages: 
            </span>
          </h1>
        </div>

        <div v-if="urduCourses" class="flex courseBoxLang align-center">
          
          <CourseCard v-for="course in urduCourses" :key="course.id" :course="course"></CourseCard>
          <div>
            <RouterLink to="/explore">

              <img src="@/assets/arrow.png" alt="" srcset="">
            </RouterLink>
          </div>
        </div>
        <div>
          <h2 v-if="urduCourses.length>0" class="subheading text-center ">
            <span class="blue text-center">
              Urdu
            </span>
          </h2>
        </div>

        <div v-if="punjabiCourses.length > 0 " class="flex courseBoxLang align-center">
         
          <CourseCard v-for="course in punjabiCourses" :key="course.id" :course="course"></CourseCard>
          <div>
            <RouterLink to="/explore">

            <img src="@/assets/arrow.png" alt="" srcset="">
            </RouterLink>

          </div>
        </div>
        <div>
          <h2 v-if="punjabiCourses.length > 0" class="subheading text-center ">
            <span class="blue text-center">
              Punjabi 
            </span>
          </h2>
        </div>
        

        <div v-if="englishCourses.length>0" class="flex courseBoxLang align-center">
          
          <CourseCard v-for="course in englishCourses" :key="course.id" :course="course"></CourseCard>
          <div>
            <RouterLink to="/explore">

            <img src="@/assets/arrow.png" alt="" srcset="">
            </RouterLink>
          </div>
        </div>
        <div>
          <h2 v-if="englishCourses.length > 0" class="subheading text-center ">
            <span class="blue text-center">
              English
            </span>
          </h2>
        </div>
        <div >
          <h1 class="heading">
            <span class="blue">
              Testimonials: 
            </span>
          </h1>
        </div>
        <div class="flex align-center justifyCenter testimonialDiv">
          <div class="testimonialCard">
            <img src="@/assets/testimonial1.jpg" alt="" srcset="">
            <div class="subheading flex justifyCenter">

              <p class="blue text-center">

                "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Amet molestiae a exercitationem at odit ducimus beatae nisi cum totam iste?"
              </p>
              
            </div>
          </div>
          <div class="testimonialCard">
            <img src="@/assets/testimonial2.jpg" alt="" srcset="">
            <div class="subheading flex justifyCenter">

                <p class="blue text-center">

                  "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Amet molestiae a exercitationem at odit ducimus beatae nisi cum totam iste?"
                </p>

                </div>     
            </div>
          <div class="testimonialCard">
            <img src="@/assets/testimonial1.jpg" alt="" srcset="">
            <div class="subheading flex justifyCenter">

                <p class="blue text-center">

                  "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Amet molestiae a exercitationem at odit ducimus beatae nisi cum totam iste?"
                </p>

            </div>
          </div>
        </div>
        

      </div>
    </div>
  </template>
  
<script>
import Carousel from '@/components/Carousel.vue';
import CourseCard from '@/components/CourseCard.vue';
import axios from "axios";
export default {
  components: {
    Carousel,
    CourseCard
  },
  data() {
    return {
      englishCourses:[],
      urduCourses:[],
      punjabiCourses:[],
      carouselItems: [
        
        { id: 1, imageUrl: './src/assets/Hero.png' },
        { id: 2, imageUrl: './src/assets/Hero.png' },
      ],
    };
  },
  mounted() {
    this.fetchCourses();
  },
  methods:{
    async fetchCourses(){
      const urdu = await axios.get('http://127.0.0.1:8000/api/courses/threebylang/urdu')
      const english = await axios.get('http://127.0.0.1:8000/api/courses/threebylang/english')
      const punjabi = await axios.get('http://127.0.0.1:8000/api/courses/threebylang/punjabi')
      console.log(urdu.data)
      this.urduCourses = urdu.data
      this.englishCourses = english.data
      this.punjabiCourses = punjabi.data
    },
  }
};
</script>

<style>
  .test{
    background-color: black;
  }

  .courseBoxLang{
    margin-left: 5%;
  }
  .testimonialDiv{
    width: 100%;
  }
  .testimonialCard img{
    width: 100%;
    height: auto;
    border-radius: 20px;

  }
  
  .heroImg{
    width: 100%;
    height: auto;
    border-radius: 50px;
  }

  .testimonialCard{
    margin-left: 10px;
    margin-right: 10px;
  }
</style>  