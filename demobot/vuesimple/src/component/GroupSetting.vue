<template>

  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">Phase Setting</h4>
    </div>
    <div class="col-12">
      <table class="table table-striped">
        <thead>
        <tr>

          <th>ID</th>
          <th>Name</th>
          <th>Created Date</th>
          <th>Current Phase</th>
          <th>Next</th>

        </tr>
        </thead>
        <tbody>
        <tr v-for="group, index in groups" class="clickable" data-toggle="collapse" data-target="#userstats"
            aria-expanded="false" aria-controls="userstats">
          <td>{{group.id}}</td>
          <td>{{group.name}}</td>
          <td>{{group.created_at}}</td>
          <td>{{group.state}}</td>
          <td>
            <button class="btn-secondary" @click="setState(group.id)">Next Phase</button>
          </td>
        </tr>
        <tr>

        </tr>
        </tbody>
      </table>
    </div>
    <div>
      <{{message}}>
    </div>
  </div>

</template>

<script>
  import {APIService} from "../api/APIService";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    name: "GroupSetting",
    data() {
      return {
        groups: [],
        currentGroup: {},
        message: ''
      }
    },
    methods: {

      getGroups() {
        apiService.getGroups().then((data) => {
          console.log(data)
          this.groups = data;


        });
      },

      setState: function (id) {

        apiService.getGroupDetails('?id=' + id).then((data) => {
          this.currentGroup = data
          let curstate = this.currentGroup[0].state

          if (curstate == 'cessation') {
            alert('You do not have any Phase to move in')
            this.message = 'Sorry..You are in Final phase'
          } else if (curstate == 'tracker') {
            this.message = 'span class="badge badge-pill badge-success">Success</span'
          } else if (curstate == 'recruitment') {
            this.message = 'Recruitment to Tracker'
          } else {
            this.message = 'Processing...'
          }

          console.log(curstate)
        });


      }
    },
    mounted() {
      this.getGroups()

    }
  }
</script>

<style scoped>

</style>
