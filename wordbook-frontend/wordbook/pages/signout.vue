<template>
    <v-app>
        <v-card width="40%" class="mx-auto mt-5">
            <v-card-title>
                <h1 class="display-1">Signout</h1>
            </v-card-title>
            <v-card-actions>
                <v-btn class="info" @click="signout">Signout</v-btn>
            </v-card-actions>
        </v-card>
    </v-app>
</template>

<script>
export default {
  name: 'Signout',
  data: () => ({}),
  methods:{
    signout(){
        this.$auth.logout('local')
    }
  }
};
</script>

