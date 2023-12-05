<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col text-center">
        <h1 class="display-4 mb-4">Product Listing</h1>
      </div>
    </div>
    <div class="row">
      <div class="col col-md-6">
        <!-- Search Box -->
        <div class="mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Search by name..."
            v-model="searchQuery"
          />
        </div>
      </div>
      <div class="col col-md-6">
        <!-- Sort Dropdown -->
        <div class="mb-3">
          <select class="form-select" v-model="sortOption">
            <option value="name">Sort by Name</option>
            <option value="price">Sort by Price</option>
          </select>
        </div>
      </div>
    </div>
    <!-- Product Cards -->
    <div class="row">
      <div
        v-for="product in sortedProducts"
        :key="product.id"
        class="col-12 col-md-4 mb-4"
      >
        <div class="card h-100">
          <div
            class="card-body d-flex flex-column align-items-center justify-content-between"
          >
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">Category: {{ product.category }}</p>
            <p class="card-text">
              Price per Unit: ${{ product.price.toFixed(2) }}
            </p>
            <!-- Quantity Selection Dropdown -->
            <div class="mb-2">
              <label for="quantity">Quantity:</label>
              <input
                type="number"
                v-model="product.qty"
                class="form-control"
                id="quantity"
                min="1"
                :max="product.maxQty"
              />
            </div>
            <button @click="addToCart(product)" class="btn btn-primary mt-auto">
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      cart: [],
      searchQuery: "",
      sortOption: "name",
      products: [
        {
          id: 1,
          name: "Product 1",
          description: "Description 1",
          category: "Category A",
          price: 10.99,
          qty: 1,
          maxQty: 5,
          image: "path/to/image1.jpg",
        },
        {
          id: 2,
          name: "Product 2",
          description: "Description 2",
          category: "Category B",
          price: 15.99,
          qty: 1,
          maxQty: 8,
          image: "path/to/image2.jpg",
        },
        {
          id: 3,
          name: "Product 3",
          description: "Description 2",
          category: "Category B",
          price: 5.99,
          qty: 1,
          maxQty: 9,
          image: "path/to/image2.jpg",
        },
      ],
      categories: [
        { id: "A", name: "Category A" },
        { id: "B", name: "Category B" },
      ],
    };
  },
  computed: {
    sortedProducts() {
      return this.products
        .filter((product) =>
          product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
        .sort((a, b) => {
          if (this.sortOption === "name") {
            return a.name.localeCompare(b.name);
          } else if (this.sortOption === "price") {
            return a.price - b.price;
          }
          return 0;
        });
    },
  },
  methods: {
    addToCart(product) {
      this.cart.push({ ...product, quantity: product.qty });
    },
  },
};
</script>

<style scoped>
/* Custom styles for enhanced visual appeal */

h1 {
  color: #007bff;
}

.card {
  border: 1px solid #ddd;
  border-radius: 10px;
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.02);
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.card-text {
  color: #6c757d;
}

.form-control,
.form-select {
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style>
