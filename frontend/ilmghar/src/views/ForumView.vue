
<!-- 
  post replies are comming all is perfect all your backend views are in order 
  make a box for posts and their replies that looks a little better than now 
  the trigger button is ready and all that is left now is to add toggle functionality and reply showing functionality to it
  notification module wont take a lot of our time it is as good as done we can work on the mobile version to
  we have to finish this embed notifications and then fix the explore view make some extra pages fix footer etc then 
  we can work on the mobile app
 -->
<template>
  


    <div class="section">
      <div>
        <img class="banner" :src="course.coverPicBlob" alt="">
      </div>
      <div class="flex justifyCenter">
     
        <h1 class="heading blue">
          <RouterLink :to="`/course/${course.id}`">

            {{ course.title }}
          </RouterLink>
        </h1>
      </div>
      <div class="sectionNoShadow p-b-2em">
        <div class="newPost">
          <div class=" postCardUser blue">
          
            New Post
        </div>
          
            <form @submit.prevent="newPost">
              <textarea ref="newPost"  name="content" id=""  rows="5"></textarea>
              <div class="flex">
                <button class="m-l-auto ">
                  Post
                </button>
              </div>
            </form>
          </div>
        <div class="m-b-2em" v-for="post in posts">
          <div class="postCard ">
            
            <div class="flex align-center">
              <div class="postCardUser blue">
                  {{ post.user }}
              </div>
       
            </div>
            <div class="flex align-center">
            <div class="px-2em postCardContent">
              <p class="text">
                {{ post.content }}
              </p>
            </div>
              <button class="dropdown-trigger m-l-auto" :data-id="post.id" :ref="`triggerBtn_${post.id}`" @click="fetchReplies(post)"> <span>{{ post.repliesNum }}</span> <i><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                  <path d="M5 3l3.057-3 11.943 12-11.943 12-3.057-3 9-9z" /></svg></i> 
              </button>
             
          </div>
        </div>
        <transition name="reply">
        <div class="replies" v-if="post.show">
          <div class="giveReply">
            <form @submit.prevent="giveReply(post)">
                <!-- add post id with this add event handler for form submit attach a model with the text area -->
              <textarea :ref="`replyContent_${post.id}`" name="content" id=""  rows="5"></textarea>
              <div class="flex">
                <button class="m-l-auto ">
                  Reply
                </button>
              </div>
            </form>
          </div>

          <div  v-for="post in post.replies">

          
          <div class="postCard ">
            
            <div class="flex align-center">
              <div class="postCardUser blue">
                  {{ post.user }}
              </div>
       
            </div>
            <div class="flex align-center">
            <div class="px-2em postCardContent">
              <p class="text">
                {{ post.content }}
              </p>
            </div>
            
             
          </div>
        </div>
      </div>
        </div>
      </transition>
        </div>


      </div>
    </div>
  </template>
  
<script>
import axios from "axios";
import { ref } from "vue";

export default {
  components: {
  },
  data() {
    return {
      course:{},
      authToken:"",
      INS:"",
      posts:{},
      startNum:0,

    };
  },
 async mounted(){
   await this.fetchData(this.$route.params.id)
  },
  created(){
    this.authToken = localStorage.getItem('authToken');
  },
  methods :{
    async giveReply(post){
      console.log(post.id)
      const textArea = this.$refs[`replyContent_${post.id}`][0];  
      const content = textArea.value
      if(!content){
        return
      }
      try {
        const data = await axios.post(`http://127.0.0.1:8000/api/forum/createpost/${this.course.id}/${post.id}`,
        {
          content:content
        } ,
        {
              headers: {
                Authorization: `Token ${this.authToken}`,
              },
        }
        )
        textArea.value = ''
        post.replies.unshift(data.data)
        post.repliesNum++
      } catch (error) {
        console.log(error)
      }

   },
   async newPost(){
      const content = this.$refs.newPost.value; 
      if(!content){
        return
      }
      try {
        const data = await axios.post(`http://127.0.0.1:8000/api/forum/createpost/${this.course.id}/0`,
        {
          content:content
        } ,
        {
              headers: {
                Authorization: `Token ${this.authToken}`,
              },
        }
        )
        this.$refs.newPost.value=""
        this.posts.unshift(data.data)
      } catch (error) {
        console.log(error)
      }

   },

      async fetchData(id){
        try{
            const data = await axios.get(`http://127.0.0.1:8000/api/courses/${id}`)
            this.course = data.data

        }
        catch(e){
          if(e.response.status === 404){
            //show 404
            console.log("show 404 page")
          }
        }
        try{
            const data = await axios.get(`http://127.0.0.1:8000/api/forum/getposts/${id}`,
            {
              headers: {
                Authorization: `Token ${this.authToken}`,
              },
            })
            this.posts = data.data
            console.log(data.data)
        }
        catch(e){
          if(e.response.status === 404){
            //show 404
            console.log("show 404 page")
          }
        }
    },
  async fetchReplies(post){
    const button = this.$refs[`triggerBtn_${post.id}`][0];  
    button.classList.toggle('dropdown-active')
    const postId = button.dataset.id
    if (post.show){
      post.show = false
    }
    else{
      try {
        const data =  await axios.get(`http://127.0.0.1:8000/api/forum/getreplies/${this.course.id}/${postId}`,
              {
                headers: {
                  Authorization: `Token ${this.authToken}`,
                },
              })
        post.replies = data.data
        post.show = true
        console.log(post)            
      } catch (error) {
        console.log(error)
      }
      
    }
  }

},
};
</script>

<style scoped>
  .test{
    background-color: black;
  }
  .giveReply{
    border-right: black solid 1px;
    border-left: black solid 1px;
    padding: 10px;
  }
  .newPost{
    border-top: black solid 1px;
    border-right: black solid 1px;
    border-left: black solid 1px;
    padding-bottom: 10px;
  }
  textarea
{
  width:98%;
  font-family: inherit;
  font-size: 1.5em;
  margin-bottom: 15px;
}


.reply-enter-active, .reply-leave-active {
  transition: max-height 0.5s ease-in-out, opacity 0.5s ease-in-out;
}
.replies{
  padding-left: 10px;
  max-height: 400px;
  overflow-y: scroll;
  }
.reply-enter-to, .reply-leave-from {
  max-height: 400px; 
}

.reply-enter-from, .reply-leave-to {
  max-height: 0;
  opacity: 0;
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
  .postCardUser{
padding: 20px;
text-decoration: underline 3px;
font-size: 3em;
  }

 
  button{
    font-size: 1.5rem;
    margin-right: 1rem;
    padding: 1%;
  }

.postCard{
  border: solid black 1px;
}

.postCardContent{
  
    color: black;
    font-weight: 100;
    font-size: .75em;
}

.dropdown-trigger > i > svg {
  width: 0.7rem;
  height: 0.7rem;
  transform: rotate(90deg);
  transition: all 0.3s ease;
  fill: yellow;
}

.dropdown-active.dropdown-trigger > i > svg {
  width: 0.7rem;
  height: 0.7rem;
  transform: rotate(-90deg);
}
span{
  font-size: 1em;
}

</style>  