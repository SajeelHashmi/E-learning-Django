<!-- create a instructor course view 
the top will be the same course image we are not updating images right now 
display the course name description as before 
then show how many students are enrolled the assignments they have submitted and the ones checked sort by unchecked
this will be a drop down div 
add drop down functionality all across the website i think this is all for the instructor as of now   -->

<template>
    <div>


      <div class="section">

        <div class="flex m-b-2em space-around">
          <div class="basis-1">
            <h1 class="heading blue">
                Welcome: {{instructor.name}}
            </h1>
            <div>
              <h1 class="subheading blue">
               Your Bio
            </h1>
            <form @submit.prevent="updateInstructorBio">

              <textarea  v-model="bio" class="m-b-2em" name="" id="" cols="30" rows="10">{{ instructor.bio }}
              </textarea>
              <button>Update</button>
            </form>
            </div>
          </div>
          <div class="basis-1">
            <img class="instructorImg" :src="instructor.pfpBlob" alt="">
          </div>
        </div>
        <div >
          <h1 class="heading">
            
            <span class="blue">
              Your courses
            </span>
              
          </h1>
        </div>
        <div class="sectionNoShadow">

          <div v-for="course in courses" class=" flex p-b-2em justifyCenter align-center">
            <CourseCard  :key="course.id" :course="course"></CourseCard>

        </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
import CourseCard from '@/components/CourseCard.vue';
import axios from "axios";

export default {
  components: {
    CourseCard
  },
  data() {
    return {
      courses:{},
      instructor:{},
      authToken:"",
      INS:"",
      bio : ''
    };
  },
  mounted(){
    this.fetchCourses()
    this.fetchInstructorInfo()
  },
  created(){
    this.authToken = localStorage.getItem('authToken');
    this.INS = localStorage.getItem('INS');
  },
  methods :{
      async fetchCourses(){
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/instructor/instructorcourses?ins=${this.INS}`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.courses = data.data
        }
        catch(e){
          console.log(e.response)
        }
    },
  updateInstructorBio(){
    axios.post(`http://127.0.0.1:8000/api/instructor/updatebio?ins=${this.INS}`,
              {
                bio:this.bio
              },
            {
              headers:{
                Authorization:`Token ${this.authToken}`,
                'Content-Type': 'multipart/form-data',
              }
            }).then(res =>{
              console.log(res)
            }).catch(res =>{
              console.error(res)
            })
          },
  async fetchInstructorInfo(){
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/instructor/?ins=${this.INS}`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.instructor = data.data
          this.bio = this.instructor.bio
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
  textarea{
    width: 100%;
    font-family: inherit;
    background-color: #e7e7e7;
    padding: 20px;
    font-size: 1.5em;
  }
  img{
    
  width: 500px;
  height: auto;
  }
  .heading{
    margin-top: 0;
  }

</style>  