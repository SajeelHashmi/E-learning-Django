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


      <div class="section ">

        <div >
          <h1 class="heading">

            <span class="blue">
              Our Mission
            </span>
          </h1>
        </div>
<div class="sectionNoShadow ourMission">
          <h3 class="text-center blue">
            "At Ilm Ghar, our mission is to break down linguistic barriers and foster inclusive learning by providing accessible, engaging, and high-quality educational resources in local languages. Recognizing the rich linguistic diversity in Pakistan, we aim to empower students across the nation, especially in rural areas and those with linguistic preferences for Punjabi, Pushto, Seraiki, Urdu, and Sindhi."
          </h3>
          <h3 class="blue">

            We are committed to addressing the challenges posed by the absence of educational materials in local languages. Our platform strives to:
          </h3>
          <ul class="sectionNoShadow">
            <li>
              <span class="blue">
                Enhance Accessibility:
              </span>
               Ilm Ghar seeks to bridge the gap in educational accessibility by offering a diverse range of courses and materials in local languages. We believe that every student should have equal access to quality educational resources, regardless of their linguistic background.
            </li>


            <li>
              <span class="blue">
                Promote Engagement:
              </span>
             We understand the pivotal role language plays in effective learning. Ilm Ghar is dedicated to creating an environment where students can learn in the language they are most comfortable with, fostering greater engagement, understanding, and academic success.
            </li>
            <li>
              <span class="blue">
                Provide Quality Learning Materials:
              </span>
               Ilm Ghar is committed to producing and curating high-quality educational content in local languages. By doing so, we aim to elevate the overall standard of education, ensuring that students have access to materials that meet the highest educational standards.
            </li>

            <li>
              <span class="blue">
                Cultural Relevance:
                            </span>
               Our platform recognizes the cultural nuances embedded in local languages. Ilm Ghar endeavors to incorporate cultural relevance into educational materials, enhancing students' depth of understanding and fostering cultural appreciation in the learning process.
            </li>
            <li>
              <span class="blue">
                Address Educational Inequality:
                            </span>
               Ilm Ghar actively works towards reducing educational inequality by focusing on students who have been underserved in terms of linguistic preferences. We believe that providing education in local languages is a key step in leveling the playing field and promoting equal opportunities for success and personal development.
            </li>
          </ul>
          <h3 class="text-center blue">
"Ilm Ghar is not just an online learning platform; it's a catalyst for positive change in the educational landscape of Pakistan. Join us in our mission to empower students, celebrate linguistic diversity, and build a brighter future through accessible and culturally relevant education."

          </h3>





    




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

  },
  data() {
    return {
          
    };
  },

};
</script>

<style>
  .test{
    background-color: black;
  }

 .ourMission{
  font-size: 1.25em;
 }
 .ourMission li{
  font-size: 1.25em;
  font-weight: 100;
 }
</style>  