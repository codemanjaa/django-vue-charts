<template>
  <div class="container">
    <reactive-bar v-if="loaded" :chartData="chartData" :options="{responsive: true, maintainAspectRatio: false}"/>
  </div>

</template>

<script>
  import ReactiveBar from './ReactiveBar'

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";
  import GroupGadget from "./GroupGadget";

  export default {
    name: "GroupMoodAllContainer",
    components: {ReactiveBar},
    data: () => ({
      loaded: false,
      chartData: {}
    }),


    methods: {

      loadData: function (id) {

       // GroupGadget.methods.getGroupMoodAll()


         apiService.getGroupMoodAll('?gid=').then(data => {
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
