<template>

  <div style="margin-left: 10px;">
    <div style="background-color: #E8EFF0; margin-top: 10px; width: available; margin-bottom: 5px; padding: 5px;">
      <h4 class="card-title">Create New Group</h4>
    </div>

    <b-form @submit.stop.prevent="onSubmit">

      <b-form-group id="example-input-group-1" label="ID" label-for="example-input-1">
        <b-form-input
          id="id"
          name="id"
          readonly
          v-model="$v.form.id.$model"
          :state="$v.form.id.$dirty ? !$v.form.id.$error : null"
          aria-describedby="input-1-live-feedback"
        ></b-form-input>

        <b-form-invalid-feedback id="input-1-live-feedback">
          This is a required field.
        </b-form-invalid-feedback>
      </b-form-group>


      <b-form-group id="example-input-group-1" label="Name" label-for="example-input-1">
        <b-form-input
          id="name"
          name="example-input-1"
          v-model="$v.form.name.$model"
          :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
          aria-describedby="input-1-live-feedback"
        ></b-form-input>

        <b-form-invalid-feedback id="input-1-live-feedback">
          This is a required field. Minimum 3 chars.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="example-input-group-1" label="State" label-for="example-input-1">
        <b-form-input
          id="state"
          name="state"
          value="recruitment"
          readonly

        ></b-form-input>


      </b-form-group>

      <b-form-group id="example-input-group-1" label="Created at" label-for="example-input-1">
        <b-form-input
          id="createdat"
          name="createdat"

          readonly
          v-model="this.datestamp"

        ></b-form-input>


      </b-form-group>

      <b-button type="submit" variant="primary" :disabled="$v.form.$invalid">Submit</b-button>
    </b-form>
  </div>
</template>

<script>
  import {validationMixin} from 'vuelidate'
  import {required, minLength} from 'vuelidate/lib/validators'
  import {APIService} from "../api/APIService";

  const APU_URL = 'http://localhost:8000';
  const apiService = new APIService();

  export default {
    mixins: [validationMixin],
    data() {
      return {
        group: [],
        datestamp: '',

        form: {
          id: null,
          name: null,

        }
      }
    },
    validations: {
      form: {

        id: {

          required,
        },
        name: {
          required,
          minLength: minLength(3),

        }
      }
    },
    methods: {
      create: function () {

        //let id = document.getElementById('id').value;

        let name = document.getElementById('name').value
        let state = 'recruitment'
        let today = new Date();
        let date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
        let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var dateTime = date + ' ' + time;
        var group = {
          'id': this.form.id,
          'name': name,
          'state': state,
          'created_at': dateTime

        }
        apiService.createGroup(group);


      },
      getGroupId() {

        apiService.getGroupLastId().then((data) => {
          this.group = data;
          this.form.id = this.group['id']
          console.log(data['id'])
        })

      },

      onSubmit() {
        this.$v.form.$touch()
        if (this.$v.form.$anyError) {
          return
        }

        this.create()
        // Form submit logic
      }

    },
    mounted() {
      console.log('Test')
      let today = new Date();
      let date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
      let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      var dateTime = date + ' ' + time;
      this.datestamp = dateTime;
      this.getGroupId();
      console.log(this.form.id + ' ' + this.datestamp)
    }
  }
</script>
