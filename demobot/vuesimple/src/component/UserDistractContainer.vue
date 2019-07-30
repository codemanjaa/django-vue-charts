<template>
   <div class="container">

    <reactive-bar v-if="loaded" :chartData=chartData   :options="{position: 'relative',
responsive: true, maintainAspectRatio: false  }"/>
  </div>

</template>

<script>
  import ReactiveBar from "./ReactiveBar";
  import {mapState} from "vuex"

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";

  export default {
    name: "UserDistractContainer",
    components: {ReactiveBar},
    data: () => ({
      loaded: false,
      chartData: null
    }),

       methods: {

      loadData: function (id) {

        //Test run
        if (id==null) {
          apiService.getUserDistract('?id=f788476143e945f0a729c05294210604').then(data => {
            //apiService.getUserMood('?id=' + id).then(data => {
            this.chartData = data
            this.loaded = true
          })
        } else {
          apiService.getUserDistract('?id=' + id).then(data => {
            this.chartData = data
            this.loaded = true
          })

        }


      },
      renderChart: function (data, options) {

        this.chartData = data
        this.options = options

      }
    },

    computed: mapState(["usermoodcontainer"]),


    mounted() {
       // this.renderChart(this.chartData, this.options)
      this.loadData(this.id)

    }
  }
</script>

<style scoped>

</style>
