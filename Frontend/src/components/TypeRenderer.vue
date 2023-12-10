<template>
  <button :class="btnClass">
    {{ value }}
  </button>
</template>

<script>
export default {
  name: "TypeRenderer",
  data() {
    return {
      btnClass: "btn btn-sm m-1",
      value: "",
    };
  },

  beforeMount() {
    if (this.params.data.type === "CREATE") {
      this.btnClass += " btn-primary";
    } else if (this.params.data.type === "UPDATE") {
      this.btnClass += " btn-warning";
    } else if (this.params.data.type === "DELETE") {
      this.btnClass += " btn-danger";
    }

    this.value = this.params.data.type;
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
