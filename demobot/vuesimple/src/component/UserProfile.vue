<template>
  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">User Statistics</h4>
    </div>

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">
      <div class="row">
        <div class="col-12">
          <div class="dropdown">

            <select class="form-control form-control-lg btn-primary" name="grouplist" id="grouplist" v-model="selected"
                    v-on:change="onChange">
              <option value="" v-show="getGroupGadget" disabled>Select a Group</option>
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

      </div>
    </div>

    <div style="margin-top: 25px">
      <div class="row">
        <div class="col-12">
          <table class="table table-striped">
            <thead>
            <tr v-if="userloaded">
              <th>#</th>
              <th @click="sort('name')">Name</th>
              <th @click="sort('last name')">Last Name</th>
              <th @click="sort('date')">Last Interaction Date</th>
            </tr>
            </thead>

            <tbody>
            <tr v-for="user, index in sortedUsers" class="clickable" data-toggle="collapse" data-target="#userstats"
                aria-expanded="false" aria-controls="userstats">
              <td>{{index+1}}</td>
              <td>{{user.first_name}}</td>
              <td>{{user.last_name}}</td>
              <td>{{user.last_interaction}}</td>
              <td>
                <button class="btn-secondary" @click="viewProfile(user.id)">View</button>
              </td>
            </tr>
            <tr>
            </tr>
            </tbody>
            <tbody id="userstats" class="collapse" v-if="userloaded">
            <tr aria-rowspan="">

            </tr>


            </tbody>

          </table>
          <!--debug: sort={{currentSort}}, dir = {{currentSortDirection}}-->
          <p>
            <button @click="prevPage">Previuos</button>
            <button @click="nextPage">Next</button>
          </p>

        </div>

      </div>
    </div>

    <div class="container showtime" v-if="userdetailsloaded" id="showtime" ref="showtime">

      <div class="row" style="margin-top: 25px">
        <div class="col-12">
          <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">User Details</h6>
          </div>

          <div class="form-group row" style="background-color: #eeeeee; margin-left:5px; margin-top: 10px;">

            <label class="col-sm-4 col-form-label">First Name</label>
            <div class="col-sm-8" style="margin-bottom: 2px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].first_name">
            </div>
            <label class="col-sm-4 col-form-label">Last Name </label>
            <div class="col-sm-8" style="margin-bottom: 2px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].last_name">
            </div>

            <label class="col-sm-4 col-form-label">Gender</label>
            <div class="col-sm-8" style="margin-bottom: 2px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].gender">
            </div>
            <label class="col-sm-4 col-form-label">State </label>
            <div class="col-sm-8" style="margin-bottom: 2px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].state">
            </div>
            <label class="col-sm-4 col-form-label">Facebook Id</label>
            <div class="col-sm-8" style="margin-bottom: 2px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].facebook_id">
            </div>
            <label class="col-sm-4 col-form-label">Last Interaction on: </label>
            <div class="col-sm-8" style="margin-bottom: 2px;margin-bottom: 5px;">
              <input type="text" readonly class="form-control" v-bind:value="userdetails[0].last_interaction">
            </div>
            <div style="background-color: goldenrod; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">Group Modification</h6>
          </div>
            <div style="background-color: #86989B" class="col-sm-12">

              <div class="row">
                <label class="col-sm-4 col-form-label">Group ID: </label>
                <br/>
                <div class="col-sm-2" style="margin-bottom: 2px;">
                  <input type="text" readonly align="center" class="form-control" v-bind:value="userdetails[0].gid">
                </div>
                <div class="col-sm-4" style="margin-bottom: 10px; margin-top: 5px">


                  <select class="form-control form-control-sm btn-secondary" name="gplist" id="gplist" v-model="selectedgid"
                          v-on:change="getgid">
                    <option value="" disabled>{{userdetails[0].gid}}</option>
                    <option v-for="group in groups" v-bind:value="group.id">
                      {{group.id}} - {{group.name}}
                    </option>
                  </select>

                </div>
                <div class="col-sm-2" style="margin-bottom: 10px; margin-top: 5px">
                  <input type="hidden" name="gid" v-bind:value="userdetails[0].id">
                  <button class="btn-primary" @click="modify(userdetails[0].id)">Move</button>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
      <button v-on:click="isHidden = !isHidden">Show Notification</button>
      <br/>
      <div v-if="!isHidden" class="card border-warning mb-3"
           style="max-width: 48rem;">
        <div class="card-header">Visual Notification Alert</div>
        <div class="card-body text-warning">
          <h5 class="card-title">Graphic inconsistent</h5>
          <p class="card-text">Please kindly note that, due to the lack of availabe data, you might encounter with
            some empty charts or visual inconsitency in the Stats area below.
            <button v-on:click="isHidden = !isHidden">Hide me</button>
          </p>
        </div>
      </div>

      <div class="row" style="margin-top: 25px">
        <div class="col-6">
          <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">User Mood Stats</h6>
          </div>
          <user-chart :chart-data="usermoodstas" :options="{responsive: true, maintainAspectRatio: false}"></user-chart>

        </div>

        <div class="col-6">
          <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">User Loneliness Stats</h6>

          </div>
          <user-pie :chart-data="useralonestats" :options="{responsive: true, maintainAspectRatio: false}"></user-pie>


        </div>
      </div>
      <div class="row" style="margin-top: 25px">
        <div class="col-6">
          <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">User Smoking Drive Stats</h6>
          </div>
          <user-pie :chart-data="userdrivestats" :options="{responsive: true, maintainAspectRatio: false}"></user-pie>

        </div>

        <div class="col-6">
          <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

            <h6 class="card-title">User Distraction Stats</h6>

          </div>
          <user-chart :chart-data="userdistractionstats"
                      :options="{responsive: true, maintainAspectRatio: false}"></user-chart>


        </div>
      </div>
    </div>

  </div>


