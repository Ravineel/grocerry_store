<template>
  <div class="container mt-5">
    <h2>User Login</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          v-model="username"
          class="form-control"
          id="username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="password"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "UserLogin",
  data() {
    return {
      userUsername: "",
      userPassword: "",
    };
  },
  mounted() {
    console.log("UserLogin component mounted");
  },
  methods: {
    userlogin() {
      // Your login logic
    },
  },
};
</script>

<style scoped></style>
