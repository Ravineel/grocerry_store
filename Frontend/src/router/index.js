import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/DashboardView.vue";
import LoginView from "../views/LoginView.vue";
import AdminView from "../views/AdminView.vue";
import CartView from "../views/CartView.vue";
import ManagerView from "../views/ManagerView.vue";
import ProductCreateView from "../views/CreateProductView.vue";
import ProductEditView from "../views/EditProductView.vue";
import CategoryCreateView from "../views/CreateCategoryView.vue";
import EditCategoryView from "../views/EditCategoryView.vue";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

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
      path: "/logout",
      name: "Logout",
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/cart",
      name: "Cart",
      component: CartView,
    },

    {
      path: "/admin",
      name: "Admin",
      component: AdminView,
      meta: {
        requiresAuth: true,
        requiresRole: ["admin"],
      },
    },
    {
      path: "/manager",
      name: "Manager",
      component: ManagerView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
    {
      path: "/product/create",
      name: "CreateProduct",
      component: ProductCreateView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
    {
      path: "/product/edit/:product_id",
      name: "EditProduct",
      component: ProductEditView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
    {
      path: "/category/create",
      name: "CreateCategory",
      component: CategoryCreateView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
    {
      path: "/category/edit/:category_id",
      name: "EditCategory",
      component: EditCategoryView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
  ],
});

// role
// 0 - guest
// 1 - user
// 2 - manager
// 3 - admin

router.beforeEach((to, from, next) => {
  const $toast = useToast({ position: "top-right", duration: 3000 });
  const publicPages = ["/login", "/", "/cart"];
  const authRequired = !publicPages.includes(to.path);
  const loggedInUserRole = sessionStorage.getItem("userRole");
  const role = ["guest", "user", "manager", "admin"];
  const isAuthorized = sessionStorage.getItem("isAuthenticated") === "true";

  // User is not logged in and trying to access a protected route
  if (!isAuthorized && authRequired) {
    next({ name: "Login" });
    $toast.error("Please log in to access this page!");
  }
  // User is logged in but doesn't have the required role
  else if (
    isAuthorized &&
    authRequired &&
    to.meta.requiresRole &&
    !to.meta.requiresRole.includes(role[loggedInUserRole])
  ) {
    next(false);
    $toast.error("You don't have permission to access this page!");
  }
  // User is logged in and trying to access a public page
  else if (isAuthorized && to.name == "Login") {
    next(false);
    $toast.info("You are already logged in!");
  }
  // User clicks logout, clear session storage and redirect to login
  else if (to.name == "Logout") {
    // Clear session storage
    sessionStorage.clear();
    // Set isAuthenticated to false
    sessionStorage.setItem("isAuthenticated", false);
    // Redirect to the login page
    next({ name: "Login" });
    $toast.info("You have been logged out!");
  } else {
    // Continue with the navigation
    next();
  }
});

export default router;
