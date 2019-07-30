<template>
  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">Group Statistics</h4>
    </div>

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">
      <div class="row">
        <div class="col-9">
          <div class="dropdown">

            <select name="grouplist" id="grouplist" v-model="selected" v-on:change="onChange">
              <option value="">Select a Group</option>
              <option value="all">all</option>
              <option v-for="group in groups" v-bind:value="group.id">
                {{group.id}} - {{group.name}}
              </option>
            </select>


            <div class="dropdown-menu" aria-labelledby="groupSelector">
              <a class="dropdown-menu" href="#">Group1</a>
            </div>
          </div>
        </div>
        <div>
          <div class="col">
            <select name="groupuserlist" id="groupuserlist" v-model="selected" v-on:change="onChange" autocomplete="on">
              <option value="" v-show="">Select a user</option>
              <option v-for="user in groupusers">
                {{user.first_name}}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div style="margin-top: 25px">
      <div class="row">
        <div class="col-3">
          <div class="card bg-light mb-sm-n1" style="max-width: 10rem">
            <div class="card-header">State</div>
            <div class="card-body center">
              <center><h6>{{groupgadget.state}}</h6></center>

            </div>


          </div>
        </div>
        <div class="col-3">
          <div class="card bg-light mb-sm-n1" style="max-width: 8rem">
            <div class="card-header">Men</div>
            <div class="card-body">
              <center><h5>{{groupgadget.total_men}} </h5></center>
            </div>
          </div>
        </div>
        <div class="col-3">
          <div class="card bg-light mb-sm-n1" style="max-width: 8rem">
            <div class="card-header">Women</div>
            <div class="card-body">
              <center><h5>{{groupgadget.total_women}}</h5></center>
            </div>
          </div>
        </div>
        <div class="col-3">
          <div class="card bg-light mb-sm-n1" style="max-width: 8rem">
            <div class="card-header">Total</div>
            <div class="card-body">
              <center><h5>{{groupgadget.total_user}}</h5></center>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="row" style="margin-top: 25px">
      <div class="col-6">

        <div v-if="chartgenderloaded"
             style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Gender Stats</h6>
        </div>


        <gender-pie v-if="chartgenderloaded" :chartData="chartgenderdata"
                    :options="{responsive: true, maintainAspectRatio: false}"/>

        <!--<group-chart></group-chart>-->
      </div>

      <div class="col-6">
        <div v-if="totalcigarloaded"
             style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Total Cigars Stats</h6>

        </div>
        <total-cigars-bar v-if="totalcigarloaded"></total-cigars-bar>

        <!--<user-bar-container></user-bar-container>-->
      </div>
    </div>

    <div class="row" style="margin-top: 25px">
      <div class="col-12">
        <div v-if="groupmoodloaded"
             style="background-color: #E8EFF0; margin-top: 10px; width: 600px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Mood Bar</h6>
        </div>

        <group-mood-reactive-bar v-if="groupmoodloaded" :chartData="groupmoodchardata"
                                 :options="{responsive: true, maintainAspectRatio: false}"/>

      </div>

    </div>

    <div class="row" style="margin-top: 25px">
      <div class="col-12">
        <div v-if="chartactive"
             style="background-color: #E8EFF0; margin-top: 10px; width: 600px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Group Desire Stats</h6>
        </div>
        <group-desire-reactive-bar v-if="groupdesireloaded" :chartData="groupdesirechartdata"
                                   :options="{responsive: true, maintainAspectRatio: false}"/>

      </div>

    </div>

    <div class="row" style="margin-top: 25px">
      <div class="col-12">
        <div v-if="chartactive"
             style="background-color: #E8EFF0; margin-top: 10px; width: 600px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Context Stats</h6>
        </div>

        <group-context-container v-if="chartactive">
          <reactive-dognut :chartData=this.groupcontextchartdata></reactive-dognut>
        </group-context-container>

      </div>

    </div>


    <div class="row" style="margin-top: 25px">
      <div class="col-12">
        <div v-if="chartactive" style="background-color: #E8EFF0; margin-top: 10px; width: 600px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Mood Doughnut Stats</h6>
        </div>

        <mood-doughnut  v-if="groupmoodloaded" :chartData="groupmoodchardata"
                                 :options="{responsive: true, maintainAspectRatio: false}"/>

      </div>

    </div>
    <div class="row" style="margin-top: 25px">
      <div class="col-12">

        <div v-if="chartactive"
             style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title"></h6>
        </div>


      </div>


    </div>


  </div>


</template>

