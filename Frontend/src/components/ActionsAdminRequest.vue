<!-- ActionsRenderer.vue -->
<template>
  <div class="d-flex justify-content-center align-items-center">
    <button
      class="btn btn-sm btn-success m-1"
      @click="onApproveClick()"
      v-if="isApproved && !approvalProcessed"
    >
      Approve
    </button>
    <button
      class="btn btn-sm btn-danger m-1"
      @click="onRejectClick()"
      v-if="isApproved && !approvalProcessed"
    >
      Reject
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      approvalProcessed: false,
    };
  },
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
      this.approvalProcessed = true;
      this.params.onApprove(this.params.data);
    },
    onRejectClick() {
      this.approvalProcessed = true;
      this.params.onReject(this.params.data);
    },
  },
};
</script>

<style scoped></style>
