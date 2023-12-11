// initial state
const state = () => ({
  categories: [],

  requestCategories: [],

  isloading: false,
  error: null,

  created: false,
  requestCreated: false,
});

// getters
const getters = {
  categories: (state) => state.categories,
  requestCategories: (state) => state.requestCategories,

  isloading: (state) => state.isloading,
  error: (state) => state.error,

  created: (state) => state.created,
  requestCreated: (state) => state.requestCreated,
};

// actions
const actions = {
  async getAllCategories({ commit }) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/get/all",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setCategories", data);
        commit("setLoading", false);
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  async getCategoryById({ commit }, payload) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/v1/category/get/${payload}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setCategories", data);
        commit("setLoading", false);
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  // '/api/v1/category/admin/create','/api/v1/category/admin/update','/api/v1/category/admin/delete'

  async createCategoryAdmin({ commit }, payload) {
    commit("setLoading", true);
    commit("setCreated", false);
    commit("setError", null);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/admin/create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },
  async updateCategoryAdmin({ commit }, payload) {
    commit("setLoading", true);
    commit("setCreated", false);
    commit("setError", null);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/admin/update",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setCreated", false);
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },
  async deleteCategoryAdmin({ commit }, payload) {
    commit("setLoading", true);
    commit("setError", null);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/admin/delete",
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  async createCategoryRequestManager({ commit }, payload) {
    commit("setLoading", true);
    commit("setRequestCreated", false);
    commit("setError", null);

    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/manager/request/create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setRequestCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        console.log("An error occured: ", data.error_message);
      } else {
        commit("setRequestCreated", false);
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  async getRequestCategoryManager({ commit }) {
    commit("setLoading", true);
    commit("setError", null);
    commit("requestCategories", []);
    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/manager/request/get",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
        }
      );
      const status = response.status;
      const data = await response.json();

      if (status === 200) {
        commit("setRequestCategories", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", "SERVER ERROR");
      commit("setLoading", false);
    }
  },

  async getRequestCategoryAdmin({ commit }) {
    commit("setLoading", true);
    commit("setError", null);
    commit("setRequestCategories", []);
    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/category/request/get/all",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
        }
      );
      const status = response.status;
      const data = await response.json();
      console.log(data);
      if (status === 200) {
        commit("setRequestCategories", data);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },

  async approveRequestCategory({ commit }, payload) {
    commit("setLoading", true);
    commit("setError", null);
    commit("setRequestCreated", false);
    try {
      const response = await fetch(
        `http://localhost:5000/api/v1/category/request/approval`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            authorization: `Bearer ${sessionStorage.getItem("userToken")}`,
          },
          body: JSON.stringify(payload),
        }
      );
      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setRequestCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);

        if (data.error_code === "TOKEN_EXPIRED") {
          commit("setError", "Your session has expired. Please login again.");
        }
        if (data.error_code === "TOKEN_INVALID") {
          commit("setError", "Your session is invalid. Please login again.");
        }
        if (data.error_code === "INVALID_ROLE") {
          commit("setError", "You are not authorized to perform this action.");
        }
        return data;
      } else {
        commit("setLoading", false);
        commit("setError", data.error_message);
      }
    } catch (err) {
      console.log("An error occured: ", err);
      commit("setError", err);
      commit("setLoading", false);
    }
  },
};

// mutations
const mutations = {
  setCategories: (state, categories) => (state.categories = categories),
  setRequestCategories: (state, requestCategories) =>
    (state.requestCategories = requestCategories),

  setLoading: (state, loading) => (state.isloading = loading),
  setError: (state, error) => (state.error = error),

  setCreated: (state, created) => (state.created = created),
  setRequestCreated: (state, requestCreated) =>
    (state.requestCreated = requestCreated),
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
