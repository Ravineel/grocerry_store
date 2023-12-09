<template>
  <div class="container-fluid p-5">
    <div class="row d-flex justify-content-center">
      <div class="col-12 mt-2">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <h4 class="card-title text-center">Products Table</h4>
            </div>
            <div class="card-text m-1">
              <button class="btn btn-outline-primary" @click="onClickCreate">
                Create Product
              </button>
            </div>
            <div class="card-text">
              <ManagerProductTable />
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 mt-2">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <h4 class="card-title text-center">Category Table</h4>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 mt-2">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <h4 class="card-title text-center">Your Requests</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ManagerProductTable from "@/components/ManagerProductTable.vue";
export default {
  name: "ManagerView",
  components: {
    ManagerProductTable,
  },
  data() {
    return {};
  },
  methods: {
    onClickCreate() {
      this.$router.push("/manager/create");
    },
  },
};
</script>
