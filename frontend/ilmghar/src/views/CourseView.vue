<template>
  <div class="section">
      <div>
        <img class="banner" :src="course.coverPicBlob" alt="">
      </div>
      <div class="flex justifyCenter">
        <h1 class="heading blue">
           {{ course.title }}
        </h1>
      </div>
      <div class="sectionNoShadow">
          <h1 class="subheading blue">
            Description:
            <span class="text">
                {{ course.description }}
              </span>
          </h1>
          <button v-for="tag in course.tags">{{ tag.name }}</button>
          <div class="m-t-2em flex">

            <button @click="registerCourse" class="m-l-auto">
              Register
            </button>
          </div>
      </div>
      <div class="flex justifyCenter">
        <h1 class="heading blue">About the Instructor</h1>
      </div>
      <div class="sectionNoShadow  space-around flex" style=" height: 500px;" v-if="course && course.instructor">
        <div>

          <h1 class="basis-1 subheading blue">Name: <span class="text">{{ course.instructor.name }}</span></h1>
          <h1 class="basis-1 subheading blue">Bio: <span class="text">{{ course.instructor.bio }}</span></h1>
     

        </div>
        <div >
          <img :src="course.instructor.pfpBlob" class="basis-1" alt="">
        </div>
      </div>
      <div v-else class="sectionNoShadow">
        <p>Loading...</p>
      </div>

    </div>
  </template>
  
<script>
import axios from "axios";

export default {
  components: {
  },
  data() {
    return {
      course:{},
      authToken:"",
      INS:"",
    };
  },
 async mounted(){
   await this.fetchData(this.$route.params.id)
  },
  created(){
    this.authToken = localStorage.getItem('authToken');
  },
  methods :{
      async registerCourse(){
        try{
          if(this.authToken){
            const data = await axios.post(`http://127.0.0.1:8000/api/student/registernewcourse/${this.course.id}`,
              {},
              {
                headers:{
                Authorization:`Token ${this.authToken}`
                }
               },)
              console.log("reroute to registered page")
              this.$router.push(`/registered/${this.course.id}`)
            }
             
            else{
            window.alert("please login to register a course")

          }
          }
        catch(e){
          console.log(e)
        }
      },
      async fetchData(id){
        try{
          if(this.authToken){
            const data = await axios.get(`http://127.0.0.1:8000/api/courses/registered/${id}`,{
              headers:{
                Authorization:`Token ${this.authToken}`
              }     
            })
            if(data.data.registered){
              console.log("reroute to registered page")
              this.$router.push(`/registered/${id}`)
            }
            else{
              const data = await axios.get(`http://127.0.0.1:8000/api/courses/${id}`)

              this.course = data.data
              console.log(data.data)
            }
          }

          else{
            const data = await axios.get(`http://127.0.0.1:8000/api/courses/${id}`)

            console.log("no authToken",data.data)
            this.course = data.data


          }
        }
        catch(e){
          if(e.response.status === 404){
            //show 404
            console.log("show 404 page")
          }
        }
    },
  
  async fetchInstructorInfo(){
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/instructor/?ins=${this.INS}`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.instructor = data.data
          console.log(this.instructor)
        }
        catch(e){
          console.log(e.response)
        }
  },
},
};
</script>

<style scoped>
  .test{
    background-color: black;
  }
  img{
    
  width: auto;
  height: 400px;
  }
  .banner{
    width: 100%;
    height: 400px;
  }
  p{
    font-size: 2em;
  }
  .text{
    color: black;
    font-weight: 100;
    font-size: 1.5rem;
  }
  button{
    font-size: 2rem;
    margin-right: 1rem;
  }

</style>  