import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ExploreView from '@/views/ExploreView.vue'
import DashboardView from '@/views/DashboardView.vue'
import InstructorView from '@/views/InstructorView.vue'
import CourseView from '@/views/CourseView.vue'
import RegisteredView from '@/views/RegisteredView.vue'
import InstructorCourseView from '@/views/InstructorCourseView.vue'
import ForumView from '@/views/ForumView.vue'
import AboutUs from '@/views/AboutUs.vue'

import lectureVid from '@/views/lectureVidView.vue'
import Careers from '@/views/Careers.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    }, 
    {
      path: '/careers',
      name: 'careers',
      component: Careers
    },   
     
    {
      path: '/aboutus',
      name: 'About us',
      component: AboutUs
    },
    {
      path: '/explore',
      name: 'explore',
      component:ExploreView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()) {
          next()
        } else {
          next('/');
        }
      }
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: InstructorView,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()&& checkInstructor()) {
          next()
        } else {
          next('/');
        }
      }
    },
    {
      path: '/course/:id',
      name: 'Course',
      component: CourseView,
      props: true,
    },
    {
      path: '/registered/:id',
      name: 'RegisteredCourse',
      component: RegisteredView,
      props: true,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()) {
          next()
        } else {
          next('/course/:id');
        }
      }
    },
    {
      path: '/yourcourse/:id',
      name: 'InstructorCourseView',
      component: InstructorCourseView,
      props: true,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()) {
          next()
        } else {
          next('/course/:id');
        }
      }
    },
    {
      path: '/forum/:id',
      name: 'ForumView',
      component: ForumView,
      props: true,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()) {
          next()
        } else {
          next('/');
        }
      }
    },
    {
      path: '/lecture/:id',
      name: 'lectureVideo',
      component: lectureVid,
      props: true,
      beforeEnter: (to, from, next) => {
        if (checkLoginStatus()) {
          next()
        } else {
          next('/');
        }
      }
    },
    
  ]
})
function checkLoginStatus() {
  const authToken = localStorage.getItem('authToken');
  return authToken ? true : false;
}
function checkInstructor() {
  const INS = localStorage.getItem('INS');
  return INS ? true : false;
}

export default router
