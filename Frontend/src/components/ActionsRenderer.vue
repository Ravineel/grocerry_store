<!-- ActionsRenderer.vue -->
<template>
  <div class="d-flex justify-content-center align-items-center">
    <button class="btn btn-sm btn-warning m-1" @click="onEditClick()">
      Edit
    </button>
    <button class="btn btn-sm btn-danger m-1" @click="onDeleteClick()">
      Delete
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    onEditClick() {
      this.params.onEdit(this.params.data);
    },
    onDeleteClick() {
      this.params.onDelete(this.params.data);
    },
  },
};
</script>
