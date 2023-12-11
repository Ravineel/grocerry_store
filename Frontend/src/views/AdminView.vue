<template>
  <div class="container-fluid p-5">
    <!-- <div class="row d-flex justify-content-center">
      <div class="card card-graph">
        <div class="card-body">
          <div class="card-body">
            <div class="card-title text-center">
              <h1>Sales graph</h1>
            </div>
            <div class="chart-area">
              <LineChart />
            </div>
          </div>
        </div>
      </div>
    </div> -->
    <div class="row d-flex justify-content-center mt-3">
      <div class="col-12 col-md-6 mt-1">
        <div class="card card-user">
          <div class="card-body">
            <div class="card-body">
              <div class="card-title text-center">
                <h1>User Counts</h1>
              </div>
              <div class="chart-area">
                <BarChart :chartType="'user'" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-6 mt-1">
        <div class="card card-man">
          <div class="card-body">
            <div class="card-body">
              <div class="card-title text-center">
                <h1>Store Managers</h1>
              </div>

              <div class="chart-area">
                <BarChart />
              </div>
              <div class="card-text text-center mt-3">
                <router-link to="/admin/manager">
                  <button class="btn btn-primary">View Managers</button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row d-flex justify-content-center mt-3">
      <div class="col-12 col-md-4 mt-1">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <div class="card-title text-center">
                <h2>Requests</h2>
              </div>
              <div class="card-text">
                <h4 class="text-center">
                  Total Request Made: {{ totalRequest }}
                </h4>
              </div>
              <div class="card-text text-center m-1">
                <router-link to="/admin/request">
                  <button class="btn btn-primary">View Requests</button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4 mt-1">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <div class="card-title text-center">
                <h2>Categories</h2>
              </div>
              <div class="card-text">
                <h4 class="text-center">
                  Total Categories: {{ totalCategory }}
                </h4>
              </div>
              <div class="card-text text-center m-1">
                <router-link to="/admin/category">
                  <button class="btn btn-primary">View Categories</button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4 mt-1">
        <div class="card">
          <div class="card-body">
            <div class="card-body">
              <div class="card-title text-center">
                <h2>Products</h2>
              </div>
              <div class="card-text">
                <h4 class="text-center">Total Products: {{ totalProduct }}</h4>
              </div>
              <div class="card-text text-center m-1">
                <router-link to="/admin/product">
                  <button class="btn btn-primary">View Products</button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BarChart from "@/components/charts/BarChart.vue";
import LineChart from "../components/charts/LineChart.vue";

export default {
  name: "AdminView",
  components: {
    BarChart,
    LineChart,
  },

  data() {
    return {
      totalRequest: 0,
      totalCategory: 0,
      totalProduct: 0,
    };
  },
  created() {
    this.$store.dispatch("categories/getRequestCategoryAdmin").then((data) => {
      if (!sessionStorage.getItem("isAuthenticated")) {
        this.$router.push("/login");
      } else if (this.$store.getters["categories/error"]) {
        this.$toast.error(this.$store.getters["categories/error"]);
      }
      this.totalRequest = data.length;
    });

    this.$store.dispatch("categories/getAllCategories").then((data) => {
      if (!sessionStorage.getItem("isAuthenticated")) {
        this.$router.push("/login");
      } else if (this.$store.getters["categories/error"]) {
        this.$toast.error(this.$store.getters["categories/error"]);
      }
      this.totalCategory = data.length;
    });
    this.$store.dispatch("products/getAllProducts").then((data) => {
      if (!sessionStorage.getItem("isAuthenticated")) {
        this.$router.push("/login");
      } else if (this.$store.getters["products/error"]) {
        this.$toast.error(this.$store.getters["products/error"]);
      }
      this.totalProduct = data.length;
    });
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

.card:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.card-man,
.card-user {
  min-height: 400px !important;
}

.btn-outline-primary {
  color: #007bff;
  border-color: #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: #fff;
}

/* Additional styling for dark background */
.container-fluid {
  margin-top: -20px;
  min-height: 100vh;
  color: #fff;
  background-color: #1e1e2b;
}
</style>
