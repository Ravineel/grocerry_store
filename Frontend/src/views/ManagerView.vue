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
              <button class="btn btn-primary m-1" @click="onClickCreateProduct">
                Create Product
              </button>
              <button class="btn btn-info m-1" @click="onClickDownlaodReport">
                Downlaod Report
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
    async onClickDownlaodReport() {
      const res = await fetch(
        "http://0.0.0.0:5000/api/v1/manager/get/product_report"
      );
      const data = await res.json();

      if (res.ok) {
        this.$toast.success("Report has been triggered successfully");

        const task_id = data.task_id;
        console.log(task_id);

        const interval = setInterval(async () => {
          const csv_res = await fetch(
            `http://0.0.0.0:5000/api/v1/manager/get/csv_report/${task_id}`
          );
          if (csv_res.ok) {
            this.$toast.success("Report will download now");
            clearInterval(interval);
            window.location.href = `http://0.0.0.0:5000/api/v1/manager/get/csv_report/${task_id}`;
          }
        }, 5000);
      }
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
