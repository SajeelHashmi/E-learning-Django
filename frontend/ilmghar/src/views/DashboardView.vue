<template>
    <div>


      <div class="section">

        <div  class="flex-col align-center">
          <h1 class="heading">
            <span class="yellow">
               Welcome 

            </span>
            <span class="blue">
              {{student.name}}
            </span>
          </h1>
          <p class="tagLine blue">
            Lets Start Learning
          </p>
        </div>
        <div v-if="registeredCourses.length!=0">  
        <div  >
        
          <h1 class="heading">
            
            <span class="blue">
              Your courses
            </span>
              
          </h1>
        </div>
        <div class="sectionNoShadow">

          <div v-for="course in registeredCourses" class="flex  m-b-2em align-center space-around" >
            
            <CourseCard  :course = "course" ></CourseCard>
            
              <div  class="progress">
                
                <div  class="bar">
                </div>
              </div>

            
          </div>
        </div>
      </div>
      <div v-else>
        <div   class="flex-col align-center justifyCenter m-t-2em ">
          <div class="subheading">
            <p class="blue">
              You have no registed courses as of now
            </p>
            <div class="sectionNoShadow">

              <span class="blue">
                Register Courses and join the Fun
              </span>
            </div>
            
          </div>
          <RouterLink to="/explore">

            <button class="btn "> Explore</button>
          </RouterLink>
        </div>
      </div>
        <div >
          <h1 class="heading">
            
            <span class="blue">
              Suggested for you
            </span>
              
          </h1>
        </div>

        <div class="flex  p-b-2em justifyCenter align-center">
          <CourseCard v-for="course in suggestedCourses" :key="course.id" :course="course"></CourseCard>

          <div>
            <RouterLink to = "/explore">

              <img src="@/assets/arrow.png" alt="" srcset="">
            </RouterLink>
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
      registeredCourses:{},
      suggestedCourses:{},
      student:{},
      authToken:""
    };
  },
 async mounted(){

   await this.fetchCourses()
   const progressBar = document.querySelectorAll('.progress');
   setTimeout(() => {
     for(let bar of progressBar){
         bar.style.setProperty('--progress', '50%');
       }
     }, 0);
    this.fetchStudentInfo()
  },
  created(){
    this.authToken = localStorage.getItem('authToken');

  },
  methods:{
    async fetchCourses(){
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/student/registeredcourses`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.registeredCourses = data.data
          console.log(this.registeredCourses)
          

        }
        catch(e){
          console.log(e.response)
        }
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/student/suggested`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.suggestedCourses = data.data
          console.log(this.registeredCourses)


          }
          catch(e){
          console.log(e.response)
          }
    },
  
  async fetchStudentInfo(){
        try{

          const data = await axios.get(`http://127.0.0.1:8000/api/student/`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }

          })
          this.student = data.data
          console.log(this.student)
        }
        catch(e){
          console.log(e.response)
        }
  },
  }
};
</script>

<style scoped>
  .test{
    background-color: black;
  }
  @property --progress {
  syntax: "<length>";
  initial-value: 0%;
  inherits: true;
}

.progress {
  --progress: 0%;
  width: 500px;
  height: 50px;
  border: 1px solid #0000000f ;
  padding: 12px 10px;
  box-shadow: 2px 2px 10px #000000ff;
}

.progress .bar {
  width: var(--progress);
  height: 100%;
  background: #105BAD;
  background-repeat: repeat;
  transition: width 3s ease 3s;
}



  .courseBoxLang{
    margin-left: 5%;
  }
 
 
  .tagLine{
    font-size: 2em;
    margin: 0;
  }
  .btn{
    font-size: 1.5em;
  }
</style>  