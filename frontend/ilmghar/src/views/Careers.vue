<template>
  <div class="flex justifyCenter m-t-2em section">
    <div class="m-t-2em m-b-2em " >
      <img class="heroImg" src="@/assets/CareersHero.png"  />
      
    </div>
  </div>
  <div class="section">
    <div>
      <h1 class="heading text-center">

        <span class="blue">
          Careers
        </span>
      </h1>
    </div>
    <div>
      <h1 class="heading ">

        <span class="blue">
          Why Join us
        </span>
      </h1>
    </div>
    <div class="sectionNoShadow ourMission">
      <h3 class="text-center blue">
        Embark on a Fulfilling Journey with Ilm Ghar

        At Ilm Ghar, we're not just shaping the future of education; we're creating opportunities for personal and
        professional growth. Joining our team means becoming part of a dynamic and passionate community that is committed
        to breaking down barriers and making a lasting impact on the educational landscape of Pakistan.
      </h3>
      <h3 class="blue">

        Here's why you should consider being a part of our journey:
      </h3>
      <ul class="sectionNoShadow">
        <li>
          <span class="blue">
            Meaningful Impact:
          </span>
          Be part of a mission-driven organization dedicated to making quality education accessible to all. Your work at
          Ilm Ghar will contribute to breaking down linguistic barriers and empowering students across Pakistan.
        </li>


        <li>
          <span class="blue">
            Innovation at the Core:
          </span>
          We foster a culture of innovation and creativity. Join a team that embraces forward-thinking ideas, values
          diversity of thought, and encourages continuous learning and improvement.
        </li>
        <li>






          <span class="blue">
            Collaborative Environment:
          </span>
          Ilm Ghar is a place where collaboration thrives. Work with a team of dedicated professionals who are passionate
          about education and believe in the power of collective effort to drive positive change.
        </li>

        <li>
          <span class="blue">
            Career Development:
          </span>
 We are invested in your success. Joining Ilm Ghar means access to continuous learning
      opportunities, skill development programs, and a supportive environment that encourages you to reach your full
      potential.

        </li>
        <li>
          <span class="blue">
            Inclusive Culture:
          </span>
           Ilm Ghar values diversity and inclusivity. We believe that diverse perspectives lead to better
      solutions. Join a workplace where your unique background and ideas are not only welcomed but celebrated.
        </li>
      </ul>
      <h3 class="text-center blue">
        "Ready to make a difference? Explore opportunities with Ilm Ghar and be part of a team that is redefining education for a brighter future. Your journey towards a rewarding career starts here.

      </h3>
    </div>
    <div>
      <h1 class="heading text-center">

        <span class="blue">
          Submit your application
        </span>
      </h1>
    </div>

    <div class=" formBox sectionNoShadow flex">
      <div>
        <img src="@/assets/careerForm.jpeg" alt="">
      </div>
      <div class="formDiv section">
        <form  @submit.prevent="submitFrm">
          <input  required v-model="firstName " type="text" placeholder="First Name">
          <input  required v-model="lastName" type="text" placeholder="Last Name">
          <input  required v-model="email" type="email" placeholder="Email Address">

          <br>
          <label for="desc"> A short summary of yourself </label>
          <br>
          <textarea required  v-model="description" name="desc" id="" cols="30" rows="10"></textarea>
          <button>Submit</button>
        </form>

      </div>
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
      firstName:'',
      lastName:'',
      email:'',

      description:'',

    };
  },
  methods: {
    async submitFrm() {
      try {
      const res = await axios.post('http://127.0.0.1:8000/api/instructor/new',  {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
        description: this.description,
      })
      
      this.firstName = ''
        this.lastName = ''
        this.email = ''
        this.description = ''
        window.alert("Your application has been submitted\n Thank you for applying")






      } catch (error) {
        console.error('Error submitting form:', error);

      }
      
      
    },
  },

};
</script>

<style scoped>
.formDiv{
width: 100%;
margin-left: 20px;
border: 2px solid black;


}
.formBox img{
height: 400px;
width: auto;
margin: 20px 0;
border-radius: 50px;

}
.formDiv input,.formDiv textarea,.formDiv label{
width: 90%;
margin:10px;
font-family: inherit;
font-size: 1.1em;

}
.formDiv button{

margin:10px;
font-family: inherit;
font-size: 1.1em;

}

</style>  