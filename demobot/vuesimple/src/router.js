import Vue from 'vue'
import Router from 'vue-router'
import GroupGadget from './component/GroupGadget.vue'
import UserProfile from './component/UserProfile'
import Welcome from "./component/Welcome";
import UserDetails from "./component/UserDetails";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Welcome
    },
    {
      path: '/groups',
      component: GroupGadget
    },
    {
      path: '/users',
      component: UserProfile
    },
    {
      path: '/userdetails',
      component: UserDetails
    }
  ]
})
