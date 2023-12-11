<template>
  <div class="container-fluid">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h3 class="mb-0 text-center">Login</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Email</label>
                <input
                  type="text"
                  v-model="email"
                  class="form-control"
                  id="email"
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
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    login() {
      try {
        this.$store
          .dispatch("user/login", {
            email: this.email,
            password: this.password,
          })
          .then(() => {
            if (this.$store.getters["user/isAuthenticated"]) {
              // Redirect to Home view or any other route
              this.$router.push({ name: "Home" });
              this.$toast.success("Login successful!");
            } else {
              console.log(this.$store.getters["user/getErrors"]);
              // Handle unsuccessful login, e.g., show an error message
              this.$toast.error(this.$store.getters["user/getErrors"]);
            }
          });
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>

<style scoped>
.card {
  border: 0;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-radius: 10px 10px 0 0;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style>
