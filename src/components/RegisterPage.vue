<template>
  <div class="text-center" data-gr-c-s-loaded="true">
    <!--    <h2>Register</h2>-->
    <form @submit.prevent="handleSubmit" class="form-signin">
      <img alt="" class="mb-4" height="72" src="../assets/owl.svg"
           width="72">
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input :class="{ 'is-invalid': submitted && errors.has('firstName') }" class="form-control"
               name="firstName" placeholder="Ex. Ivan" type="text" v-model="user.firstName" v-validate="'required'"/>
        <div class="invalid-feedback" v-if="submitted && errors.has('firstName')">{{ errors.first('firstName') }}
        </div>
      </div>
      <div class="form-group">
        <label for="lastName">Last Name</label>
          <input :class="{ 'is-invalid': submitted && errors.has('lastName') }" class="form-control"
                 name="lastName" placeholder="Ex. Ivanov" type="text" v-model="user.lastName" v-validate="'required'"/>
          <div class="invalid-feedback" v-if="submitted && errors.has('lastName')">{{ errors.first('lastName') }}
          </div>
      </div>
      <div class="form-group">
        <label for="username">Username</label>
          <input :class="{ 'is-invalid': submitted && errors.has('username') }" class="form-control"
                 name="username" placeholder="Ex. i.ivanov@innopolis.ru" type="text" v-model="user.username"
                 v-validate="'required'"/>
          <div class="invalid-feedback" v-if="submitted && errors.has('username')">{{ errors.first('username') }}
          </div>
      </div>
      <div class="form-group">
        <label htmlFor="password">Password</label>
          <input :class="{ 'is-invalid': submitted && errors.has('password') }" class="form-control"
                 name="password" placeholder="Password" type="password" v-model="user.password"
                 v-validate="{ required: true, min: 6 }"/>
          <div class="invalid-feedback" v-if="submitted && errors.has('password')">{{ errors.first('password') }}
          </div>
      </div>
      <div class="form-group">
        <button :disabled="status.registering" class="btn btn-primary">Register</button>
        <img
          src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
          v-show="status.registering"/>
        <router-link class="btn btn-link" to="/login">Cancel</router-link>
      </div>
    </form>
    <p class="mt-5 mb-3 text-muted">Students breakdown team</p>
  </div>
</template>

<script>
  import {mapActions, mapState} from 'vuex'

  export default {
    data() {
      return {
        user: {
          firstName: '',
          lastName: '',
          username: '',
          password: ''
        },
        submitted: false
      }
    },
    computed: {
      ...mapState('account', ['status'])
    },
    methods: {
      ...mapActions('account', ['register']),
      handleSubmit(e) {
        this.submitted = true;
        this.$validator.validate().then(valid => {
          if (valid) {
            this.register(this.user);
          }
        });
      }
    }
  };
</script>


<style scoped>
  .form-signin {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;

  }

  *, ::after, ::before {

    box-sizing: border-box;

  }
</style>
