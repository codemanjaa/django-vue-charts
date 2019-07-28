<script>

  import {Pie, mixins} from 'vue-chartjs'
  import regeneratorRuntime from "regenerator-runtime";

  export default {
    extends: Pie,
     mixins: [mixins.reactiveProp],
    // props: ['chartData', 'options'],
     props: {
     chartData: {
       type: Object,
       default: null,

     },
       options: {
         type: Object,
         default: null
       }
     },
    mounted() {
      this.renderChart(this.chartData, this.options)
    }
  }
</script>

<style scoped>

</style>
