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

  getGroupUserList(id){
    const url = `${API_URL}/api/groupuserlist/${id}`;
    return axios.get(url).then(response => response.data);

  }

}
