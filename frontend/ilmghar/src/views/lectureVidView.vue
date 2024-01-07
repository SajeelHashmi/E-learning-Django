
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
      <div class="flex justifyCenter">
        <h1 class="heading blue">
           {{ lecture.title }}
        </h1>
      </div>
      <div class="sectionNoShadow ">
        <h1 class="subheading blue">
          Lecture number {{ lecture.number }}
        </h1>
      </div>
      <div>
        
        <video ref="video" width="100%" height="640" controls></video>

      </div>
     <div class="sectionNoShadow">

       <div class="flex align-center">
         
         <h3 class="subheading blue">
           Description:
          </h3>
          <span class="m-l-halfem">
            {{ lecture.description }}
          </span>
          <button :data-id="lecture.id" @click="downloadNotes" class="m-l-auto"> Notes
          </button>
          
          
        </div>
      </div>


    </div>
  </template>
  
<script>
import axios from "axios";
import router from "../router";
import Hls from 'hls.js';
export default {
  components: {
  },
  data() {
    return {
      authToken:"",
      INS:"",
      lecture:"",
      courseId:"",
    
    };
  },
 async mounted(){
  const lectureId = this.$route.query.id;
  // the fetch data view can be modified to fetch only the data like lecture name number etc related assignments and notes
  // all the other functionality in now being handle via the hls package
  this.courseId =this.$route.params.id 
   this.fetchData(this.courseId,lectureId)
   let hls = new Hls({
      xhrSetup: xhr => {
        xhr.setRequestHeader('Authorization', `Token ${this.authToken}`)
      }
    })
    let video = this.$refs["video"];
    // const res = await axios.get(`http://127.0.0.1:8000/api/student/lecture/${this.$route.params.id}/output.m3u8?id=${idQueryParam}`)
    // console.log('res')
    // console.log(res.data)

    hls.loadSource(`http://127.0.0.1:8000/api/student/lecture/${this.courseId}/${lectureId}/output.m3u8`);
    console.log(hls)
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function () {
      video.play();
    });
  },
  beforeDestroy() {

  },
  created(){
    this.authToken = localStorage.getItem('authToken');
  },
  methods :{
    async downloadNotes(event){
      const button  = event.target
      const lectureId = button.dataset.id
      const url = `http://127.0.0.1:8000/api/student/downloadnotes/${this.courseId}?id=${lectureId}`;
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
 
  
      async fetchData(courseId,lectureId){
        if (this.authToken) {
          try{
            const data = await axios.get(`http://127.0.0.1:8000/api/student/lecture/${courseId}/${lectureId}`,{
              headers:{
                Authorization:`Token ${this.authToken}`
              }
            })
            console.log(data.data)
            this.lecture = data.data
         
        }
        catch(e){
          console.log("s")
          console.log(e)
          // router.push(`/`)
        }
        } else {
          console.log("data fetch failed")
          // router.push(`/`)

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
 

</style>  