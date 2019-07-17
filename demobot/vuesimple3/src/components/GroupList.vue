<template>
<div>
<h1>Group Statistics</h1>
<div class="container" id="group">
      <h3 class="text-center">Group List</h3>
      <div class="columns medium-4" >
        <div class="card">
          <div class="card-section">
            <p> Number of Groups: {{groups.length}}  </p>
          </div>
          <div class="card-divider">
            <p></p>
          </div>
        </div>
      </div>
    </div>

<table class="table table-bordered table-hover" border="1">

<thead>

<tr>

<th>Group</th>
<th>Name</th>
<th>State</th>
<th>Created Date</th>

</tr>
</thead>
<tbody>
<tr v-for="group in groups">

<th>{{ group.id }}</th>

<th>{{ group.name }}</th>
<th>{{ group.state }}</th>
<th>{{ group.created_at}}</th>

</tr>
</tbody>
</table>
<div>
</div>
</div>

</template>

<script>


import {APIService} from "../api/APIService";

const API_URL = 'http://localhost:8000';
const apiService = new APIService();

export default {

name: 'GroupList',

components: {

},

data() {

  return {
  groups: [],
  numberOfGroups:0,

   };

},

methods: {

getGroups(){
    apiService.getGroups().then((data) => {
        console.log(data)
        this.groups = data;
        this.numberOfGroups= data.length;
    });
},
},

mounted() {
  this.getGroups();
  },
}
</script>
