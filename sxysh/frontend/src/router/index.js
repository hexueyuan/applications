import Vue from 'vue'
import Router from 'vue-router'
import DataPage from '@/components/data'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'DataPage',
      component: DataPage
    }
  ]
})
