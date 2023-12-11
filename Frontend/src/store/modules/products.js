// initial state
const state = () => ({
  products: [],

  isloading: false,
  error: null,
  created: false,
});

// getters
const getters = {
  products: (state) => state.products,
  isloading: (state) => state.isloading,
  error: (state) => state.error,
  created: (state) => state.created,
};

// actions using fetch api
const actions = {
  async getAllProducts({ commit }) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        "http://localhost:5000/api/v1/product/get/all",
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
        commit("setProducts", data);
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

  async getProductById({ commit }, payload) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/v1/product/get/${payload}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const status = response.status;
      const data = await response.json();
      console.log(data);

      if (status === 200) {
        commit("setProducts", data);
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
  async createProduct({ commit }, payload) {
    commit("setLoading", true);
    commit("setError", null);
    commit("setCreated", false);
    try {
      console.log("payload: ", payload);
      const response = await fetch(
        "http://localhost:5000/api/v1/product/create",
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

      if (status === 201) {
        commit("setCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);
        commit("setCreated", false);

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

  async updateProduct({ commit }, payload) {
    commit("setLoading", true);
    commit("setError", null);
    commit("setCreated", false);
    try {
      console.log("payload: ", payload);
      const response = await fetch(
        "http://localhost:5000/api/v1/product/update",
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

      console.log(data);
      if (status === 200) {
        commit("setCreated", true);
        commit("setLoading", false);
        return data;
      } else if (status === 401) {
        sessionStorage.removeItem("userToken");
        sessionStorage.removeItem("isAuthenticated");
        commit("setLoading", false);
        commit("setCreated", false);

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

  async deleteProduct({ commit }, payload) {
    commit("setLoading", true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/v1/product/delete`,
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
};

// mutations
const mutations = {
  setProducts: (state, products) => (state.products = products),
  setLoading: (state, loading) => (state.isloading = loading),
  setError: (state, error) => (state.error = error),
  setCreated: (state, created) => (state.created = created),
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
