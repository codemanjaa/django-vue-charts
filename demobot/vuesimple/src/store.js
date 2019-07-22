import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import {APIService} from "./api/APIService";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

export default new Vuex.Store({
  state: {
    groupgadget : [],
    chartdata : [],
    userdesiredata: {},

    piechartdata: {
          labels: ['Men', 'Women'],
          datasets: [
            {

              label: 'Gender Ratio',
              backgroundColor: ['#3a2ff8', '#ef5ef9'],
              data: []
            }
          ],
        },
  },


  mutations: {
    SET_GROUPGADGET(state, groupgadget){
      console.log('commiting mutation '+groupgadget)
      state.groupgadget = groupgadget
      state.chartdata = groupgadget
    },

    SET_USERDESIREDATA(state, userdesiredata ){
      state.userdesiredata = userdesiredata
    }


  },
  actions: {
    load_groupgadget({commit}){
      apiService.getGroupGadget().then(data => {
        console.log('calling mutation')
          commit('SET_GROUPGADGET', data)
        });
    },
    load_groupgadget_with_id({commit}, id){
      apiService.getGroupGadget('?gid='+id).then(data => {
        console.log('calling mutation')
          commit('SET_GROUPGADGET', data)
        });
    },
    LOAD_USERDESIREDATA({commit}){
      apiService.getUserProfile().then(data => {
        commit('SET_USERDESIREDATA', data)
      });
    }
  },
  getters: {
    getChart(state){
      return state.chartdata;
    },
    getDesire(state){
      return state.userdesiredata;
    }
  }
})
