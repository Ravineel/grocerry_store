import { createStore, createLogger } from "vuex";

import products from "./modules/products";
import categories from "./modules/categories";
import orders from "./modules/orders";
import user from "./modules/user";
import checkout from "./modules/checkout";

const debug = process.env.NODE_ENV !== "production";

export default createStore({
  modules: {
    products,
    categories,
    orders,
    products,
    user,
    checkout,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});
