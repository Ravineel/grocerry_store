<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col">
        <h1 class="text-center">Edit Category</h1>
      </div>
    </div>
    <form @submit.prevent="editCategory">
      <div className="row mt-2 mt-md-5">
        <div className="col-12 col-md-6">
          <div className="mb-3">
            <label for="name" className="form-label">Category Name</label>
            <input
              type="text"
              v-model="formdata.category_name"
              className="form-control"
              id="name"
              required
            />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="mb-3">
            <label for="description" class="form-label"
              >Category Description</label
            >
            <input
              class="form-control"
              v-model="formdata.description"
              id="description"
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
export default {
  name: "EditCategoryView",
  data() {
    return {
      formdata: {
        category_name: "",
        description: "",
        type: "UPDATE",
      },
    };
  },

  created() {
    const categoryId = this.$route.params.category_id;

    if (categoryId) {
      this.$store
        .dispatch("categories/getCategoryById", categoryId)
        .then((res) => {
          if (res) {
            this.formdata = {
              category_id: res.category_id,
              category_name: res.category_name,
              description: res.description,
              type: "UPDATE",
            };
          } else {
            console.error("category data not found");
          }
        })
        .catch((error) => {
          console.error("Error fetching category data:", error);
        });
    }
  },

  methods: {
    editCategory() {
      const userRole = sessionStorage.getItem("userRole");
      console.log(userRole);

      if (userRole === "2") {
        console.log("manager");
        this.$store
          .dispatch("categories/createCategoryRequestManager", this.formdata)
          .then((res) => {
            if (this.$store.getters["categories/error"]) {
              this.$router.push("/manager");
              this.$toast.error(this.$store.getters["categories/error"]);
            } else {
              this.$router.push({ name: "Manager" });
              this.$toast.success("Request for Category Created Successfully");
            }
          });
      } else if (userRole === "3") {
        this.$store
          .dispatch("categories/updateCategoryAdmin", this.formdata)
          .then((res) => {
            if (this.$store.getters["categories/error"]) {
              this.$router.push("/admin");
              this.$toast.error(this.$store.getters["categories/error"]);
            } else {
              this.$router.push({ name: "AdminCategory" });
              this.$toast.success("Category Created Successfully");
            }
          });
      }
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
