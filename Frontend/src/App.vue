<template>
  <div class="container-fluid">
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
  box-sizing: border-box;
}
</style>
