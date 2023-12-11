<template>
  <button :class="btnClass">
    {{ value }}
  </button>
</template>

<script>
export default {
  name: "ManagerStatusRenderer",
  data() {
    return {
      btnClass: "btn btn-sm m-1",
      value: "",
    };
  },

  beforeMount() {
    console.log(this.params.data);
    // is_manager_active: true
    if (this.params.data.is_manager_active === true) {
      this.btnClass += " btn-success";
    } else {
      this.btnClass += " btn-danger";
    }

    this.value =
      this.params.data.is_manager_active === true ? "Active" : "Inactive";
  },
};
</script>

<style scoped>
.btn {
  width: 100%;
  border-radius: 50px;
  border: none;
  outline: none;
  box-shadow: none;

  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 0;
}
</style>
