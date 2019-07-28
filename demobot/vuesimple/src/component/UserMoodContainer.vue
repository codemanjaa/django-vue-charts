<template>
  <div class="container">

    <reactive-bar v-if="loaded" :chartData=chartData v-bind="usermoodcontainer"  :options="{responsive: true, maintainAspectRatio: false}"/>
  </div>
</template>

<script>
  import ReactiveBar from "./ReactiveBar";
  import {mapState} from "vuex"
  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";

  export default {
    name: "UserMoodContainer",
    components: {ReactiveBar},
    data: () => ({
      loaded: false,
      chartData: null
    }),


    methods: {

      loadData: function (id) {

        //Test run
        if (id==null) {
          apiService.getUserMood('?id=f788476143e945f0a729c05294210604').then(data => {
            //apiService.getUserMood('?id=' + id).then(data => {
            this.chartData = data
            this.loaded = true
          })
        } else {
          apiService.getUserMood('?id=' + id).then(data => {
            //apiService.getUserMood('?id=' + id).then(data => {
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

    },
    updated() {

    }
  }
</script>

<style scoped>

</style>
