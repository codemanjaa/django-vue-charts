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
        <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Gender Ratio</h6>
        </div>
         <chart-container>

        </chart-container>

        <!--<group-chart></group-chart>-->
      </div>

      <div class="col-6">
        <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">Dynamic Ratio</h6>
        </div>

        <!--<div class="app">-->
          <!--{{ dataChart }}-->
          <!--<button v-on:click="changeData">Change data</button>-->
          <!--<line-chart :data="dataChart" :options="{responsive: true, maintainAspectRatio: false}"></line-chart>-->

        <!--</div>-->

        <group-chart>

        </group-chart>

        <!--</chart-container>-->
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

  export default {
    name: "GroupGadget",

    components: {ChartContainer, GroupChart},
    data() {
      return {
        groups: [],
        selected: '',
        groupusers: [],
        selecteduser: '',


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
      onChange: function () {
        var self = this
        console.log(self.groups);
        var gid = this.selected;
        console.log(gid);
        if (gid == "") {
          this.getGroupGadget();
        } else {
          //apiService.getGroupGadget('?gid='+this.selected).then((data) => {
          this.$store.dispatch('load_groupgadget_with_id', this.selected)
          //console.log(data)
          //this.groupgadget = data;
          //});

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
    computed: mapState(["groupgadget"])
  };
</script>

<style scoped>

</style>
