import Vue from 'vue'
import Router from 'vue-router'
import GroupGadget from './component/GroupGadget.vue'
import UserProfile from './component/UserProfile'
import Welcome from "./component/Welcome";
import UserDetails from "./component/UserDetails";
import GroupSetting from "./component/GroupSetting";
import CreateNewGroup from "./component/CreateNewGroup"
import Logout from "./component/Logout";

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
    },
    {
      path: '/groupsetting',
      component: GroupSetting
    },
    {
      path: '/creategroup',
      component: CreateNewGroup
    },
    {
       path: '/logout',
       beforeEnter(to,from,next){
         window.location = "/admin/logout"
       }
    }

  ]
})
