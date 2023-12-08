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

  async getProductById({ commit }, payload) {},
  async createProduct({ commit }, payload) {},
  async updateProduct({ commit }, payload) {},
  async deleteProduct({ commit }, payload) {},
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
