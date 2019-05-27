import Vue from 'vue'
import Router from 'vue-router'
import firstPage from '@/components/firstPage'
import secondPage from '@/components/secondPage'
import thirdPage from '@/components/thirdPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'firstPage',
      component: firstPage
    },
    {
      path: '/second',
      name: 'secondPage',
      component: secondPage
    },
    {
      path: '/third',
      name: 'thirdPage',
      component: thirdPage
    }
  ]
})
