<template>
  <div class="container-fluid">
    <div
      class="modal fade"
      id="cartModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="cartModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog odal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Shopping Cart</h5>
            <button
              type="button"
              class="close"
              @click="closeCartModal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <!-- Display cart items here -->
            <div v-if="cart.length === 0">
              <p>Your cart is empty.</p>
            </div>
            <div v-else>
              <div v-for="cartItem in cart" :key="cartItem.product_id">
                <p>
                  <strong>{{ cartItem.product_name }}</strong> - Quantity:
                  {{ cartItem.quantity }} - ₹{{ cartItem.total.toFixed(2) }}
                </p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeCartModal"
            >
              Close
            </button>
            <button type="button" class="btn btn-primary">Checkout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CartModal",

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
    closeCartModal() {
      console.log("Closing cart modal");
      // Emit a custom event to notify the parent component to close the modal
      this.$emit("close-cart-modal");
    },
  },

  created() {
    this.loadCartFromLocalStorage();
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
