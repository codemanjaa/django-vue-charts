<template>
  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">Group Statistics</h4>
    </div>

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">
      <div class="row">
        <div class="col-9">
          <div class="dropdown">

            <select name="grouplist" id="grouplist" v-model="selected"  v-on:change="onChange">
              <option value="" v-show="getGroupGadget">Select a Group</option>
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
            <select name="groupuserlist" id="groupuserlist" v-model="selected" v-on:change="onChange">
            <option value="" v-show="">Select a user</option>
              <option v-for="user in groupusers" >
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
              <center><h5>{{groupgadget.state}}</h5></center>

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
  </div>


</template>

<script>

  import {APIService} from "../api/APIService";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    name: "GroupGadget",

    components: {},
    data() {
      return {
        groupgadget: [],
        groups: [],
        selected: '',
        groupusers: [],
        selecteduser: '',


      };

    },
    methods: {
      getGroupGadget() {
        apiService.getGroupGadget().then(data => {
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
      getGroupUserList(){
        apiService.getGroupUserList().then(data =>{
          this.groupusers = data;
        })
      },
      onChange: function () {
        var self = this
        console.log(self.groups);
        var gid = this.selected;
        console.log(gid);
       if(gid==""){
         this.getGroupGadget();
       }
       else{
          apiService.getGroupGadget('?gid='+this.selected).then((data) => {
          console.log(data)
          this.groupgadget = data;
        });

          apiService.getUsers('?gid='+this.selected).then((data) => {
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
  };
</script>

<style scoped>

</style>
