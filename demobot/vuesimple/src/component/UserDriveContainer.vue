<template>
  <div class="container">
    <mood-pie v-if="loaded" :chartData="chartData" :options="{responsive: true, maintainAspectRatio: false}"></mood-pie>
  </div>
</template>

<script>
  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";
  import MoodPie from './MoodPie'

  export default {
    name: "UserDriveContainer",
    components: {MoodPie},

    data: () => ({
      loaded: false,
      chartData: null,


    }),

    methods: {

      loadData: function (id) {

        //Test run
        if (id == null) {
          apiService.getUserDrive('?id=f788476143e945f0a729c05294210604').then(data => {
            //apiService.getUserMood('?id=' + id).then(data => {
            this.chartData = data
            this.loaded = true
          })
        } else {
          apiService.getUserDrive('?id=' + id).then(data => {
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

    mounted() {
      this.loadData()
    }
  }
</script>

<style scoped>

</style>
