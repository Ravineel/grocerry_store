import { createRouter, createWebHistory } from "vue-router";
import CartView from "../views/CartView.vue";
import HomeView from "../views/DashboardView.vue";
import LoginView from "../views/LoginView.vue";
import AdminView from "../views/AdminView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
    },

    {
      path: "/login",
      name: "Login",
      component: LoginView,
    },
    {
      path: "/admin",
      name: "Admin",
      component: AdminView,
    },
    {
      path: "/cart",
      name: "Cart",
      component: CartView,
    },
  ],
});

export default router;
