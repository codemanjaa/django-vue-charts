<script>

  import {Doughnut} from 'vue-chartjs'

  export default {
    extends: Doughnut,
    props: {
      chartData: {
        type: Object,
        default: null
      },
      options: {
        type: Object,
        default: null
      }
    },
    methods: {
      render() {
        this.renderChart(this.chartData, this.options)
      }
    },


    mounted() {
      this.render()
    },
    watch: {
    'chartData': {
      handler(newOption, oldOption) {
        this.renderChart(this.chartData, this.options)
      },
      deep: true
    }
  }
  }
</script>
