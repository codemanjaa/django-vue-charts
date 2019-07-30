<template>
  <div class="container">
    <gender-pie v-if="loaded" :chartData="chartData" :options="{responsive: true, maintainAspectRatio: false}"/>
  </div>
</template>

<script>

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();
  import {APIService} from "../api/APIService";
  import GenderPie from './GenderPie'

  export default {

    name: "GenderPieContainer",
    components: {GenderPie},
    data: () => ({
      loaded: false,
      chartData: {},
      first: true

    }),


    methods: {

      loadData: function () {
        let self = this;
        apiService.getGroupPie('?gid=all').then(data => {
          this.chartData = data
          this.loaded = true
        })


      },

      loadsecond: function () {
        apiService.getGroupPie().then(data => {
          this.chartData = data
          this.loaded = true
        })

      }
    },


    mounted() {
      if (this.first) {
        this.loadData()
        console.log('First of the mounted')
        this.first = false
      } else {
        this.loadsecond()
        console.log('Second of the mounted')
      }


    },
    computed: {},

    created() {
      //this.loadData()
    },
    watch: {
      chartData: function (newValue, oldValue) {

        console.log('This is chartData....')

      }
    }

  }
</script>

<style scoped>

</style>
