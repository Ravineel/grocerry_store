export const API_ENDPOINTS = {
  CATEGORY: {
    GET_ALL: "/category/get/all",
    GET_BY_ID: "/category/get",
    ADMIN: {
      CREATE: "/category/admin/create",
      UPDATE: "/category/admin/update",
      DELETE: "/category/admin/delete",
    },
    MANAGER: {
      CREATE_REQUEST: "/category/manager/request/create",
      GET_REQUEST: "/category/manager/request/get",
    },
    REQUEST: {
      GET_ALL: "/category/request/get/all",
      APPROVE: "/category/request/approval",
    },
  },
  PRODUCT: {
    GET_ALL: "/product/get/all",
    GET_BY_ID: "/product/get",
    CREATE: "/product/create",
    UPDATE: "/product/update",
    DELETE: "/product/delete",
  },
  USER: {
    LOGIN: "/user/login",
    SIGNUP: "/user/signup",
    ADMIN: {
      GET_MANAGERS: "/admin/get/manager",
      UPDATE_MANAGER: "/admin/update/manager",
      GET_MANAGER_DATA: "/admin/get/manager_data",
      GET_DATA_COUNT: "/admin/get/data_count",
    },
  },
  ORDER: {
    CHECKOUT: "/order/checkout",
    GET_ALL: "/order/get/all",
    GET_BY_ID: "/order/get",
  },
};
