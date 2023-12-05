<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col text-center">
        <h1 class="display-4 mb-4">Shopping Cart</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div v-if="cart.length === 0" class="alert alert-info" role="alert">
          Your cart is empty.
        </div>
        <div v-else>
          <div v-for="(item, index) in cart" :key="index" class="card mb-3">
            <div
              class="card-body d-flex justify-content-between align-items-center"
            >
              <div>
                <h5 class="card-title">{{ item.name }}</h5>
                <p class="card-text">
                  Price per Unit: ${{ item.price.toFixed(2) }}
                </p>
                <p class="card-text">Quantity: {{ item.quantity }}</p>
              </div>
              <button @click="removeFromCart(index)" class="btn btn-danger">
                Remove
              </button>
            </div>
          </div>
          <div class="text-end">
            <h5>Total: ${{ calculateTotal().toFixed(2) }}</h5>
            <button @click="checkout" class="btn btn-success">Checkout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Cart",
  props: {
    cart: Array,
  },
  methods: {
    removeFromCart(index) {
      this.$emit("remove-from-cart", index);
    },
    calculateTotal() {
      return this.cart.reduce(
        (total, item) => total + item.price * item.quantity,
        0
      );
    },
    checkout() {
      // Add your checkout logic here
      alert("Checkout functionality is not implemented in this example.");
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
