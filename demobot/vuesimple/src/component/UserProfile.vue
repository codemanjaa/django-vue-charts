<template>
  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">User Statistics</h4>
    </div>

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">
      <div class="row">
        <div class="col-9">
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
            <tr>
              <th @click="sort('name')">Name</th>
              <th @click="sort('group')">Group</th>
              <th @click="sort('date')">Join Date</th>
            </tr>
            </thead>

            <tbody>
            <tr v-for="user in sortedUsers">
              <td>{{user.first_name}}</td>
              <td>{{user.gid}}</td>
              <td>{{user.last_interaction}}</td>
              <td>
                <button class="btn-secondary" >View</button>
              </td>
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
  </div>


</template>

<script>

  import {APIService} from "../api/APIService";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    name: "UserProfile",

    components: {},
    data() {
      return {
        groupgadget: [],
        groups: [],
        selected: '',
        groupusers: [],
        selecteduser: '',
        currentSort: 'name',
        currentSortDirection: 'asc',
        pageSize:10,
        currentPage: 1


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
      nextPage: function(){
        if((this.currentPage*this.pageSize)<this.groupusers.length) this.currentPage++;
      },
      prevPage: function(){
        if(this.currentPage > 1) this.currentPage--;
      },
      sort: function (s) {
        if (s === this.currentSort) {
          this.currentSortDirection = this.currentSortDirection === 'asc'?'desc':'asc';
        }
        this.currentSort = s;

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
          let start  = (this.currentPage-1)*this.pageSize;
          let end  = this.currentPage*this.pageSize;
          if(index >= start && index <end) return true;
        });

      }
    },
    mounted() {

      // this.getGroupGadget();
      this.getGroups();

    },
  };
</script>

<style scoped>

</style>
