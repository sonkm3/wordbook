<template>
    <span>
        <span v-if="$auth.user">
            {{$auth.user['email']}}
        </span>
        <nuxt-link
            v-if="$auth.user"
            to='/signout'
        >
            signout
        </nuxt-link>
    </span>
</template>

<script>
export default {
  name: 'AccountMenu',
  data() {
    return {
    };
  },
  methods:{
  }
};
</script>



