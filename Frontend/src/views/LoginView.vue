<template>
  <div class="container-fluid">
    <div class="row">
      <UserLogin />
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
