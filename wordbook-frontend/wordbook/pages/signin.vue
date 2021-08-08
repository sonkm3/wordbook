<template>
    <v-app>
        <v-card width="40%" class="mx-auto mt-5">
            <v-card-title>
                <h1 class="display-1">Signin</h1>
            </v-card-title>
            <v-card-text>
                <v-form>
                    <v-text-field
                        v-model="email"
                        required
                        label="email"
                        :error-messages="errorMessage"
                    />
                    <v-text-field
                        v-model="password"
                        required
                        :type="showPassword ? 'text' : 'password'"
                        label="password"
                        :error-messages="errorMessage"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showPassword = !showPassword"
                    />
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn class="info" @click="signin">Signin</v-btn>
            </v-card-actions>
        </v-card>
    </v-app>
</template>


<script>
import axios from "axios";

export default {
  name: 'Signin',
  middleware: 'auth',
  auth: 'guest',
  data: () => ({
    showPassword: false,
    email: '',
    password:'',
    errorMessage:[],
  }),
  methods:{
    signin(){
        this.$auth.loginWith('local',{
            data:{'email': this.email, 'password': this.password}
        }).then (response => {
            axios.defaults.headers.common.Authorization = this.$auth.strategy.token.get();
            this.$router.push('/courses')
        }).catch((err) => {
            this.loading = false;
            this.errorMessage = err.response.data.nonFieldErrors ? err.response.data.nonFieldErrors : [];
        })
    }
  }
};

</script>

