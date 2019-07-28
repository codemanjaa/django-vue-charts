<template>
  <div class="container">
    <div class="row" style="margin-top: 25px">
      <div class="col-6">
        <div style="background-color: #E8EFF0; margin-top: 10px; width: 300px; margin-bottom: 5px; padding: 5px;">

          <h6 class="card-title">User Details</h6>
        </div>
        <UserMoodContainer></UserMoodContainer>
      </div>
  </div>
  </div>
</template>

<script>

  import UserMoodContainer from './UserMoodContainer'

    export default {
        name: "UserDetails",
        components: {UserMoodContainer,}

    }
</script>

<style scoped>

</style>
