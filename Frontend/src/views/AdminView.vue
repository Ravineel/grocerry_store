<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col text-center">
        <h1><i class="fas fa-user-cog"></i> Admin Dashboard</h1>
      </div>
    </div>
    <div class="row mt-2">
      <button @click="toggleCategoriesTable" class="btn btn-primary">
        View Categories
      </button>
      <div v-if="showCategoriesTable" class="mt-2">
        <div class="col mt-1">
          <button class="btn btn-outline-danger btn-sm">
            Create New Category
          </button>
        </div>
        <div class="row mt-2">
          <AdminCategoryTableVue />
        </div>
      </div>
    </div>
    <div class="row mt-3">
      <button @click="toggleProductsTable" class="btn btn-success">
        View Products
      </button>
      <div v-if="showProductsTable" class="mt-2">
        <div class="col mt-1">
          <button class="btn btn-outline-danger btn-sm">
            Create New Product
          </button>
        </div>
        <div class="row mt-2">
          <AdminProductTableVue />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import AdminCategoryTableVue from "@/components/AdminCategoryTable.vue";
import AdminProductTableVue from "@/components/AdminProductTable.vue";
export default {
  components: {
    AdminCategoryTableVue,
    AdminProductTableVue,
  },
  setup() {
    const showCategoriesTable = ref(true);
    const showProductsTable = ref(true);

    const toggleCategoriesTable = () => {
      showCategoriesTable.value = !showCategoriesTable.value;
    };

    const toggleProductsTable = () => {
      showProductsTable.value = !showProductsTable.value;
    };

    return {
      showCategoriesTable,
      showProductsTable,
      toggleCategoriesTable,
      toggleProductsTable,
    };
  },
};
</script>
