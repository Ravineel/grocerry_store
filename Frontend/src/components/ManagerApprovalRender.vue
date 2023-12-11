<!-- ActionsRenderer.vue -->
<template>
  <div class="d-flex justify-content-center align-items-center">
    <button
      class="btn btn-sm btn-primary m-1"
      @click="onApproveClick()"
      v-if="!state"
    >
      Approve
    </button>
    <button
      class="btn btn-sm btn-danger m-1"
      @click="onRejectClick()"
      v-if="state"
    >
      Deactive
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      state: null,
    };
  },
  created() {
    this.state = this.params.data.is_manager_active;
  },
  methods: {
    onApproveClick() {
      this.params.onApprove(this.params.data);
    },
    onRejectClick() {
      this.params.onReject(this.params.data);
    },
  },
};
</script>
