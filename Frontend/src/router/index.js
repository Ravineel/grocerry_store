import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/DashboardView.vue";
import LoginView from "../views/LoginView.vue";
import AdminView from "../views/AdminView.vue";

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
      component: AdminView,
      meta: {
        requiresAuth: true,
        requiresRole: ["manager", "admin"],
      },
    },
    {
      path: "/logout",
      name: "Logout",
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
  const publicPages = ["/login", "/"];
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
    !to.meta.requiresRole.includes(role[loggedInUserRole])
  ) {
    console.log(to.meta.requiresRole);
    console.log(role[loggedInUserRole]);
    next(false);
    $toast.error("You don't have permission to access this page!");
  }
  // User is logged in and trying to access a public page
  else if (isAuthorized && to.name == "Login") {
    next(false);
    $toast.info("You are already logged in!");
  }
  //User clicks logout, redirect to login and clear session storage
  else if (to.name == "Logout") {
    sessionStorage.clear();
    next({ name: "Login" });
    $toast.info("You have been logged out!");
  } else {
    // Continue with the navigation
    next();
  }
});

export default router;
