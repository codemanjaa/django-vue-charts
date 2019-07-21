

<script>


  import {Bar, Pie, mixins} from 'vue-chartjs'
  import {mapState} from "vuex"
  import regeneratorRuntime from "regenerator-runtime"

  export default {
    extends: Pie,
    //mixins: [mixins.reactiveProp],
    //props: ['data', 'options'],
    mounted() {

      this.filldata();
      // this.renderChart(this.chartdata, this.options)


      // Overwriting base render method with actual data.

    },

    methods: {
      filldata: function() {
        this.renderChart({
          labels: ['Men', 'Women'],
          datasets: [
            {
              label: 'Gender Ratio',
              backgroundColor: ['#3a2ff8', '#ef5ef9'],
              data: [57, 37]
            }
          ]
        })

      }
    },
    computed: {
      setData:()=> {

        this.chartData = {
          labels: ['Men', 'Women'],
          datasets: [
            {

              label: 'Gender Ratio',
              backgroundColor: ['#3a2ff8', '#ef5ef9'],
              data: [this.$store.getters.getChart.total_men, this.$store.getters.getChart.total_women]
            }
          ],
        }
      }
    }
  }


  // export default {
  //   mixins : Bar,
  //   name: "GroupChart",
  //
  //   data: () => ({
  //     chartdata: {
  //       labels: ['January', 'February'],
  //       datasets: [
  //         {
  //           label: 'Data One',
  //           backgroundColor: '#f87979',
  //           data: [40, 20]
  //         }
  //       ]
  //     },
  //     options: {
  //       responsive: true,
  //       maintainAspectRatio: false
  //     },
  //     mounted() {
  //     this.renderChart(this.chartdata, this.options)
  //   }
  //   }),
  //
  // }

</script>

<style scoped>

</style>
