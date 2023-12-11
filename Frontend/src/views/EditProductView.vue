<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col">
        <h1 class="text-center">Edit Product</h1>
      </div>
    </div>
    <form @submit.prevent="editProduct">
      <div className="row mt-2 mt-md-5">
        <div className="col-12 col-md-6">
          <div className="mb-3">
            <label for="name" className="form-label">Product Name</label>
            <input
              type="text"
              v-model="formdata.product_name"
              className="form-control"
              id="name"
              required
            />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="description" class="form-label"
              >Product Description</label
            >
            <input
              class="form-control"
              v-model="formdata.description"
              id="description"
              required
            />
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="category" class="form-label">Category Name</label>
            <select
              class="form-select"
              v-model="formdata.category_id"
              id="category"
              required
            >
              <option
                v-for="category in $store.state.categories.categories"
                :key="category.category_id"
                :value="category.category_id"
              >
                {{ category.category_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="manufacturer" class="form-label"
              >Manufacturer Name</label
            >
            <input
              type="text"
              v-model="formdata.manufacturer"
              class="form-control"
              id="manufacturer"
              required
            />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="manufacturerDate" class="form-label"
              >Manufacturing Date</label
            >
            <input
              type="date"
              v-model="formdata.mfg_date"
              class="form-control"
              id="manufacturerDate"
              required
            />
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input
              type="number"
              v-model="formdata.rate"
              class="form-control"
              id="price"
              min="0"
              step="0.01"
              required
            />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="quantity" class="form-label">Quantity</label>
            <input
              type="number"
              v-model="formdata.qty"
              class="form-control"
              id="quantity"
              required
            />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="unit" class="form-label">Unit</label>
            <input
              type="text"
              v-model="formdata.unit"
              class="form-control"
              id="unit"
              required
            />
          </div>
        </div>

        <div className="d-flex justify-content-center pt-1 mb-4">
          <button className="btn btn-dark btn-lg" type="submit">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "EditProductView",

  data() {
    return {
      formdata: null,
    };
  },
  beforeMount() {
    this.formdata = {
      product_name: "",
      description: "",
      category_id: "",
      manufacturer: "",
      rate: "",
      qty: "",
      unit: "",
      mfg_date: "",
      product_id: "",
    };
  },
  created() {
    this.$store.dispatch("categories/getAllCategories");
    const productId = this.$route.params.product_id;

    if (productId) {
      this.$store
        .dispatch("products/getProductById", productId)
        .then((res) => {
          if (res) {
            this.formdata = {
              product_id: res.product_id,
              product_name: res.product_name,
              description: res.description,
              category_id: res.category_id,
              manufacturer: res.manufacturer,
              rate: res.rate,
              qty: res.qty,
              unit: res.unit,
              mfg_date: moment(res.mfg_date).format("YYYY-MM-DD"),
            };
          } else {
            console.error("Product data not found");
          }
        })
        .catch((error) => {
          console.error("Error fetching product data:", error);
        });
    }
  },

  methods: {
    editProduct() {
      this.$store
        .dispatch("products/updateProduct", this.formdata)
        .then((res) => {
          if (this.$store.getters["products/error"]) {
            this.$toast.error(this.$store.getters["products/error"]);
          } else {
            this.$toast.success("Product Update Successfully");
            if (sessionStorage.getItem("userRole") == 2) {
              this.$router.push({ name: "Manager" });
            } else if (sessionStorage.getItem("userRole") == 3) {
              this.$router.push({ name: "AdminProduct" });
            }
          }
        });
    },
  },
};
</script>

<style scoped>
.form-label {
  font-weight: bold;
  color: #333;
}

.form-control {
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  padding: 0.5rem;
}

.form-select {
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  padding: 0.5rem;
}

.container {
  border: 1px solid #ced4da;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  padding: 2rem;
  background-color: #fff;
}
</style>
