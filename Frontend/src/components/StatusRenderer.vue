<template>
  <button :class="btnClass">
    {{ value }}
  </button>
</template>

<script>
export default {
  name: "StatusRenderer",
  data() {
    return {
      btnClass: "btn  m-1",
      value: "",
    };
  },

  beforeMount() {
    if (this.params.data.request_status === "PENDING") {
      this.btnClass += " btn-warning";
    } else if (this.params.data.request_status === "APPROVED") {
      this.btnClass += " btn-success";
    } else if (this.params.data.request_status === "REJECTED") {
      this.btnClass += " btn-danger";
    }

    this.value = this.params.data.request_status;
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
