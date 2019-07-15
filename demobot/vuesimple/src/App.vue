<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-4">
        <sidebar-menu :menu="menu"/>
      </div>


      <div class="col-8">

        <group-gadget></group-gadget>
      </div>
    </div>
    <div class="row">
       <div class="col-4">
       </div>
      <div class="col-8">
        <UserProfile></UserProfile>
      </div>
    </div>
  </div>
</template>

<script>
  import GroupList from './component/GroupList.vue';
  import GroupStat from "./component/GroupStat";
  import GroupGadget from "./component/GroupGadget";
  import UserProfile from "./component/UserProfile"

  export default {

    data() {
      return {
        menu: [
          {
            header: true,
            title: 'Admin Panel - Stop Smoking',
            // component: componentName
            // visibleOnCollapse: true
            // class: ''
            // attributes: {}
          },
          {
            href: '/',
            title: 'Dashboard',
            icon: 'fa fa-user',
            /*
            // custom icon
            icon: {
                element: 'span',
                class: 'fa fa-user',
                attributes: {}
                text: ''
            }
            */
            // disabled: true
            // class: ''
            // attributes: {}
            // alias: '/path'
            /*
            badge: {
                text: 'new',
                class: 'default-badge'
                // attributes: {}
                // element: 'span'
            }
            */
          },
          {
            title: 'Group Management',
            icon: 'fa fa-chart-area',
            child: [
              {
                href: '/api/group/',
                title: 'Groups Statistics',
              }
            ]
          },
          {
            title: 'User Management',
            icon: 'fa fa-chart-area',
            child: [
              {
                href: '/api/user',
                title: 'Profile',
              }
            ]
          },
          {
            title: 'Setting',
            icon: 'fa fa-chart-area',
            child: [
              {
                href: '/api/groupstat',
                title: 'Preferences ',
              }
            ]
          }
        ]
      }
    },
    components: {GroupGadget, GroupStat, GroupList, UserProfile}
  }
</script>
