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
    piechartdata: {},
    usermoodcontainer:{}
  },


  mutations: {
    SET_GROUPGADGET(state, groupgadget){
      console.log('commiting mutation '+groupgadget)
      state.groupgadget = groupgadget
      state.chartdata = groupgadget
    },

    SET_USERDESIREDATA(state, userdesiredata ){
      state.userdesiredata = userdesiredata
    },

     SET_PIECHARTDATA(state, piechartdata ){
      state.piechartdata = piechartdata
    },
    SET_USERMOODCONTAINER(state, usermoodcontainer){
      state.usermoodcontainer = usermoodcontainer
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
    },
    LOAD_PIECHARTDATA_with_id({commit}, id){
      apiService.getGroupPie('?gid='+id).then(data => {
        commit('SET_PIECHARTDATA', data)
      });
    },
    LOAD_USERMOODCONTAINER_WITH_id({commit}, id){
      apiService.getUserMood('?id='+id).then(data => {
        console.log('calling mutation')
          commit('SET_USERMOODCONTAINER', data)
        });
    },

  },
  getters: {
    getChart(state){
      return state.chartdata;
    },
    getDesire(state){
      return state.userdesiredata;
    },
    getPiechart(state){
      return state.piechartdata;
    }
  }
})
