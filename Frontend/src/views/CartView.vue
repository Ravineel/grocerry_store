<template>
  <div class="container">
    <h1 class="display-4 mb-4">Shopping Cart</h1>

    <!-- Display cart items here -->
    <div v-if="cart.length === 0" class="alert alert-info">
      Your cart is empty.
    </div>
    <div v-else>
      <div
        v-for="cartItem in cart"
        :key="cartItem.product_id"
        class="card mb-3"
      >
        <div class="card-body">
          <h5 class="card-title">
            <strong>{{ cartItem.product_name }}</strong>
          </h5>
          <p class="card-text">
            Quantity:
            <input
              type="number"
              v-model="cartItem.quantity"
              @input="updateCartItem(cartItem)"
              min="1"
              class="form-control d-inline w-25"
            />
            <span class="mx-2">-</span> ₹{{ cartItem.total.toFixed(2) }}
            <button
              type="button"
              class="btn btn-link text-danger float-end"
              @click="removeItem(cartItem)"
            >
              Remove
            </button>
          </p>
        </div>
      </div>

      <!-- Display total cost -->
      <div class="mt-4">
        <h4>Total Cost: ₹{{ calculateTotalCost().toFixed(2) }}</h4>
      </div>
    </div>

    <div class="modal-footer">
      <router-link to="/" class="btn btn-secondary">
        Continue Shopping
      </router-link>
      <button
        type="button"
        class="btn btn-primary"
        @click="checkout"
        :disabled="cart.length === 0"
      >
        Checkout
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CartView",

  data() {
    return {
      cart: [], // Initialize cart from local storage on component creation
    };
  },

  methods: {
    // Load cart from local storage on component creation
    loadCartFromLocalStorage() {
      const storedCart = localStorage.getItem("cart");
      this.cart = storedCart ? JSON.parse(storedCart) : [];
    },
    checkout() {
      // Add your checkout logic here

      const payload = {
        products: this.cart,
      };

      this.$store
        .dispatch("checkout/createOrder", payload)
        .then((res) => {
          if (sessionStorage.getItem("isAuthenticated")) {
            this.cart = [];
            localStorage.removeItem("cart");
            if (this.$store.getters["checkout/created"]) {
              this.$router.push({ name: "Home" });
              this.$toast.success("Order placed successfully! ");
            } else {
              this.$toast.warning(this.$store.getters["checkout/error"]);
              this.$toast.error("Order failed! ");
            }
          } else {
            this.$router.push({ name: "Login" });
            this.$toast.success("Session Expired! Please Login Again!");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    calculateTotalCost() {
      return this.cart.reduce((total, cartItem) => total + cartItem.total, 0);
    },
    updateCartItem(cartItem) {
      // Update total cost when quantity changes
      cartItem.total = cartItem.quantity * cartItem.rate;
      this.saveCartToLocalStorage();
    },
    removeItem(cartItem) {
      // Remove item from cart
      this.cart = this.cart.filter(
        (item) => item.product_id !== cartItem.product_id
      );
      this.saveCartToLocalStorage();
    },
    saveCartToLocalStorage() {
      localStorage.setItem("cart", JSON.stringify(this.cart));
    },
  },

  created() {
    this.loadCartFromLocalStorage();
  },
};
</script>

<style scoped>
/* Add your custom styles here */
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.02);
}
</style>
