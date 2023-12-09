<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Grocery Store</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/login" class="nav-link" v-if="!isAuthenticated"
              >Login</router-link
            >
          </li>
          <li class="nav-item">
            <router-link to="/logout" class="nav-link" v-if="isAuthenticated"
              >Logout</router-link
            >
          </li>
          <li class="nav-item">
            <router-link to="/cart" class="nav-link">
              <v-icon name="hi-solid-shopping-cart" scale="1.3" />
            </router-link>
          </li>
          <li class="nav-item" v-if="showManagerDashboardLink">
            <router-link to="/manager" class="nav-link"
              >Manager Dashboard</router-link
            >
          </li>
          <li class="nav-item" v-if="showAdminDashboardLink">
            <router-link to="/Admin" class="nav-link"
              >Admin Dashbaord</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",

  data() {
    return {
      isAuthenticated: false,
      userRole: null,
      roles: ["guest", "user", "manager", "admin"],
    };
  },
  computed: {
    showManagerDashboardLink() {
      return (
        this.isAuthenticated &&
        (this.userRole === "admin" || this.userRole === "manager")
      );
    },
    showAdminDashboardLink() {
      return this.isAuthenticated && this.userRole === "admin";
    },
  },
  watch: {
    isAuthenticated(newVal) {
      // Handle changes in isAuthenticated
      console.log("isAuthenticated changed:", newVal);
    },
    userRole(newVal) {
      // Handle changes in userRole
      console.log("userRole changed:", newVal);
    },
  },
  created() {
    console.log(sessionStorage.getItem("isAuthenticated"));
    this.isAuthenticated = sessionStorage.getItem("isAuthenticated");
    console.log(this.isAuthenticated);
    const role = sessionStorage.getItem("userRole")
      ? sessionStorage.getItem("userRole")
      : 0;
    this.userRole = this.roles[role];
  },
};
</script>

<style scoped>
.navbar {
  width: 100%;
  margin: 0%;
  padding: auto;
  margin-bottom: 20px;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.navbar {
  background-color: #50e0b0;
}
</style>
