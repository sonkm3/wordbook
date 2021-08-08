<template>
    <v-app>
        <v-card width="40%" class="mx-auto mt-5">
            <v-card-title>
                <h1 class="display-1">Signup</h1>
            </v-card-title>
            <v-card-text>
                <v-form>

                    <v-text-field
                        v-model="email"
                        required
                        label="email"
                        :error-messages="errorMessages.email"
                    />
                    <v-text-field
                        v-model="password"
                        required
                        :type="showPassword ? 'text' : 'password'"
                        label="password"
                        :error-messages="errorMessages.password"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showPassword = !showPassword"
                    />

                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn class="info" @click="signup">Signup</v-btn>
            </v-card-actions>
        </v-card>
    </v-app>
</template>


<script>
export default {
  name: 'Signup',
  middleware: 'auth',
  auth: 'guest',
  data: () => ({
    showPassword: false,
    email: '',
    password:'',
    errorMessages:{'email':[], 'password': []},
  }),
  methods:{
    signup(){
        this.loading = true;
        this.$axios.post(
            `/auth/users/`,
            {
                'email': this.email,
                'password': this.password,
            }
        ).then((response) => {
            this.loading = false;
            this.$router.push('/signin')
        }).catch((err) => {
            this.loading = false;
            this.errorMessages.email = err.response.data.email ? err.response.data.email : [];
            this.errorMessages.password = err.response.data.password ? err.response.data.password : [];
        });
    },
  }
};

</script>

