<template>
  <div class="container">
    <reactive-dognut v-if="loaded" :chartData="chartData" :options="{responsive: true, maintainAspectRatio: false}"/>
  </div>

</template>

<script>
  import ReactiveDognut from './ReactiveDognut'

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";

  export default {
    name: "GroupContextContainer",
    components: {ReactiveDognut},

    data: () => ({
      loaded: false,
      chartData: {}
    }),

    methods: {

      loadData: function () {

        apiService.getGroupContext('?gid=all').then(data => {
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
