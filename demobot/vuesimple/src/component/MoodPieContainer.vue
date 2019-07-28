<template>
<div class="container">
  <mood-pie v-if="loaded" :chartData="chartData" :options="null"></mood-pie>
</div>
</template>

<script>
  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";
  import MoodPie from './MoodPie'

  export default {
    name: "MoodPieContainer",
    components: {MoodPie},

    data: () => ({
      loaded: false,
      chartData: null,
      first: true

    }),

     methods: {

      loadData: function () {
        let self = this;
        apiService.getGroupMood().then(data => {
          this.chartData = data
          this.loaded = true
        })
      }
     },

    mounted() {
      this.loadData()
    }

  }
</script>

<style scoped>

</style>
