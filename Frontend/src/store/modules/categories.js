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

  async getCategoryById({ commit }, payload) {},

  async createCategoryAdmin({ commit }, payload) {},
  async updateCategoryAdmin({ commit }, payload) {},
  async deleteCategoryAdmin({ commit }, payload) {},

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
        sessionStorage.setItem("isAuthenticated", false);
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
        sessionStorage.setItem("isAuthenticated", false);
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

  async getRequestCategoryAdmin({ commit }) {},

  async approveRequestCategory({ commit }, payload) {},
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
