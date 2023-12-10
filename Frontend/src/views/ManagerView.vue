<template>
  <div class="container-fluid p-5">
    <div class="row justify-content-center">
      <div class="col-12 mt-3">
        <div class="card">
          <div class="card-body">
            <div class="card-title text-center">
              <h4>Your Requests</h4>
            </div>
            <div class="card-text">
              <ManagerRequestTable />
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 mt-3">
        <div class="card">
          <div class="card-body">
            <div class="card-title text-center">
              <h4>Category Table</h4>
            </div>
            <div class="card-text mb-2">
              <button class="btn btn-primary" @click="onClickCreateCategory">
                Create Request for Category
              </button>
            </div>
            <div class="card-text">
              <ManagerCategoryTable />
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 mt-3">
        <div class="card">
          <div class="card-body">
            <div class="card-title text-center">
              <h4>Products Table</h4>
            </div>
            <div class="card-text mb-2">
              <button class="btn btn-primary" @click="onClickCreateProduct">
                Create Product
              </button>
            </div>
            <div class="card-text">
              <ManagerProductTable />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ManagerProductTable from "@/components/ManagerProductTable.vue";
import ManagerCategoryTable from "@/components/ManagerCategoryTable.vue";
import ManagerRequestTable from "@/components/ManagerRequestTable.vue";

export default {
  name: "ManagerView",
  components: {
    ManagerProductTable,
    ManagerCategoryTable,
    ManagerRequestTable,
  },
  methods: {
    onClickCreateProduct() {
      this.$router.push("/product/create");
    },
    onClickCreateCategory() {
      this.$router.push("/category/create");
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  color: #343a40;
}

.btn-outline-primary:hover {
  color: #fff;
  background-color: #007bff;
  border-color: #007bff;
}
</style>
