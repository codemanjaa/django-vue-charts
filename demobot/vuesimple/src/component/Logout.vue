<template>
  <div class="container-fluid">

    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">

      <h4 class="card-title">Log out</h4>

    </div>
  </div>
</template>

<script>
  import {APIService} from "../api/APIService";
  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    name: "Logout",

    methods: {
      logout(){
        apiService.logout()
      },
      mounted(){
        console.log('?????');
        this.logout()

      }

    }
  }

</script>

<style scoped>

</style>
