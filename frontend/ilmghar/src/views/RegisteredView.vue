
<!-- work on the play lecture button and create a view to play the lecture doing that will complete our student module 
then we will work on the instructor module creating the instructor views for registered courses and fixing the instructors dashboard 
after that we will start our work on the explore pae and its logic 
finally we will work on the forums and notifications app 
first we will work on the forums app 
and lastly the notifications app 
if i get all this working by thursday night i will start working on the flutter app for this
friday will br for the testAuth project and saturday sunday we shall finish this   -->


<template>
  


    <div class="section">
      <div>
        <img class="banner" :src="course.coverPicBlob" alt="">
      </div>
      <div class="flex justifyCenter align-center ">
        <div class="">

          <h1 class="heading blue">
            {{ course.title }}
            
          </h1>
        </div>
     

      </div>
      <div class="flex justifyCenter align-center ">
        <div class="flex justifyCenter m-l-auto px-2em" >
          <RouterLink :to="`/forum/${course.id}`">

            <button class="btn">
              
              Forum
            </button>
          </RouterLink>

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
          <div class="sectionNoShadow">

          
          <div class="flex align-center">

            <h3 class="subheading blue">
              Description:
            </h3>
            <span class="m-l-halfem">
              {{ lecture.description }}
            </span>
            <button  :data-id="lecture.id" @click="downloadNotes" class="btn m-l-auto"> Notes
            </button>
            <RouterLink :to="`/lecture/${course.id}?id=${lecture.id}`">

              <button  class="btn m-l-halfem"> Play 
              </button>
            </RouterLink>
          </div>
          <h3 class="subheading blue">
            Assignment
          </h3>
          <div class="flex align-center">
            <table>
                <thead >
                  <th class="blue" scope="col">Title</th>
                  <th class="blue" scope="col">Total Marks</th>
                  <th class="blue" scope="col">Assignment File</th>
                  <th class="blue" scope="col">Submission</th>
                  <th class="blue"  scope="col">Marks Obtained</th>
                  <th class="blue" scope="col">Remarks</th>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ lecture.assignment.title }}</td>
                    <td>{{ lecture.assignment.marks }}</td>
                  
                    <td>
                        <button @click="downloadAssignment" :data-id="lecture.id">
                          download
                        </button>
                    </td>
                    <td v-if="lecture.assignment.submission">
                        <button @click="downloadSubmission" :data-id="lecture.id">

                          download
                        </button>
                      </td>
                    <td v-else>
                        <button  :data-id="lecture.assignment.id" @click="openSubmitDialog">
                          Submit
                        </button>                    
                     </td>
                    <td v-if="lecture.assignment.submission && lecture.assignment.submission.checked ">
                    {{ lecture.assignment.submission.marksObt }}
                    </td>
                    <td v-else-if="lecture.assignment.submission">
                      Assignment not checked yet
                    </td>
                    <td v-else>
                      Assignment not submitted Yet 
                    </td>
                    <td v-if="lecture.assignment.submission && lecture.assignment.submission.checked ">
                    {{ lecture.assignment.submission.remarks }}
                    </td>
                    <td v-else-if="lecture.assignment.submission">
                      Assignment not checked yet
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
        <dialog ref="submitDialog" class="px-2em">
          <h2 class="blue">Submit Assignment</h2>
          Only .pdf, .docx files are accepted

          <form @submit.prevent="submitAssignment">
            <div class="m-b-2em">
              <input type="file" required accept=".pdf, .docx" ref="fileInput">
            </div>
            <div class ="flex space-around">

            <button >Submit</button>
              <button type="button" @click="closeSubmit">Close</button>
            </div>

            </form>
        </dialog>
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
      assignmentId :0
    };
  },
 async mounted(){
   await this.fetchData(this.$route.params.id)
  },
  created(){
    this.authToken = localStorage.getItem('authToken');
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
      const lectureId = button.dataset.id
      const url = `http://127.0.0.1:8000/api/student/downloadsubmission/${this.course.id}?id=${lectureId}`;
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
    async downloadNotes(event){
      const button  = event.target
      const lectureId = button.dataset.id
      const url = `http://127.0.0.1:8000/api/student/downloadnotes/${this.course.id}?id=${lectureId}`;
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
    async submitAssignment() {
      // Get the file input element
      const fileInput = this.$refs.fileInput;
      
      // Check if a file is selected
      if (fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
      }

      // Create FormData object
      const formData = new FormData();
      formData.append('submission', fileInput.files[0]);
      console.log(formData)

      try {
      
    const data = await axios.post(`http://127.0.0.1:8000/api/student/submit/${this.assignmentId}`,
              formData,
            {
              headers:{
                Authorization:`Token ${this.authToken}`,
                'Content-Type': 'multipart/form-data',
              }
            })
            await this.fetchData(this.$route.params.id)
            this.closeSubmit();
      } catch (error) {
        // Handle errors
        // console.error('Error submitting assignment:', error);
        alert('An error occurred while submitting the assignment.');
      }
    },
        openSubmitDialog(event){
          const button  = event.target
          this.assignmentId = button.dataset.id
          const dialog = this.$refs.submitDialog
          console.log(dialog)
          dialog.showModal()
        },
        closeSubmit(event){
          const dialog = this.$refs.submitDialog
          dialog.close()
        },
      async fetchData(id){
        if (this.authToken) {
          try{
            const data = await axios.get(`http://127.0.0.1:8000/api/student/getregisteredcourse?id=${id}`,{
              headers:{
                Authorization:`Token ${this.authToken}`
              }
            })
            this.course = data.data
            console.log(this.course)
        }
        catch(e){
          console.log(e)
          router.push(`/course/${id}`)
        }
        } else {
          router.push(`/course/${id}`)

        }
        
    },
  

},
};
</script>

<style scoped>

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
  .btn{
    font-size: 1.5em;
  }
 

</style>  