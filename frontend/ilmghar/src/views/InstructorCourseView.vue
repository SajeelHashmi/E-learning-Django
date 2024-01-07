
<!-- work on the play lecture button and create a view to play the lecture doing that will complete our student module 
then we will work on the instructor module creating the instructor views for registered courses and fixing the instructors dashboard 
after that we will start our work on the explore pae and its logic 
finally we will work on the forums and notifications app 
first we will work on the forums app 
and lastly the notifications app 
if i get all this working by thursday night i will start working on the flutter app for this
friday will br for the testAuth project and saturday sunday we shall finish this  
this instructor view is working as anticipated work on the forunms app now and then work on thenotification app and embed these 2
 -->


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
      <div class="flex justifyCenter align-center ">
        <div class="flex justifyCenter m-l-auto px-2em" >
          <button>

            Forum
          </button>

        </div>
      </div>
      <div class="flex justifyCenter">
        <h1 class="heading blue">
           Lectures
        </h1>
      </div>
      <div class="sectionNoShadow">
         <div v-for="lecture in course.lectures" class="p-b-2em">
          <h3 class="heading blue">
            {{ lecture.title }}
          </h3>
         
          <div class="flex align-center ">
            <h3 class="subheading blue">
              Description:
            </h3>

            <span class="m-l-halfem">
              {{ lecture.description }}
            </span>
            <button :data-id="lecture.id" @click="downloadNotes" class="m-l-auto">Notes
            </button>
            <button :data-id="lecture.id" @click="downloadNotes" class="m-l-halfem">Update Notes
            </button>
            <RouterLink :to="`/lecture/${course.id}?id=${lecture.id}`">

              <button  class="m-l-halfem"> Play 
              </button>
            </RouterLink>
          </div>
        
          <div class="flex align-center ">

          <h3 class="subheading blue">
            Assignment
          </h3>
          <span class="m-l-halfem">
              {{ lecture.assignment.title }}
            </span>
          </div>
        

          <div class="sectionNoShadow">
          <h3 class="subheading blue">
            Submissions
          </h3>
          <div class="flex align-center">
            <table>
                <thead >
                  <th class="blue" scope="col">Student</th>
                  <th class="blue" scope="col">Total Marks</th>
                  <th class="blue" scope="col">Assignment File</th>
                  <th class="blue" scope="col">Submission</th>
                  <th class="blue"  scope="col">Marks Obtained</th>
                  <th class="blue" scope="col">Remarks</th>
                  <th class="blue" scope="col">Checked</th>

                </thead>
                <tbody>

                    <tr v-for="student in lecture.assignment.students">
                    <td>{{ student.student.name }}</td>
                    <td>{{ lecture.assignment.marks }}</td>
                  
                    <td>
                        <button @click="downloadAssignment" :data-id="lecture.id">
                          download
                        </button>
                    </td>
                 
                    <td v-if="student.submission">
                        <button @click="downloadSubmission" :data-lecture="`${lecture.id}`" :data-student = "`${student.student.id}`">
                          download
                        </button>
                      </td>
                  
                    <td v-else>
                        <button  >
                          Not submitted
                        </button>                    
                     </td>
                 
                     

                       <td v-if="student.submission && student.submission.checked ">
                        {{ student.submission.marksObt }}
                      </td>
                  
                      <td v-else-if="student.submission">
                        <input type="number" v-model="student.submission.marks"  :ref="`${lecture.id}_${student.student.id}_marks`" placeholder="Not Checked Yet" min="0" max="10">
                      </td>
                   
                      <td v-else>
                        Assignment not submitted Yet 
                      </td>
                      <td v-if="student.submission && student.submission.checked ">
                        {{ student.submission.remarks }}
                      </td>
                    
                      <td v-else-if="student.submission">
                        <textarea v-model="student.submission.remarks" :ref="`${lecture.id}_${student.student.id}_remarks`"  cols="15" rows="5" >
                        </textarea>
                      </td>
                      <td v-else>
                        Assignment not submitted Yet 
                      </td>
                      <td v-if="student.submission && student.submission.checked ">
                          Checked
                      </td>
                      <td v-else-if="student.submission">
                          <button :data-lecture="`${lecture.id}`" :data-student = "`${student.student.id}`" @click="checkSubmission($event,student.submission)">
                            Mark as Checked
                          </button>
                      </td>
                      <td v-else>
                        Assignment not submitted Yet 
                      </td>
              
                   

                  </tr>  
                </tbody>
                
              </table>
            
           
          </div>
          <div class="sectionNoShadow">
           
            
          </div>
          
        </div>
          
        </div> 

      </div>

    </div>
  </template>
  
<script>
import axios from "axios";
import router from "../router";

