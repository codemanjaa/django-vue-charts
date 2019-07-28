<template>
  <div class="container">
    <user-chart
      v-if="loaded"
      v-bind:chart-data="chartData"
    />
  </div>
</template>

<script>
  import UserChart from './UserChart'
  import regeneratorRuntime from "regenerator-runtime";
  import {APIService} from "../api/APIService";

  const API_URL = 'http://localhost:8000';
  const apiService = new APIService();


  export default {
    name: 'BarChartContainer',
    components: {UserChart},

    data: () => ({
      chartData: null,
      options: null,
      loaded: false,
      datapoints: []
    }),

    // data() {
    //   return {
    //     datapoints: [],
    //     loaded: false,
    //     chartdata: null
    //   }
    // },
    methods: {
      getData() {
        apiService.getUserProfile().then(data => {
          this.datapoints = [data.desirenone, data.desirelow, data.desiremedium, data.desirehigh, data.desireextreme]

        })

      },

      drawBar() {
        this.getData()
        var bar = this.chartData = {
          labels: ['None', 'Low', 'Medium', 'High', 'Extreme'],
          datasets: [{
            label: '# Desire Behavior',
            data: this.datapoints,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        }
          this.options = {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true
                }
              }
            ]
          },
          maintainAspectRatio: false,
          title: {
            display: true,
            text: "Desire  Stats"
          }
        }

      }


    },
    async mounted() {
      this.loaded = false
      try {
        await this.drawBar()
        this.loaded = true
      } catch (e) {
        console.error(e)
      }
    },
    computed: {
      setBar: function () {
        this.drawBar()


      }
    }

  }

</script>




