<template>
  <div class="app-container">
    <Navbar :key="has_changed" />
    <router-view :key="$route.fullPath" />
  </div>
</template>

<script>
import { RouterView } from "vue-router";
import Navbar from "@/views/NavbarView.vue";

export default {
  name: "App",
  components: {
    Navbar,
    RouterView,
  },
  data() {
    return {
      has_changed: true,
    };
  },
  watch: {
    $route(to, from) {
      this.has_changed = !this.has_changed;
    },
  },
};
</script>

<style>
* {
  margin: 0%;
  padding: 0%;
  box-sizing: border-box;
}
.app-container {
  width: 100%;
  margin: 0%;
  padding: 0%;
  box-sizing: border-box;
}
body {
  margin: 0;
}
</style>
