<script>

  import {Bar} from 'vue-chartjs'

  export default {
    extends: Bar,
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
