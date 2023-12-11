<template>
  <div class="container-fluid p-5">
    <div class="row justify-content-center">
      <div class="col-12 mt-3">
        <div class="card">
          <div class="card-body">
            <div class="card-title text-center mb-5">
              <h1>Products</h1>
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
import ManagerProductTable from "../components/ManagerProductTable.vue";

export default {
  name: "AdminProductView",
  components: {
    ManagerProductTable,
  },
  methods: {
    onClickCreateProduct() {
      this.$router.push("/product/create");
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid rgba(255, 255, 255, 0.125);
  border-radius: 0.5rem;
  transition: box-shadow 0.3s;
  background: #27293d;
  color: #fff;
  margin-bottom: 20px;
}

.card {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
.card {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
}

.btn-outline-primary {
  color: #007bff;
  border-color: #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: #fff;
}

.container-fluid {
  margin-top: -20px;
  min-height: 100vh;
  color: #fff;
  background-color: #1e1e2b;
}
</style>
