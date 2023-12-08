import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.js";
import ToastPlugin from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

import { OhVueIcon, addIcons } from "oh-vue-icons";
import { HiSolidShoppingCart } from "oh-vue-icons/icons";

addIcons(HiSolidShoppingCart);

const app = createApp(App);
app.component("v-icon", OhVueIcon);

app.use(ToastPlugin, {
  position: "top-right",
  duration: 3000,
  dismissible: true,
});
app.use(store);
app.use(router);

app.mount("#app");
