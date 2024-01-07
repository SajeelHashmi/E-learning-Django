<template>
    <div>
      <div class="flex main ">
        <div class="sidebar sectionNoMargin">
          <form @change.prevent ="filter">
    
        <!-- Language Field -->
        <div>
          <h2 class="subheading blue">Languages:</h2>
          <div v-for="language in languages" >
            <input type="checkbox" v-model="selectedLanguages" :ref="`lang_${language.name}`"  :value="language.name" />
            <label>{{ capitalized(language.name) }}</label>
          </div>
        </div>

       

        <!-- Subject Field -->
        <div>
          <h2 class="subheading blue">Subjects:</h2>
          <div v-for="subject in subjects">
            <input type="checkbox" v-model="selectedSubjects" :ref="`subject_${subject.name}`" :value="subject.name" />
            <label>{{ subject.name }}</label>

          </div>
        </div>

        <!-- Tags Field -->
        <div>
          <h2 class="subheading blue">Tags:</h2>
          <div v-for="tag in tags" >
            <input type="checkbox" v-model="selectedTags" :ref="`tag_${tag.name}`"  :value="tag.name" />
            <label>{{ tag.name }}</label>

          </div>
        </div>

      </form>
        </div>
        <div class="sectionNoMargin mainContent">
        <div class=" m-b-2em">
          
          <div class="flex justifyCenter cardRow" v-for="(chunk, index) in courseChunks" :key="index">
            <CourseCard v-for="course in chunk" :course="course" :key="course.id"></CourseCard>
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
      allCourses:{},
      languages:'',
      subjects:'',
      tags:'',
      filteredCourses : [],
      selectedLanguages:[],
      selectedSubjects:[],
      selectedTags:[],

    };
  },
  computed: {
    courseChunks() {
      const chunkSize = 3;
      const chunks = [];
      for (let i = 0; i < this.filteredCourses.length; i += chunkSize) {
        chunks.push(this.filteredCourses.slice(i, i + chunkSize));
      }
      return chunks;
    },
  },
  mounted() {
    const q = this.$route.query.q || '';

    this.fetchData(q);
  },
  
  watch: {
    '$route.query.q': function(newQuery) {
            this.fetchData(newQuery || '');
    },
  },
  methods : {

    filter(){
  
      this.filteredCourses = this.allCourses.filter(this.filterCourses);
    },
    filterCourses(course) {

  const languageMatch = this.selectedLanguages.length === 0 || this.selectedLanguages.includes(course.language.name);
  const subjectMatch = this.selectedSubjects.length === 0 || this.selectedSubjects.includes(course.subject.name);
  let tagMatch = false
  console.log("selected tags",this.selectedTags)
  if(this.selectedTags.length === 0){
    tagMatch = true
  }
  else{
    for(let tags of course.tags){
      for (let index = 0; index < this.selectedTags.length; index++) {
        const element = this.selectedTags[index];
        if(tags.name == element){
          tagMatch = true
          break
        } 
      }
  
    }
  }
  return languageMatch && subjectMatch && tagMatch;
},
    async fetchData(query){

      try {
        const data = await axios.get(`http://127.0.0.1:8000/api/courses/languages`)
        this.languages = data.data
        console.log(this.languages)
      } catch (error) {
        console.log(error.response)
      }
      try {
        const data = await axios.get(`http://127.0.0.1:8000/api/courses/tags`)
        this.tags = data.data
        console.log(this.languages)
      } catch (error) {
        console.log(error.response)
      }
      try {
        const data = await axios.get(`http://127.0.0.1:8000/api/courses/subjects`)
        this.subjects = data.data
      } catch (error) {
        console.log(error.response)
      }
      try {
        let url = ''
        if (query){
            url = `http://127.0.0.1:8000/api/courses/allcourses?q=${query}`
        }
        else{
           url = `http://127.0.0.1:8000/api/courses/allcourses`
        }
          const courses = await axios.get(url)
        
        console.log(courses.data)
        this.allCourses = courses.data
        this.filteredCourses = courses.data
      } catch (error) {
        console.log(error)
      }

    },
    capitalized(str) {
      const capitalizedFirst = str[0].toUpperCase();
      const rest = str.slice(1);
      return capitalizedFirst + rest;
    },
  }
};
</script>

<style scoped>
.main{
  margin-top: 2em;
}
label{
  font-size: 1.5em;
  white-space: nowrap;
}
input[type='checkbox'] {
  padding: 10px;
  height: 20px;
  width: 20px;
 }
  .sidebar{
    flex: 15%;
    padding-bottom: 10px;
    padding-left: 10px;
  }
  .mainContent{
    margin-left: 15px;
    flex: 85%;
  }
  .cardRow{
    margin-top: 2em;
  }
 
</style>  