export default {
  components: {
  },
  data() {
    return {
      course:{},
      authToken:"",
      INS:"",
      submitLink :'',
    };
  },
  async mounted(){
    await this.fetchData(this.$route.params.id)
    console.log(this.course)
  },
  created(){
    this.authToken = localStorage.getItem('authToken');
    this.INS = localStorage.getItem('INS');
  },
  methods :{
    async downloadAssignment(event){
      const button  = event.target
      const lectureId = button.dataset.id
      const url = `http://127.0.0.1:8000/api/student/downloadassignment/${this.course.id}?id=${lectureId}`;
      try {
       const response = await axios.get(url, {
          headers: {
            Authorization: `Token ${this.authToken}`,
          },
        })
          
        const link = document.createElement('a');

    
        const blob = new Blob([response.data]);

        link.href = window.URL.createObjectURL(blob);

        console.log(response.headers)
        document.body.appendChild(link);
        const contentDispositionHeader = response.headers['content-disposition'];
        const fileNameMatch = contentDispositionHeader.match(/filename="(.+)"/);

        if (fileNameMatch && fileNameMatch[1]) {
          link.download = fileNameMatch[1];
        } else {
          console.error('Unable to extract filename from content-disposition header');
        }
        link.click();
        document.body.removeChild(link);

      } catch (e) {
        console.error('Error downloading file:', e);

      }


          
            
    },
    async downloadSubmission(event){
      const button  = event.target
      const lectureId = button.dataset.lecture
      const studentId = button.dataset.student

      const url = `http://127.0.0.1:8000/api/instructor/downloadsubmission/${lectureId}?id=${studentId}&&ins=${this.INS}`;
      try {
       const response = await axios.get(url, {
          headers: {
            Authorization: `Token ${this.authToken}`,
          },
        })
          
        const link = document.createElement('a');

    
        const blob = new Blob([response.data]);

        link.href = window.URL.createObjectURL(blob);

        console.log(response.headers)
        document.body.appendChild(link);
        const contentDispositionHeader = response.headers['content-disposition'];
        const fileNameMatch = contentDispositionHeader.match(/filename="(.+)"/);

        if (fileNameMatch && fileNameMatch[1]) {
          link.download = fileNameMatch[1];
        } else {
          console.error('Unable to extract filename from content-disposition header');
        }
        link.click();
        document.body.removeChild(link);

      } catch (e) {
        console.error('Error downloading file:', e);

      }      
    },
    async checkSubmission(event,submission){
      const button  = event.target
      const lectureId = button.dataset.lecture
      const studentId = button.dataset.student
      const remarks = this.$refs[`${lectureId}_${studentId}_remarks`][0];
      const marksInput = this.$refs[`${lectureId}_${studentId}_marks`][0];     
      
      if(!(marksInput.value>0&&marksInput.value<11)){
        console.log("invalid input")
        submission.marks = null
      } 


   
      const url = `http://127.0.0.1:8000/api/instructor/checksubmission/${lectureId}?id=${studentId}&&ins=${this.INS}`;
      try {
       const response = await axios.post(url,
       {
        marks:marksInput.value,
        remarks:remarks.value
       },
       {
          headers: {
            Authorization: `Token ${this.authToken}`,
          },
        })
      submission.checked = true
        
      } catch (e) {
        console.error('Error checking submission:', e.response);

      }      
    },


    async fetchData(id){
      if (this.authToken) {
        try{
          console.log(this.INS)
          const data = await axios.get(`http://127.0.0.1:8000/api/instructor/getcoursedata?id=${id}&&ins=${this.INS}`,{
            headers:{
              Authorization:`Token ${this.authToken}`
            }
          })
          console.log(data)
          this.course = data.data
      }
      catch(e){
        console.log(e)
        // router.push(`/course/${id}`)
      }
      } else {
        router.push(`/course/${id}`)

      }
        
    },
  

},
};
</script>

<style scoped>
   textarea{
    width: 80%;
    font-family: inherit;
    background-color: #e7e7e7;
    padding: 5px;
  }
  .test{
    background-color: black;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 1.1em;
    text-align: center;

  }

  /* Table header styles */
  table th {
    background-color: #ffffff;
    font-size: 1.25em;
    padding: 10px;
    border: 1px solid #bfbfbf;
  }

  /* Table cell styles */
  table td {
    padding: 10px;
    border: 1px solid #bfbfbf;
  }
  img{
    
  width: auto;
  height: 400px;
  }
  .banner{
    width: 100%;
    height: 400px;
  }
  span{
    font-size: 1.5em;
  }
  button{
    font-size: 1em;
  }
  .text{
    color: black;
    font-weight: 100;
    font-size: 1.5rem;
  }
 

</style>  