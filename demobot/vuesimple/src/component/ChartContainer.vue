<template>
  <div class="container">
    <pie-chart
      v-if="loaded"
      v-bind:chart-data="chartData"
      :options="options"/>
  </div>
</template>

<script>
  import PieChart from './Chart.vue'
  import {mixins} from 'vue-chart.js'
  import regeneratorRuntime from "regenerator-runtime";
  import {mapState} from "vuex"


  export default {
    name: 'PieChartContainer',
    components: {PieChart},
    //props: ["data", "options"],

    // data: () => ({
    //   loaded: false,
    //   chartData: null,
    //
    // }),

    data: function () {

      return {
        loaded: false,
        chartData: null,
      }
    },


    options: () => {
      options = null
    },
    methods: {
      drawchart() {

        var pie =  this.chartData = {
          labels: ['Men', 'Women'],
          datasets: [
            {

              label: 'Gender Ratio',
              backgroundColor: ['#3a2ff8', '#ef5ef9'],
              data: [this.$store.getters.getChart.total_men, this.$store.getters.getChart.total_women]
            }
          ],
        }
        return pie
      }
    },

    mounted() {
      var c = this.drawchart()
      this.loaded = true
    },
    computed: {

      setData: function () {
        this.loaded = false
        this.drawchart()
        this.options = null
        this.loaded = true


      }

    }
  }
</script>