<script>

  import {APIService} from "../api/APIService";
  import GroupChart from './GroupChart'

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  import {mapState} from "vuex"
  import ChartContainer from "./ChartContainer";
  import GroupLineChart from './GroupLineChart'
  import UserBarContainer from "./UserBarContainer";
  import ReactiveBarContainer from "./ReactiveBarContainer";
  import GenderPieContainer from "./GenderPieContainer";
  import MoodPieContainer from "./MoodPieContainer";
  import TotalCigarsBar from "./TotalCigarsBar";
  import GroupContextContainer from "./GroupContextContainer";
  import ReactiveDognut from "./ReactiveDognut";
  import GroupMoodAllContainer from "./GroupMoodAllContainer";
  import TestBar from './TestBar'
  import GroupMoodReactiveBar from "./GroupMoodReactiveBar";
  import GroupDesireReactiveBar from "./GroupDesireReactiveBar";
  import GenderPie from "./GenderPie";
  import MoodDoughnut from "./MoodDoughnut";

  export default {
    name: "GroupGadget",

    components: {
      MoodDoughnut,
      GenderPie,
      GroupDesireReactiveBar,
      GroupMoodReactiveBar,
      GroupMoodAllContainer,
      ReactiveDognut,
      TestBar,
      GroupContextContainer,
      TotalCigarsBar,
      MoodPieContainer,
      GenderPieContainer, ReactiveBarContainer, UserBarContainer, ChartContainer, GroupChart,
    },
    data() {
      return {
        groups: [],
        selected: '',
        groupusers: [],
        selecteduser: '',
        groupmoodchardata: {},
        groupdesirechartdata: {},
        groupcontextchartdata: {},
        chartgenderdata: {},
        groupmoodloaded: false,
        groupdesireloaded: false,
        chartgenderloaded: false,
        totalcigarloaded: false,
        chartactive: false


      };

    },
    methods: {
      getGroupGadget() {
        this.$store.dispatch('load_groupgadget')

      },
      getGroups() {

        apiService.getGroups().then((data) => {
          console.log(data)
          this.groups = data;
          this.numberOfGroups = data.length;

        });
      },
      getGroupUserList() {
        apiService.getGroupUserList().then(data => {
          this.groupusers = data;
        })
      },

      getGroupPie() {

        apiService.getGroupPie('?gid=' + this.selected).then((data) => {
          this.$store.dispatch('LOAD_PIECHARTDATA_with_id', this.selected)
          //GenderPieContainer.$set.data.chartData = this.$store.state.getPiechart()
          console.log("Group pie    " + this.$store.state.getPiechart)
          //this.groupusers = data;
        });


      },

      getGroupContext() {
        apiService.getGroupContext().then((data) => {

        })

      },
      getGroupMoodAll() {
        apiService.getGroupMoodAll().then((data) => {
          this.groupmoodchardata = data

        })
      },


      onChange: function () {
        var self = this
        console.log(self.groups);
        var gid = this.selected;
        console.log(gid);
        if (gid == "") {
          this.getGroupGadget();
          this.getGroupContext();

        } else {
          //apiService.getGroupGadget('?gid='+this.selected).then((data) => {
          this.$store.dispatch('load_groupgadget_with_id', this.selected)
          this.$store.dispatch('LOAD_USERDESIREDATA')
          this.totalcigarloaded = true
          this.chartactive = true

          apiService.getGroupContext('?gid=' + this.selected).then((data) => {
            this.groupcontextchartdata = data
            console.log('This is group context chart data ' + data)

          });
          apiService.getGroupMoodAll('?gid=' + this.selected).then((data) => {
            this.groupmoodchardata = data
            this.groupmoodloaded = true


            console.log('This is group mood  for ' + this.selected + ' >>>> ' + data.datasets + this.groupmoodloaded)

          });

          apiService.getGroupDesireAll('?gid=' + this.selected).then((data) => {
            this.groupdesirechartdata = data
            this.groupdesireloaded = true
            console.log('This is group mood  for ' + this.selected + ' >>>> ' + data.datasets + this.groupmoodloaded)

          });


          apiService.getGroupPie('?gid=' + this.selected).then((data) => {
            this.chartgenderdata = data
            this.chartgenderloaded = true
            this.$store.dispatch('LOAD_PIECHARTDATA_with_id', this.selected)
          });

          apiService.getUsers('?gid=' + this.selected).then((data) => {
            console.log(data)
            this.groupusers = data;
          });


        }


      },

    },
    mounted() {

      // this.getGroupGadget();
      this.getGroups();


    },
    computed: mapState(["groupgadget", "GenderPieContainer"])
  };
</script>

<style scoped>

</style>
