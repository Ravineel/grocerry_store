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
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav mr-auto">
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
            <button
              type="button"
              class="nav-link btn btn-link"
              data-bs-toggle="modal"
              data-bs-target="#cartModal"
            >
              <v-icon name="hi-solid-shopping-cart" scale="1.3" />
            </button>
          </li>
          <li
            class="nav-item"
            v-if="
              isAuthenticated &&
              (userRole === 'admin' || userRole === 'manager')
            "
          >
            <router-link to="/manager" class="nav-link"
              >Manager Dashboard</router-link
            >
          </li>
          <li class="nav-item" v-if="isAuthenticated && userRole === 'admin'">
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
  created() {
    this.isAuthenticated = sessionStorage.getItem("isAuthenticated");
    const role = sessionStorage.getItem("userRole");
    this.userRole = this.roles[sessionStorage.getItem("userRole")];
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
