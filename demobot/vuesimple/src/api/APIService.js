import axios from 'axios';


const API_URL = 'http://localhost:8000';


export class APIService {

  constructor() {
  }

//Groups data retrieval
  getGroups() {
    const url = `${API_URL}/api/group/`;
    //var result = axios.get(url).then(response => {console.log(response)})
    return axios.get(url).then(response => response.data);
  }

  getGroup(id) {
    const url = `${API_URL}/api/group/${id}`;
    return axios.get(url).then(response => response.data);
  }

// User data retrieval

  getUsers() {
    const url = `${API_URL}/api/user/`;
    return axios.get(url).then(response => response.data);
  }

  getUsers(id) {
    const url = `${API_URL}/api/user/${id}`;
    return axios.get(url).then(response => response.data);
  }

// Group Statistics info retrieval

  getGroupStats() {
    const url = `${API_URL}/api/groupstat/`;
    return axios.get(url).then(response => response.data);
  }

  getGroupGadget() {
    const url = `${API_URL}/api/groupgadget/`;
    return axios.get(url).then(response => response.data);
  }

  getGroupGadget(id) {
    const url = `${API_URL}/api/groupgadget/${id}`;
    return axios.get(url).then(response => response.data);
  }


  getGroupUserList() {
    const url = `${API_URL}/api/groupuserlist/`;
    return axios.get(url).then(response => response.data);
  }

  getGroupUserList(id) {
    const url = `${API_URL}/api/groupuserlist/${id}`;
    return axios.get(url).then(response => response.data);

  }

  getUserProfile() {
    const url = `${API_URL}/api/userprofile/`;
    return axios.get(url).then(response => response.data);


  }

  getGroupPie() {

    const url = `${API_URL}/api/grouppie/`;
    return axios.get(url).then(response => response.data);

  }

  getGroupPie(id) {
    const url = `${API_URL}/api/grouppie/${id}`;
    return axios.get(url).then(response => response.data);

  }

  getGroupMood() {

    const url = `${API_URL}/api/groupmood/`;
    return axios.get(url).then(response => response.data);

  }

  /*
     getGroupMood(id) {
      const url = `${API_URL}/api/groupmood/${id}`;
      return axios.get(url).then(response => response.data);
    }
  */

  getGroupTotal() {

    const url = `${API_URL}/api/grouptotal/`;
    return axios.get(url).then(response => response.data);

  }

  getUserMood(id) {
    const url = `${API_URL}/api/usermood/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getUserDistract(id) {
    const url = `${API_URL}/api/userdistract/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getUserAlone(id) {
    const url = `${API_URL}/api/useralone/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getUserDrive(id) {
    const url = `${API_URL}/api/userdrive/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getGroupContext() {
    const url = `${API_URL}/api/groupcontext/`;
    return axios.get(url).then(response => response.data);
  }

  getGroupContext(id) {
    const url = `${API_URL}/api/groupcontext/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getGroupMoodAll() {
    const url = `${API_URL}/api/groupmoodall/`;
    return axios.get(url).then(response => response.data);
  }

  getGroupMoodAll(id) {
    const url = `${API_URL}/api/groupmoodall/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getGroupDesireAll(id) {
    const url = `${API_URL}/api/groupdesireall/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getGroupMotivationAll(id) {
    const url = `${API_URL}/api/groupmotivationall/${id}`;
    return axios.get(url).then(response => response.data);
  }

  getUserDetails(id) {
    const url = `${API_URL}/api/userdetails/${id}`;
    return axios.get(url).then(response => response.data)
  }

  getGroupDetails(id) {
    const url = `${API_URL}/api/groupdetails/${id}`;
     return axios.get(url).then(response => response.data);
  }

  updateGroup(group){

    //const url = `${API_URL}/api/group/${id}`;
    const url = `${API_URL}/api/group/${group.id}/`;
    return axios.put(url, group).then(response => response.data);
    console.log(group)

   // return axios.patch(url, data).then(response => response.data);
}


}
