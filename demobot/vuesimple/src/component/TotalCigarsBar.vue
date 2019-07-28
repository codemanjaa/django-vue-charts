<template>
  <div class="container">
    <reactive-bar v-if="loaded" :chartData="chartData" :options="null"/>
  </div>
</template>

<script>
  import ReactiveBar from './ReactiveBar'

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";


  export default {
    name: "TotalCigarsBar",
    components: {ReactiveBar},
    data: () => ({
      loaded: false,
      chartData: null
    }),


    methods: {

      loadData: function () {

        apiService.getGroupTotal().then(data => {
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
