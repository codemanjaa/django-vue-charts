<template>
    
</template>

<script>
  import Vue from 'vue'
  import {Line} from 'vue-chartjs'

    Vue.component("line-chart", {
  extends: Line,
  props: ["data", "options"],
  mounted() {
    this.renderLineChart();
  },
  computed: {
    chartData: function() {
      return this.data;
    }
  },
  methods: {
    renderLineChart: function() {
    this.renderChart(
      {
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July"
        ],
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: this.chartData
          }
        ]
      },
      { responsive: true, maintainAspectRatio: false }
    );
    }
  },
  watch: {
    data: function() {
      this._chart.destroy();
      //this.renderChart(this.data, this.options);
      this.renderLineChart();
    }
  }
});

var vm = new Vue({
  el: "",
  data: {
    message: "Hello World",
    dataChart: [10, 39, 10, 40, 39, 0, 0],
    test: [4, 4, 4, 4, 4, 4]
  },
  methods: {
    changeData: function() {
      this.dataChart = [6, 6, 3, 5, 5, 6];
    }
  }
});
</script>

<style scoped>

</style>
