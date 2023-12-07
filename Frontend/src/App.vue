<template>
  <div class="app-container">
    <Navbar />

    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import Navbar from "@/views/NavbarView.vue";
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
