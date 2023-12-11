<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="card">
        <div class="card-header">
          <h3 class="mb-0 text-center">Signup</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="signup">
            <div class="row">
              <div class="col-12 col-md-6">
                <div class="mb-3">
                  <label for="firstName" class="form-label"
                    >First Name<span className="required-asterisk">
                      *</span
                    ></label
                  >
                  <input
                    type="text"
                    v-model="first_Name"
                    class="form-control"
                    id="firstName"
                    required
                  />
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="mb-3">
                  <label for="lastName" class="form-label"
                    >Last name<span className="required-asterisk">
                      *</span
                    ></label
                  >
                  <input
                    type="text"
                    v-model="last_Name"
                    class="form-control"
                    id="lastName"
                    required
                  />
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12 col-md-6">
                <div class="mb-3">
                  <label for="email" class="form-label"
                    >Email<span className="required-asterisk"> *</span></label
                  >
                  <input
                    type="text"
                    v-model="email"
                    class="form-control"
                    id="email"
                    required
                  />
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="mb-3">
                  <label for="password" class="form-label"
                    >Password<span className="required-asterisk">
                      *</span
                    ></label
                  >
                  <input
                    type="password"
                    v-model="password"
                    class="form-control"
                    id="password"
                    required
                  />
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12 col-md-6">
                <div class="mb-3">
                  <!-- option for user role  -->
                  <label for="role" class="form-label"
                    >Role<span className="required-asterisk"> *</span>
                  </label>
                  <select
                    class="form-select"
                    v-model="role"
                    aria-label="Default select example"
                    required
                  >
                    <option value="user">User</option>
                    <option value="manager">Manager</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Signup</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupForm",
  data() {
    return {
      first_Name: "",
      last_Name: "",
      email: "",
      password: "",
      role: null,
    };
  },
  methods: {
    signup() {
      try {
        this.$store
          .dispatch("user/signup", {
            first_name: this.first_Name,
            last_name: this.last_Name,
            email: this.email,
            password: this.password,
            role: this.role,
          })
          .then(() => {
            if (this.$store.getters["user/SignedUp"]) {
              this.$emit("signup-success");
              this.$toast.success("Signup successful");
            }
          });
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>
