import Vue from "vue";
import VueRouter from "vue-router";
import LoginView from "../views/Login.vue";
import AdminDashView from "../views/AdminDash.vue";
import AdminAddShowView from "../views/AdminAddShow.vue";
import AdminEditShowView from "../views/AdminEditShow.vue";
import UserDashView from "../views/UserDash.vue";
import ShowBookingView from "../views/ShowBooking.vue";
import UserBookingView from "../views/UserBooking.vue";
import PreviewPage from "../views/Preview.vue";
import SearchShowView from "../views/SearchShow.vue";
import AnalyticsView from "../views/Analytics.vue";
import RateShowView from "../views/RateShow.vue";

Vue.use(VueRouter);

function isAuthenticatedAsAdmin() {
  const user = JSON.parse(localStorage.getItem("userSession"));
  return user !== null && user.role === "admin";
}

function isAuthenticatedAsUser() {
  const user = JSON.parse(localStorage.getItem("userSession"));
  return user !== null && user.role === "user";
}

const routes = [
  {
    path: "/",
    name: "preview",
    component: PreviewPage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/admin/dash",
    name: "admin-dash",
    component: AdminDashView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["admin"],
    },
  },
  {
    path: "/admin/:id/add-show",
    name: "admin-add-show",
    component: AdminAddShowView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["admin"],
    },
  },
  {
    path: "/admin/:id/edit-show",
    name: "admin-edit-show",
    component: AdminEditShowView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["admin"],
    },
  },
  {
    path: "/user/dash",
    name: "user-dash",
    component: UserDashView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["user"],
    },
  },
  {
    path: "/show/:id/booking",
    name: "show-booking",
    component: ShowBookingView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["user"],
    },
  },
  {
    path: "/rate/:id/show",
    name: "rate-show",
    component: RateShowView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["user"],
    },
  },
  {
    path: "/user/booking",
    name: "user-booking",
    component: UserBookingView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["user"],
    },
  },
  {
    path: "/search/:term",
    name: "search",
    component: SearchShowView,
    props: true,
    meta: {
      requiresAuth: true,
      allowedRoles: ["admin", "user"],
    },
  },
  {
    path: "/theater/:id/analytics",
    name: "analytics",
    component: AnalyticsView,
    meta: {
      requiresAuth: true,
      allowedRoles: ["admin"],
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth) {
    if (!isAuthenticatedAsAdmin() && !isAuthenticatedAsUser()) {
      // If user is not logged in, redirect to login page
      next({ name: "login" });
    } else {
      // Check if the route specifies allowed roles
      const allowedRoles = to.meta.allowedRoles;

      if (allowedRoles) {
        // If allowedRoles is defined, check if the user has the required role
        const user = JSON.parse(localStorage.getItem("userSession"));
        const userRole = user.role;

        if (!allowedRoles.includes(userRole)) {
          // User does not have the required role for this route
          next({ name: "login" });
        } else {
          // User has the required role, allow access
          next();
        }
      } else {
        // No allowedRoles specified, allow access
        next();
      }
    }
  } else {
    // No authentication required, allow access
    next();
  }
});

export default router;