</template>

<script>

  import {APIService} from "../api/APIService";
  import UserMoodContainer from "./UserMoodContainer";
  import UserDetails from "./UserDetails";
  import UserDistractContainer from "./UserDistractContainer";
  import UserAloneContainer from "./UserAloneContainer";
  import UserDriveContainer from "./UserDriveContainer";
  import {mapState} from "vuex"
  import UserChart from "./UserChart";
  import UserPie from "./UserPie";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    name: "UserProfile",

    components: {UserPie, UserChart, UserDriveContainer, UserAloneContainer, UserDistractContainer, UserMoodContainer},
    data() {
      return {
        groupgadget: [],
        groups: [],
        selected: '',
        groupusers: [],
        selecteduser: '',
        currentSort: 'name',
        currentSortDirection: 'asc',
        pageSize: 10,
        currentPage: 1,
        usermoodstas: {},
        useralonestats: {},
        userdrivestats: {},
        userdistractionstats: {},
        userdetails: {},
        userdetailsloaded: false,
        userloaded: false,
        isHidden: false,
        selectedgid: '',
        user: {},

      };

    },
    methods: {
      getGroupGadget() {
        apiService.getUsers().then(data => {
          console.log(data);
          this.groupgadget = data;
        });
      },
      getGroups() {

        apiService.getGroups().then((data) => {
          console.log(data)
          this.groups = data;
          this.numberOfGroups = data.length;
        });
      },
      getGroupUsers() {
        apiService.getUsers().then(data => {
          this.groupusers = data;
        })
      },
      nextPage: function () {
        if ((this.currentPage * this.pageSize) < this.groupusers.length) this.currentPage++;
      },
      prevPage: function () {
        if (this.currentPage > 1) this.currentPage--;
      },
      sort: function (s) {
        if (s === this.currentSort) {
          this.currentSortDirection = this.currentSortDirection === 'asc' ? 'desc' : 'asc';
        }
        this.currentSort = s;

      },
      viewProfile: function (id) {
        if (id == null) {
          console.log('This is a profile check...' + id)
        } else {

          apiService.getUserMood('?id=' + id).then(data => {
            //UserMoodContainer.methods.loadData(id)
            this.$store.dispatch('LOAD_USERMOODCONTAINER_WITH_id', id)
            this.usermoodstas = data

            // console.log('mood stats.... '+this.usermoodstas.datasets[0].data)


          });
          apiService.getUserAlone('?id=' + id).then(data => {
            this.useralonestats = data
            this.userloaded = true
          });

          apiService.getUserDrive('?id=' + id).then(data => {
            this.userdrivestats = data
            this.userloaded = true
          });

          apiService.getUserDistract('?id=' + id).then(data => {
            this.userdistractionstats = data
            this.userloaded = true
          });
          // this.goto('showtime')


          apiService.getUserDetails('?id=' + id).then(data => {
            this.userdetails = data
            this.userdetailsloaded = true
            console.log(data)

          });
        }


        window.scrollTo({
          top: 650,
          left: 100,
          behavior: 'smooth'
        });


        console.log('This is a retrieved user id: ' + id);


      },

      onChange: function () {
        var self = this
        console.log(self.groups);
        var gid = this.selected;
        console.log(gid);
        if (gid == "") {
          this.getGroupGadget();
        } else {
          apiService.getGroupGadget('?gid=' + this.selected).then((data) => {
            console.log(data)
            this.groupgadget = data;
          });

          apiService.getUsers('?gid=' + this.selected).then((data) => {
            console.log(data)
            this.groupusers = data;
          });


        }


      },
      getgid: function () {
        var self = this
        console.log(self.groups);
        var gid = this.selectedgid;
        console.log(gid);


      },

      modify: function (id) {
        var user = this.userdetails[0]
        let gid = this.selectedgid
        let uid = id

        if(gid == user.gid){
          alert('Please select the different group id')
        }
        else{
          user.gid = gid
           apiService.updateUser(user)
        }

        console.log(user)


      }


    },
    computed: {
      sortedUsers: function () {
        return this.groupusers.sort((a, b) => {
          let modifier = 1;
          if (this.currentSortDirection === 'desc') modifier = -1;
          if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
          return 0;
        }).filter((row, index) => {
          let start = (this.currentPage - 1) * this.pageSize;
          let end = this.currentPage * this.pageSize;
          if (index >= start && index < end) return true;
        });

      },

    },
    mounted() {

      // this.getGroupGadget();
      this.getGroups();

    },


  };
</script>

<style scoped>

</style>
