import Vue from 'vue'
import App from './App.vue'
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router.js'
import store from './store'



Vue.use(BootstrapVue)
Vue.use(VueSidebarMenu)


new Vue({
  el: '#app',
  data() {
    return {
      info : null
    }
  },
  beforeCreate(){
    Vue.prototype.$http = axios
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    axios.defaults.xsrfCookieName = 'csrftoken'
  },
  router,
  store,

  mounted (){
    axios
      .get('http://localhost:8000/api/groupstat/')
      .then(response => this.info = response)
  },
  render: h => h(App)
})





