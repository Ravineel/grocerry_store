<template>
  <div class="container-fluid">
    <ul class="nav nav-tabs" role="tablist">
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'login' }"
          @click="changeTab('login')"
          data-toggle="tab"
          href="#loginTab"
          >Login</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'signup' }"
          @click="changeTab('signup')"
          data-toggle="tab"
          href="#signupTab"
          >Signup</a
        >
      </li>
    </ul>

    <div class="tab-content">
      <div
        class="tab-pane"
        :class="{ active: activeTab === 'login' }"
        id="loginTab"
      >
        <UserLogin />
      </div>
      <div
        class="tab-pane"
        :class="{ active: activeTab === 'signup' }"
        id="signupTab"
      >
        <Signup @signup-success="changeTab('login')" />
      </div>
    </div>
  </div>
</template>

<script>
import UserLogin from "@/components/UserLogin.vue";
import Signup from "@/components/Signup.vue";

export default {
  name: "Login",
  components: {
    UserLogin,
    Signup,
  },
  data() {
    return {
      activeTab: "login",
    };
  },
  methods: {
    changeTab(tab) {
      this.activeTab = tab;
    },
  },
};
</script>
