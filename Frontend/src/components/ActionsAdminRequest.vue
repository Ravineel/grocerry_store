<!-- ActionsRenderer.vue -->
<template>
  <div class="d-flex justify-content-center align-items-center">
    <button
      class="btn btn-sm btn-success m-1"
      @click="onApproveClick()"
      v-if="isApproved"
    >
      Approve
    </button>
    <button
      class="btn btn-sm btn-danger m-1"
      @click="onRejectClick()"
      v-if="isApproved"
    >
      Reject
    </button>
  </div>
</template>

<script>
export default {
  computed: {
    isApproved() {
      if (this.params.data.request_status === "PENDING") {
        return true;
      } else {
        return false;
      }
    },
  },

  methods: {
    onApproveClick() {
      this.isApproved = false;
      this.params.onApprove(this.params.data);
    },
    onRejectClick() {
      this.isApproved = false;
      this.params.onReject(this.params.data);
    },
  },
};
</script>

<style scoped></style>
