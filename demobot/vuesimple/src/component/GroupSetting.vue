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
      <div v-if="messageloaded" class="card text-white  bg-success mb-3 {class}" style="max-width: 50rem;">
        <div class="card-header">Phase Notification</div>
        <div class="card-body">
          <h5 class="card-title">{{message}}</h5>
          <p class="card-text">
            Please kindly refer the documentation for more details about the phase setting.
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
    name: "GroupSetting",
    data() {
      return {
        groups: [],
        currentGroup: {},
        message: '',
        messageloaded: false,
        class: ''

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
          var group = this.currentGroup[0]
          let curPhase = group.state
          let nextPhase;
          if (curPhase == 'cessation') {
            alert('Group does not have any Phase to move in')
            this.message = group.name + ' in the Final phase'
            this.messageloaded = true
            this.class = 'card text-white bg-success mb-3'

          } else if (curPhase == 'tracker') {
            nextPhase = 'profile'
            group.state = nextPhase
            this.message = 'Loaded to profile phase'
            this.messageloaded = true
          } else if (curPhase == 'profile') {
            nextPhase = 'cessation'
            group.state = nextPhase
            this.message = 'Loaded to Cessation phase'
            this.messageloaded = true
          } else if (curPhase == 'recruitment') {
            nextPhase = 'tracker'
            group.state = nextPhase
            this.message = 'Loaded to Tracker phase'
            this.messageloaded = true
          } else {
            this.message = 'Processing...'
          }
          apiService.updateGroup(group)

          console.log(curPhase)
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
