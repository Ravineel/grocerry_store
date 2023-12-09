<template>
  <div class="container-fluid mt-4">
    <div class="row">
      <div class="col text-center">
        <h1 class="display-4 mb-4">Product Listing</h1>
      </div>
    </div>
    <div class="row mb-4">
      <!-- Search Boxes and Sort Dropdown -->
      <div class="col-12 col-sm-6 col-md-3 mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by name..."
          v-model="searchQuery"
        />
      </div>
      <div class="col-12 col-sm-6 col-md-3 mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by category..."
          v-model="searchCategory"
        />
      </div>
      <div class="col-12 col-sm-6 col-md-3 mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by Manufacturer..."
          v-model="searchMfg"
        />
      </div>
      <div class="col-12 col-sm-6 col-md-3 mb-3">
        <select class="form-select" v-model="sortOption">
          <option value="name">Sort by Name</option>
          <option value="price">Sort by Price</option>
          <option value="mfg_date">Sort by Manufacturing Date</option>
        </select>
      </div>
    </div>
    <!-- Product Cards -->
    <div class="row">
      <div
        v-for="product in sortedProducts"
        :key="product.id"
        class="col-12 col-md-4 mb-4"
      >
        <div class="card h-100 border-primary">
          <div
            class="card-body d-flex flex-column align-items-center justify-content-between"
          >
            <h5 class="card-title text-primary">{{ product.product_name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">Category: {{ product.category_name }}</p>
            <p class="card-text">
              Price per {{ product.unit }}: ₹{{ product.rate.toFixed(2) }}
            </p>
            <p class="card-text">
              Availability:
              <span class="fw-bold text-success" v-if="product.qty > 0">
                Available
              </span>
              <span class="fw-bold text-danger" v-else> Sold Out </span>
            </p>
            <!-- Add to Cart Button -->
            <button
              @click="addToCart(product)"
              class="btn btn-primary"
              v-if="product.qty > 0 && !isInCart(product)"
            >
              Add to Cart
            </button>
            <!-- Quantity Selection Dropdown -->
            <div
              class="mb-2 d-flex align-items-center"
              v-if="isInCart(product)"
            >
              <label for="quantity" class="me-2">Quantity:</label>
              <input
                type="number"
                :value="getCartItemQuantity(product)"
                @input="updateCartItem(product, $event.target.value)"
                class="form-control"
                id="quantity"
                min="1"
                :max="product.qty"
              />
            </div>
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
      showCartModal: false,
      cart: [],
      searchQuery: "",
      sortOption: "name",
      searchCategory: "",
      searchMfg: "",
    };
  },
  computed: {
    sortedProducts() {
      return this.$store.getters["products/products"]
        .filter(
          (product) =>
            product.product_name
              .toLowerCase()
              .includes(this.searchQuery.toLowerCase()) &&
            product.manufacturer
              .toLowerCase()
              .includes(this.searchMfg.toLowerCase()) &&
            product.category_name
              .toLowerCase()
              .includes(this.searchCategory.toLowerCase())
        )
        .sort((a, b) => {
          if (this.sortOption === "name") {
            return a.product_name.localeCompare(b.product_name);
          } else if (this.sortOption === "price") {
            return a.rate - b.rate;
          } else if (this.sortOption === "mfg_date") {
            return new Date(a.mfg_date) - new Date(b.mfg_date);
          }
          return 0;
        });
    },
  },
  methods: {
    addToCart(product) {
      if (!this.isInCart(product)) {
        const cart = {
          product_id: product.product_id,
          product_name: product.product_name,
          category_name: product.category_name,
          category_id: product.category_id,
          rate: product.rate,
          unit: product.unit,
          quantity: 1,
          total: product.rate * 1,
        };
        this.cart.push(cart);
        this.saveCartToLocalStorage();
      }
    },
    isInCart(product) {
      return this.cart.some((item) => item.product_id === product.product_id);
    },
    getCartItemQuantity(product) {
      const cartItem = this.cart.find(
        (item) => item.product_id === product.product_id
      );
      return cartItem ? cartItem.quantity : 0;
    },

    updateCartItem(product, value) {
      const cartItem = this.cart.find(
        (item) => item.product_id === product.product_id
      );
      if (cartItem) {
        cartItem.quantity = parseInt(value, 10);
        cartItem.total = cartItem.quantity * cartItem.rate;
        this.saveCartToLocalStorage();
      }
    },
    loadCartFromLocalStorage() {
      const storedCart = localStorage.getItem("cart");
      this.cart = storedCart ? JSON.parse(storedCart) : [];
    },
    saveCartToLocalStorage() {
      localStorage.setItem("cart", JSON.stringify(this.cart));
    },
  },
  created() {
    this.$store.dispatch("products/getAllProducts").then(() => {
      if (this.$store.getters["products/products"].length === 0) {
        this.$toast.error("Failed to fetch products!");
      } else {
        this.$toast.success("Products fetched successfully!");
      }
    });
    this.loadCartFromLocalStorage();
  },
};
</script>

<style scoped>
h1 {
  color: #007bff;
  font: bold 2.5rem Verdana, Geneva, Tahoma, sans-serif;
}

.card {
  border: 1.5px solid #000000;
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

.text-primary {
  color: #007bff;
}

.text-success {
  color: #28a745;
}

.text-danger {
  color: #dc3545;
}
</style>
