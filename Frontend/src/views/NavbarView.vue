<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
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
      isAuthenticated: sessionStorage.getItem("isAuthenticated"),
      userRole: sessionStorage.getItem("userRole"),
    };
  },
  computed: {
    showManagerDashboardLink() {
      return this.isAuthenticated && this.userRole === "2";
    },
    showAdminDashboardLink() {
      return this.isAuthenticated && this.userRole === "3";
    },
  },
  watch: {
    isAuthenticated(newVal) {
      console.log("isAuthenticated changed:", newVal);
    },
    userRole(newVal) {
      console.log("userRole changed:", newVal);
    },
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
  background-color: #1e1e2f;
  color: #fff;
}

.navbar-brand,
.navbar-nav .nav-link {
  color: #fff !important;
}

.navbar-dark .navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='30' height='30' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.8%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}
</style>
