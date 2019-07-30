<script>
  import {Doughnut, mixins} from "vue-chartjs";

  export default {
    name: "MoodPie",
    extends: Doughnut,
    mixins: [mixins.reactiveProp],
    props: ["options"],

    mounted() {
      // this.chartData is created in the mixin.
      // If you want to pass options please create a local options object
      this.renderChart(this.chartData, this.options);
    }

  }
</script>

<style scoped>

</style>
