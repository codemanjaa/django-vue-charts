<template>
    <div align="center">
    <h1>Testing Version</h1>
      <div>
        <ol>
          <li v-for="group in groups">
            {{computeStats(group.id).total_user}} {{computeStats(group.id).total_men}} {{computeStats(group.id).total_women}}
          </li>
        </ol>
      </div>
    </div>
</template>

<script>

  import {APIService} from "../api/APIService";
  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
        name: "GroupStat",

        components: {},
        data(){
          return {
            groupstat: [],
            currentGroupId: -1,
            currentGroup : {},
            groups : []
          };

        },
        methods:{
          getGroupStats(){
            apiService.getGroupStats().then(data =>{
            console.log(data);
            this.groupstat = data;
          });
          },
          getGroups(){
    apiService.getGroups().then((data) => {
        console.log(data)
        this.groups = data;
        this.numberOfGroups= data.length;
    });},
          computeStats(id){
            if(id!=undefined) {
              var groupM = this.groupstat.find(g => g.gid == id && g.gender == 'SEX_M')
              var groupW = this.groupstat.find(g => g.gid == id && g.gender == 'SEX_W')
              var totalUsers = groupM.total_user + groupW.total_user
              return {total_user: totalUsers, total_men: groupM.total_user, total_women: groupW.total_user}
            }
              return {total_user: 0, total_men: 0, total_women: 0}
          }


        },
    mounted() {

          this.getGroupStats();
          this.getGroups()
    },
  }
</script>

<style scoped>

</style>
