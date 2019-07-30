<template>
  <div id="app">
    <button @click="show = !show">Click</button>
    <div v-if="show">
      <line-chart :chart-data="message" :width="400" :height="200"></line-chart>

      <line-chart currency="€" :chart-data="message" :width="400" :height="200"></line-chart>
    </div>
  </div>
</template>

<script>

  import {Line, mixins} from "vue-chartjs";
  import Vue from 'vue';


  export default {
    extends: Line,
    name: "TestBar",
    props: {
      currency: {
        type: String,
        default: '$'
      }
    },
    data: () => ({
      message: 'Hello'
    }),
    computed: {
      options() {
        return {
          responsive: false,
          maintainAspectRatios: false,
          scales: {
            yAxes: [{
              ticks: {
                callback: (value, index, values) => {
                  return `£ ${value} ${this.currency}`;
                },
              },
            }],
          },
          tooltips: {
            enabled: true,
            callbacks: {
              label: ((tooltipItems, data) => {
                console.log(this)
                return tooltipItems.yLabel + '£' + this.message
              })
            }
          }
        }
      }
    },
    mixins: [mixins.reactiveProp],
    mounted() {
      this.renderChart(this.chartData, this.options)
    }

  }


  var vm = new Vue({
    el: '#app',
    data: {
      show: true,
      message: {}
    },

    mounted() {
      setInterval(() => {
        this.fillData()
      }, 5000)
    },
    methods: {
      fillData() {
        this.message = {
          labels: ['January' + this.getRandomInt(),
            'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
              label: 'Data One',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(), this.getRandomInt(),
                this.getRandomInt(), this.getRandomInt(),
                this.getRandomInt(), this.getRandomInt(),
                this.getRandomInt(), this.getRandomInt(),
                this.getRandomInt(), this.getRandomInt(),
                this.getRandomInt(), this.getRandomInt()]
            }
          ]
        }
      },

      getRandomInt() {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      }
    }
  })

</script>
