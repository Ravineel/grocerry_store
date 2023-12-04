<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-12">
        <h1>Login</h1>
      </div>
    </div>
    <div class="row">
      <div class="col col-md-6">
        <UserLogin />
      </div>
    </div>
  </div>
</template>

<script>
import UserLogin from "@/components/UserLogin.vue";
export default {
  name: "Login",
  components: {
    UserLogin,
  },
};
</script>
