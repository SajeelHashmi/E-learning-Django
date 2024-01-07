<template>
  <div class="card">
    <div class="cardPrimary">
      <div class="">
        <img class=" " :src="course.coverPicBlob"  alt="">
      </div>
      <div class="text-center">
        <h2>              
          <RouterLink  v-if="INS" :to="`/yourcourse/${course.id}`">
            {{ course.title }}
          </RouterLink>
              <RouterLink v-else :to="`/course/${course.id}`"  target="_blank">

              {{ course.title }}
            </RouterLink>

            </h2>

          </div>
          <div class="text-center">
            <h3>

              {{ course.subject.name }}
            </h3>
          </div>
      </div>
        <div class="cardSecondary">
          <div class="box pt-3">
            <div class="">
            <h2>

              Instructor: <span>{{ course.instructorName }}</span>
              </h2>
          </div>
          </div>
          <div class="box pt-3">
            <div class="">
            <h2>

              Language: <span>  {{ capitalized(course.language.name) }}</span>
              </h2>
          </div>
          </div>
      
          <div class="box pt-3">
            <div class="desc">
            <h2>

              Description: <span>{{ course.description }} 
              </span>
              </h2>
          </div>
          </div>

          <div class=" box pt-3">
            <div class="flex ">
              <button v-for="tag in course.tags" >{{tag.name}}</button>
            </div>
          </div>


        </div>
      </div>
</template>
  
  <script>
  import { RouterLink } from 'vue-router'

  export default {
    props: {
      course:{
        type: Object,
        required: true,
      }
    },
    data() {
      return {

        INS:false,
      };
    },
    methods: {
      capitalized(str) {
      const capitalizedFirst = str[0].toUpperCase();
      const rest = str.slice(1);
      return capitalizedFirst + rest;
    },

    },
    created() {
      
    this.INS = localStorage.getItem('INS');
  
    },
    
    beforeDestroy() {
    },
  };
  </script>
  
  <style scoped>

  img{
    margin-right: auto;
    margin-left: auto;
   width: 100%; 
   min-height: 120px;
  
  }
  span{
    color: black;
    font-size: large;
  }
 h2{
  padding-right: 10px;
  padding-left: 10px;
 }
  .card{
    display: flex;
    width: 20%;
    transition: all ease-in-out 1s;
    background-color: white;
    border: 1px black solid;
    margin: 0 1em;
    height: 350px;
    box-shadow: 5px 5px 5px   #484747;
    overflow: hidden;

  }
  .box{
    padding-left: 1rem;
  }
  button{
    margin-left: .5rem;
    margin-right: .5rem;
  }
  .card:hover{
    width: 50%;
  }
  .card:hover > div{
    max-width: 100%;
    width: 100%;
    display: block;
    opacity: 100;
    /* max-w-full w-full block opacity-100 */
  }
  .cardPrimary{

    /* bg-primary
     */
     width: 100%;
     transition: all ease-in-out 1s;
     overflow:hidden;
     /* w-[100%] transition-all ease-in-out duration-1000 overflow-y-scroll */
   }
  .cardSecondary{
    width: 0%;
    transition: all ease-in-out 1s;
    opacity: 0;
    overflow-y: scroll;
    
    /* bg-primary w-0 transition-all text-white  ease-in-out duration-1000 opacity-0 overflow-y-scroll */
  }
  </style>
  